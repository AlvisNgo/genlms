function markAsSeen(contentId) {
    fetch("/analytics/content_seen/" + contentId)
    .then(response => response.json())
    .then(data => {
        
    });
}

function markAsSeen_announce(announceId) {
    fetch("/analytics/announcement_seen/" + announceId)
    .then(response => response.json())
    .then(data => {
        
    });
}