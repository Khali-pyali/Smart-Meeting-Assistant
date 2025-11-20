import random
from datetime import datetime, timedelta

class AIService:
    @staticmethod
    def summarize_meeting(raw_notes):
        """
        Mock AI summarization.
        In a real app, this would call OpenAI/Gemini API.
        """
        if not raw_notes:
            return "No notes provided to summarize.", [], []

        # Mock logic: Extract sentences as "summary" and random "action items"
        summary = f"Meeting Summary (Generated {datetime.now().strftime('%H:%M')}):\n"
        summary += "The team discussed key project milestones. "
        if "frontend" in raw_notes.lower():
            summary += "Frontend implementation details were reviewed. "
        if "backend" in raw_notes.lower():
            summary += "Backend architecture was finalized. "
        
        # Mock Action Items extraction
        action_items = []
        if "todo" in raw_notes.lower() or "action" in raw_notes.lower():
            action_items.append({
                "description": "Review the deployment pipeline",
                "owner": "DevOps Team",
                "due_date": (datetime.now() + timedelta(days=2)).isoformat(),
                "status": "pending"
            })
        
        # Always add a generic one for demo
        action_items.append({
            "description": "Follow up on meeting points",
            "owner": "Meeting Organizer",
            "due_date": (datetime.now() + timedelta(days=1)).isoformat(),
            "status": "pending"
        })

        # Mock Tags
        tags = ["meeting", "update"]
        if "urgent" in raw_notes.lower():
            tags.append("urgent")
        
        return summary, action_items, tags

    @staticmethod
    def answer_query(query, all_meetings):
        """
        Mock RAG (Retrieval Augmented Generation).
        Searches meetings for keywords in query.
        """
        query_lower = query.lower()
        keywords = query_lower.split()  # Split into individual words
        relevant_meetings = []
        
        for meeting in all_meetings:
            # Simple keyword search in title, notes, or summary (case-insensitive)
            content = (meeting.title + " " + meeting.raw_notes + " " + meeting.ai_summary).lower()
            
            # Check if any keyword matches
            if any(keyword in content for keyword in keywords):
                relevant_meetings.append(meeting)
        
        if not relevant_meetings:
            return "I couldn't find any meetings related to your query. Try asking about specific topics discussed in your meetings, or create some meetings first!"
        
        # Construct a detailed answer
        response = f"I found {len(relevant_meetings)} relevant meeting(s):\n\n"
        for m in relevant_meetings[:5]:  # Limit to 5
            response += f"📅 **{m.title}** ({m.datetime.strftime('%Y-%m-%d %H:%M')})\n"
            
            # Show snippet of notes
            if m.raw_notes:
                snippet = m.raw_notes[:150] + "..." if len(m.raw_notes) > 150 else m.raw_notes
                response += f"   Notes: {snippet}\n"
            
            # Show AI summary if available
            if m.ai_summary:
                summary_snippet = m.ai_summary[:100] + "..." if len(m.ai_summary) > 100 else m.ai_summary
                response += f"   Summary: {summary_snippet}\n"
            
            response += "\n"
        
        return response
