$("#menu-notification").click(() => {
    $(".ajax-event-notification").remove();
    $("#menu-notification-header").text("Loading unread events ...");

    $.ajax({
        url: '/api/get_notification', // Replace with your API endpoint
        method: 'GET',
        success: function(response) {
            if (response.success) {
                $("#menu-notification-number").text(0); // set to zero, since events are already read
                
                if (response.unread_events.length > 0) {
                    $("#menu-notification-header").text(response.unread_events.length + " New Notifications");
                }
                else {
                    $("#menu-notification-header").text("No New Notification")
                }
                
                response.unread_events.forEach(event => {
                    $("#menu-notification-box .dropdown-divider").last().before(addEvent(event, true));
                });

                response.read_events.forEach(event => {
                    $("#menu-notification-box .dropdown-divider").last().before(addEvent(event, false));
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
function addEvent(event, new_event) {
    return `
    <div class="ajax-event-notification">
        <div class="dropdown-divider"></div>
        <a href="${event.link}" class="dropdown-item">
            <p>${new_event ? "*" : ""} ${event.title}</p>
            <p class="text-xs">(${event.description})</p>
            <span class="float-right text-muted text-sm">${timeAgo(event.created_at)}</span>
            <br>
        </a>
    </div>
    `;
}