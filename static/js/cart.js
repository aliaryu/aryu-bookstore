function full_delete_item(book_id, event) {
    delete_item(book_id);
    event.target.parentNode.remove()
}