function markAsSeen(contentId) {
    fetch("/analytics/content_seen/" + contentId)
    .then(response => response.json())
    .then(data => {
        
    });
}