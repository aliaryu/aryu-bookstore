function delete_address(event) {
    event.preventDefault();
    var url = event.target.parentNode.getAttribute('href');
    console.log(url)
    fetch(url, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        }
    })
    .then(response => {
        if (response.ok) {
            event.target.parentNode.parentNode.parentNode.remove();
        }
    })
}
