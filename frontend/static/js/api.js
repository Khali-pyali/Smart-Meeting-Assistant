// API Configuration
const API_BASE_URL = window.location.origin; // Use same origin (works locally and on Render)

const api = {
    getMeetings: () => axios.get(`${API_BASE_URL}/api/meetings`),
    getMeeting: (id) => axios.get(`${API_BASE_URL}/api/meetings/${id}`),
    createMeeting: (data) => axios.post(`${API_BASE_URL}/api/meetings`, data),
    updateMeeting: (id, data) => axios.put(`${API_BASE_URL}/api/meetings/${id}`, data),
    deleteMeeting: (id) => axios.delete(`${API_BASE_URL}/api/meetings/${id}`),

    getActionItems: () => axios.get(`${API_BASE_URL}/api/action-items`),
    updateActionItem: (id, data) => axios.put(`${API_BASE_URL}/api/action-items/${id}`, data),

    generateSummary: (meetingId) => axios.post(`${API_BASE_URL}/api/ai/summarize`, { meeting_id: meetingId }),
    askAI: (query) => axios.post(`${API_BASE_URL}/api/ai/ask`, { query })
};
