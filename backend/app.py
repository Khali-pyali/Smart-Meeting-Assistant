from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room
from database import db
from models import Meeting, ActionItem
from services.ai_service import AIService
import os
from datetime import datetime, timezone

app = Flask(__name__, static_folder='../frontend', static_url_path='')
app.config['SECRET_KEY'] = 'smart-meeting-secret-key'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Configure Database
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'meetings.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

# --- Routes ---

@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

# Meetings CRUD
@app.route('/api/meetings', methods=['GET'])
def get_meetings():
    meetings = Meeting.query.order_by(Meeting.datetime.desc()).all()
    return jsonify([m.to_dict() for m in meetings])

@app.route('/api/meetings', methods=['POST'])
def create_meeting():
    data = request.json
    new_meeting = Meeting(
        title=data.get('title', 'Untitled Meeting'),
        datetime=datetime.now(timezone.utc), # Default to now
        participants=data.get('participants', []), # Expecting list, model handles conversion if needed but we set default "[]"
        raw_notes=data.get('raw_notes', ""),
        tags=data.get('tags', [])
    )
    # Handle JSON serialization for storage if using Text column
    import json
    new_meeting.participants = json.dumps(data.get('participants', []))
    new_meeting.tags = json.dumps(data.get('tags', []))
    
    db.session.add(new_meeting)
    db.session.commit()
    return jsonify(new_meeting.to_dict()), 201

@app.route('/api/meetings/<int:id>', methods=['GET'])
def get_meeting(id):
    meeting = Meeting.query.get_or_404(id)
    # Fetch related action items
    action_items = ActionItem.query.filter_by(meeting_id=id).all()
    response = meeting.to_dict()
    response['action_items'] = [ai.to_dict() for ai in action_items]
    return jsonify(response)

@app.route('/api/meetings/<int:id>', methods=['PUT'])
def update_meeting(id):
    meeting = Meeting.query.get_or_404(id)
    data = request.json
    
    if 'title' in data: meeting.title = data['title']
    if 'raw_notes' in data: meeting.raw_notes = data['raw_notes']
    if 'ai_summary' in data: meeting.ai_summary = data['ai_summary']
    if 'meeting_link' in data: meeting.meeting_link = data['meeting_link']
    
    # Handle lists
    import json
    if 'participants' in data: meeting.participants = json.dumps(data['participants'])
    if 'tags' in data: meeting.tags = json.dumps(data['tags'])
    
    db.session.commit()
    return jsonify(meeting.to_dict())

@app.route('/api/meetings/<int:id>', methods=['DELETE'])
def delete_meeting(id):
    meeting = Meeting.query.get_or_404(id)
    db.session.delete(meeting)
    db.session.commit()
    return jsonify({"message": "Meeting deleted"})

# Action Items
@app.route('/api/action-items', methods=['GET'])
def get_action_items():
    items = ActionItem.query.all()
    return jsonify([item.to_dict() for item in items])

@app.route('/api/action-items/<int:id>', methods=['PUT'])
def update_action_item(id):
    item = ActionItem.query.get_or_404(id)
    data = request.json
    if 'status' in data: item.status = data['status']
    if 'owner' in data: item.owner = data['owner']
    db.session.commit()
    return jsonify(item.to_dict())

# AI Features
@app.route('/api/ai/summarize', methods=['POST'])
def summarize_meeting():
    data = request.json
    meeting_id = data.get('meeting_id')
    meeting = Meeting.query.get_or_404(meeting_id)
    
    summary, new_action_items, new_tags = AIService.summarize_meeting(meeting.raw_notes)
    
    # Update meeting
    meeting.ai_summary = summary
    
    # Merge tags
    import json
    current_tags = json.loads(meeting.tags) if meeting.tags else []
    updated_tags = list(set(current_tags + new_tags))
    meeting.tags = json.dumps(updated_tags)
    
    # Create Action Items
    created_items = []
    for item in new_action_items:
        new_ai = ActionItem(
            meeting_id=meeting.id,
            description=item['description'],
            owner=item['owner'],
            due_date=datetime.fromisoformat(item['due_date']) if item['due_date'] else None,
            status=item['status']
        )
        db.session.add(new_ai)
        created_items.append(new_ai)
    
    db.session.commit()
    
    return jsonify({
        "summary": summary,
        "tags": updated_tags,
        "action_items": [ai.to_dict() for ai in created_items]
    })

@app.route('/api/ai/ask', methods=['POST'])
def ask_ai():
    data = request.json
    query = data.get('query')
    if not query:
        return jsonify({"error": "Query required"}), 400
        
    all_meetings = Meeting.query.all()
    answer = AIService.answer_query(query, all_meetings)
    
    return jsonify({"answer": answer})

# WebRTC Signaling
@socketio.on('join_call')
def handle_join_call(data):
    room = data['meeting_id']
    join_room(room)
    emit('user_joined', {'user_id': request.sid}, room=room, include_self=False)

@socketio.on('offer')
def handle_offer(data):
    emit('offer', data, room=data['target'])

@socketio.on('answer')
def handle_answer(data):
    emit('answer', data, room=data['target'])

@socketio.on('ice_candidate')
def handle_ice_candidate(data):
    emit('ice_candidate', data, room=data['target'])

@socketio.on('leave_call')
def handle_leave_call(data):
    room = data['meeting_id']
    leave_room(room)
    emit('user_left', {'user_id': request.sid}, room=room)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=False, allow_unsafe_werkzeug=True)
