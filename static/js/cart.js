book_items = document.getElementsByClassName("book-item");
count_items = document.getElementById("count-items");
price_items = document.getElementById("price-items");

function cart_info() {
    var default_count_items = 0;
    var default_price_items = 0;
    Array.from(book_items).forEach(item => {
        var price_item = item.getAttribute("price");
        var count_item = item.getAttribute("count");
        default_count_items += parseInt(count_item);
        default_price_items += parseFloat(price_item) * parseInt(count_item);
    });
    count_items.textContent = default_count_items;
    price_items.textContent = default_price_items.toLocaleString('us-EN') + " تومان";
}

document.addEventListener("DOMContentLoaded", function() {
    cart_info();
});

function full_delete_item(book_id, event) {
    delete_item(book_id);
    event.target.parentNode.remove();
    cart_info();
}
