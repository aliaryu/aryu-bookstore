const book_id = document.getElementById('book-id').value;
const csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
const btn_response = document.getElementById('btn-response');
const like_unlike = document.getElementById('like-unlike');
like_unlike.addEventListener('click', function(event) {
    fetch(`/product/book/${book_id}/likeunlike`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        },
        body: JSON.stringify({})
    })
    .then(response => {
        if (response.status === 200) {
            response.json().then(data => {
                    if ("like" in data) {
                        this.innerHTML = ' <i class="bi bi-arrow-through-heart font-17 btn-hover"></i> لغو پسندیدن ';
                        btn_response.classList.add("d-none");
                    } else {
                        this.innerHTML = ' <i class="bi bi-suit-heart font-17 btn-hover"></i> پسندیدن ';
                        btn_response.classList.add("d-none");
                    }
                })
                .catch(error => {
                    btn_response.innerHTML = '<span class="text-danger">خطا، لطفاً بعداً امتحان کنید.</span>';
                    btn_response.classList.remove("d-none");
                });
        } else if (response.status === 403) {
            btn_response.innerHTML = '<span class="text-danger">باید به حساب کاربری خود وارد شوید.</span>';
            btn_response.classList.remove("d-none");
        } else {
            btn_response.innerHTML = '<span class="text-danger">خطا، لطفاً بعداً امتحان کنید.</span>';
            btn_response.classList.remove("d-none");
        }

    })
    .catch(error => {
        btn_response.innerHTML = '<span class="text-danger">خطا: آیا به اینترنت متصل هستید؟</span>';
        btn_response.classList.remove("d-none");
    });
});
