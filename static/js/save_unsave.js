const save_unsave = document.getElementById('save-unsave');
save_unsave.addEventListener('click', function(event) {
    fetch(`/product/book/${book_id}/saveunsave`, {
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
                    if ("save" in data) {
                        this.innerHTML = ' <i class="bi bi-bookmark-x font-17 btn-hover"></i> لغو ذخیره ';
                        btn_response.classList.add("d-none");
                    } else {
                        this.innerHTML = ' <i class="bi bi-bookmark font-17 btn-hover"></i> ذخیره ';
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
