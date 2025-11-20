// Utility to format dates
const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleString();
};

// Dashboard Logic
async function loadDashboard() {
    const content = document.getElementById('app-content');
    content.innerHTML = `
        <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3" id="meetings-grid">
            <!-- Meetings will be loaded here -->
        </div>
    `;

    try {
        const response = await api.getMeetings();
        const meetings = response.data;
        const grid = document.getElementById('meetings-grid');

        if (meetings.length === 0) {
            grid.innerHTML = `
                <div class="col-span-full text-center py-12 bg-white rounded-lg border border-gray-200 shadow-sm">
                    <i data-lucide="calendar" class="mx-auto h-12 w-12 text-gray-400"></i>
                    <h3 class="mt-2 text-sm font-medium text-gray-900">No meetings</h3>
                    <p class="mt-1 text-sm text-gray-500">Get started by creating a new meeting.</p>
                    <div class="mt-6">
                        <button onclick="openNewMeetingModal()" class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700">
                            <i data-lucide="plus" class="-ml-1 mr-2 h-5 w-5"></i>
                            New Meeting
                        </button>
                    </div>
                </div>
            `;
            lucide.createIcons();
            return;
        }

        grid.innerHTML = meetings.map(meeting => `
            <div class="bg-white overflow-hidden shadow rounded-lg hover:shadow-md transition-shadow cursor-pointer" onclick="window.location.href='/meeting_detail.html?id=${meeting.id}'">
                <div class="px-4 py-5 sm:p-6">
                    <div class="flex items-center justify-between">
                        <h3 class="text-lg leading-6 font-medium text-gray-900 truncate">${meeting.title}</h3>
                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                            ${meeting.participants.length} Participants
                        </span>
                    </div>
                    <div class="mt-2 max-w-xl text-sm text-gray-500">
                        <p><i data-lucide="clock" class="inline w-4 h-4 mr-1"></i> ${formatDate(meeting.datetime)}</p>
                    </div>
                    <div class="mt-4">
                        <div class="flex flex-wrap gap-2">
                            ${meeting.tags.map(tag => `<span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-indigo-100 text-indigo-800">#${tag}</span>`).join('')}
                        </div>
                    </div>
                </div>
            </div>
        `).join('');
        lucide.createIcons();

    } catch (error) {
        console.error('Error loading meetings:', error);
        content.innerHTML = `<div class="text-red-500 text-center">Failed to load meetings. Is the backend running?</div>`;
    }
}

// New Meeting Modal Logic (Simple prompt for now, can be enhanced)
async function openNewMeetingModal() {
    const title = prompt("Enter meeting title:");
    if (!title) return;

    try {
        await api.createMeeting({
            title: title,
            participants: [],
            raw_notes: "",
            tags: []
        });
        window.location.reload();
    } catch (error) {
        alert("Failed to create meeting");
    }
}

// Initialize based on page
document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;
    if (path === '/' || path === '/index.html') {
        loadDashboard();
    }
});
