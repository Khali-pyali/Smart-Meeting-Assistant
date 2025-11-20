const API_BASE_URL = 'http://localhost:5000/api';

const api = {
    // Meetings
    getMeetings: () => axios.get(`${API_BASE_URL}/meetings`),
    getMeeting: (id) => axios.get(`${API_BASE_URL}/meetings/${id}`),
    createMeeting: (data) => axios.post(`${API_BASE_URL}/meetings`, data),
    updateMeeting: (id, data) => axios.put(`${API_BASE_URL}/meetings/${id}`, data),
    deleteMeeting: (id) => axios.delete(`${API_BASE_URL}/meetings/${id}`),

    // Action Items
    getActionItems: () => axios.get(`${API_BASE_URL}/action-items`),
    updateActionItem: (id, data) => axios.put(`${API_BASE_URL}/action-items/${id}`, data),

    // AI
    generateSummary: (meetingId) => axios.post(`${API_BASE_URL}/ai/summarize`, { meeting_id: meetingId }),
    askAI: (query) => axios.post(`${API_BASE_URL}/ai/ask`, { query })
};
