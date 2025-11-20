# Smart Meeting & Task Assistant

A full-stack web application to help engineering teams organize meetings, extract action items using AI, and search through past discussions.

## Features

- 📝 **Meeting Management**: Create, view, and edit meeting notes
- 🎥 **Built-in Video Calls**: Start video calls directly in the app using WebRTC
- 🔗 **External Video Links**: Support for Google Meet/Zoom links
- 🤖 **AI-Powered Summarization**: Automatically generate meeting summaries and extract action items
- 🏷️ **Smart Tagging**: Auto-tag meetings based on content
- ✅ **Action Items Tracker**: Centralized dashboard for all tasks across meetings
- 💬 **Ask AI**: Search through your meeting history with natural language queries

## Tech Stack

### Backend
- **Python 3.13** with Flask
- **SQLite** database
- **Flask-SocketIO** for real-time video calling
- **SQLAlchemy** ORM

### Frontend
- **HTML5, CSS3, JavaScript (Vanilla)**
- **Tailwind CSS** for styling
- **WebRTC** for peer-to-peer video calls
- **Axios** for API communication

## Setup & Installation

### Prerequisites
- Python 3.x installed on your system

### Steps

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Smart_meeting_app_by_Surbhi
   ```

2. **Navigate to backend and create virtual environment**
   ```bash
   cd backend
   python -m venv venv
   ```

3. **Activate virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Mac/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install flask flask-sqlalchemy flask-cors flask-socketio python-socketio
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open in browser**
   Navigate to [http://localhost:5000](http://localhost:5000)

## Usage

### Creating a Meeting
1. Click **"+ New Meeting"** on the dashboard
2. Enter a meeting title
3. Add your meeting notes in the notes section
4. Click **"Save Notes"**

### Starting a Video Call
1. Open a meeting
2. Click **"Start Video Call"** button
3. Grant camera/microphone permissions
4. Share the meeting link with others to join

### Using AI Features
1. **Generate Summary**: After adding notes, click **"Generate"** in the AI Summary section
2. **View Action Items**: Extracted tasks appear automatically in the Action Items section
3. **Ask AI**: Go to the "Ask AI" page and ask questions about your past meetings

## Project Structure

```
Smart_meeting_app_by_Surbhi/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── models.py           # Database models
│   ├── database.py         # Database configuration
│   ├── services/
│   │   └── ai_service.py   # Mock AI service
│   └── meetings.db         # SQLite database (auto-generated)
├── frontend/
│   ├── index.html          # Dashboard
│   ├── meeting_detail.html # Meeting view/edit page
│   ├── action_items.html   # Action items table
│   ├── ask_ai.html         # AI search interface
│   ├── video_call.html     # Video call page
│   └── static/
│       └── js/
│           ├── api.js      # API wrapper
│           └── app.js      # Main frontend logic
└── README.md
```

## API Endpoints

- `GET /api/meetings` - List all meetings
- `POST /api/meetings` - Create new meeting
- `GET /api/meetings/:id` - Get meeting details
- `PUT /api/meetings/:id` - Update meeting
- `DELETE /api/meetings/:id` - Delete meeting
- `GET /api/action-items` - List all action items
- `PUT /api/action-items/:id` - Update action item
- `POST /api/ai/summarize` - Generate AI summary
- `POST /api/ai/ask` - Query meetings with AI

## Future Improvements

- Real AI integration (OpenAI/Gemini API)
- User authentication
- Calendar integration
- Email notifications for action items
- Export meetings to PDF
- Voice transcription during video calls
- Advanced search filters

## License

MIT License

## Author

**Surbhi**

---

**Note**: This application uses a mock AI service. For production use, integrate with a real AI API like OpenAI or Google Gemini.
- **Ask AI**: Chat interface to search through your meeting notes.
