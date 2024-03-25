const add_to_cart = document.getElementById("addtocart");
add_to_cart.addEventListener("click", function(event) {
    add_increase_item(book_id);
    this.innerHTML = ' <i class="bi bi-bag-check font-17 btn-hover"></i> افزوده شد';
    this.disabled = true;
    this.classList.add("opacity-100")
});
