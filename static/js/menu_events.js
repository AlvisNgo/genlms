$("#menu-notification").click(() => {
    $(".ajax-event-notification").remove();
    $("#menu-notification-header").text("Loading unread events ...");

    $.ajax({
        url: '/api/unread_events', // Replace with your API endpoint
        method: 'GET',
        success: function(response) {
            if (response.success && response.events) {
                $("#menu-notification-number").text(response.events.length);
                $("#menu-notification-header").text(response.events.length + " Notifications");

                response.events.forEach(event => {
                    $("#menu-notification-box .dropdown-divider").last().before(addEvent(event));
                });
            }
        },
        error: function() {
            console.error('Failed to fetch events.');
        }
    });
})

// Function to format the time difference
function timeAgo(dateString) {
    const now = new Date();
    const date = new Date(dateString);
    const diff = Math.floor((now - date) / 60000); // Difference in minutes

    if (diff < 1) return "Just now";
    if (diff < 60) return `${diff} mins`;
    if (diff < 1440) return `${Math.floor(diff / 60)} hrs`;
    return `${Math.floor(diff / 1440)} days`;
}

// Function to add an event to the dropdown
function addEvent(event) {
    return `
    <div class="ajax-event-notification">
        <div class="dropdown-divider"></div>
        <a href="${event.link}" class="dropdown-item">
            <p>${event.title}</p>
            <p class="text-xs">(${event.description})</p>
            <span class="float-right text-muted text-sm">${timeAgo(event.created_at)}</span>
            <br>
        </a>
    </div>
    `;
}