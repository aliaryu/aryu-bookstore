function get_cookie() {
    var cookie_name = "cart=";
    var decoded_cookie = decodeURIComponent(document.cookie);
    var cookie_array = decoded_cookie.split(";");
    for(var i = 0; i < cookie_array.length; i++) {
        var cart = cookie_array[i].trim();
        if (cart.indexOf(cookie_name) == 0) {
            var cart_string = cart.substring(cookie_name.length, cart.length);
            return JSON.parse(cart_string);
        }
    }
    return {};
}

function set_cookie(cart_object) {
    var cart_str = JSON.stringify(cart_object);
    var expiration_date = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toUTCString();
    document.cookie = "cart=" + cart_str + ";expires=" + expiration_date + ";path=/";
}

function add_increase_item(book_id) {
    var cart = get_cookie();
    if (cart.hasOwnProperty(book_id)) {
        cart[book_id]++;
    } else {
        cart[book_id] = 1;
    }
    set_cookie(cart);
}

function delete_decrease_item(book_id) {
    var cart = get_cookie();
    if (cart.hasOwnProperty(book_id)) {
        cart[book_id]--;
        if (cart[book_id] === 0) {
            delete cart[book_id];
        }
    }
    set_cookie(cart);
}
