const author_id = document.getElementById('author-id').value;
const csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
const comment_success = document.getElementById('comment-success');
const comment_error = document.getElementById('comment-error');
const comment_form = document.getElementById('comment-form');
comment_form.addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    fetch(`/product/author/${author_id}/comment`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrf_token
        },
        body: formData
    })
    .then(response => {
        if (response.ok) {
            this.reset();
            const form_elements = Array.from(this.elements);
            form_elements.forEach(element => {
                element.classList.add('d-none');
            });
            comment_error.classList.add("d-none");
            comment_success.classList.remove("d-none");
        } else {
            response.json().then(data => {
                comment_error.innerHTML = '<span class="text-danger">خطا(ها):</span>';
                const ul = document.createElement('ul');
                ul.classList.add("mb-0")
                for (const key in data) {
                    if (key === "message") {
                        for (let index = 0; index < data[key].length; index++) {
                            const error = data[key][index];
                            const li = document.createElement('li');
                            li.textContent = `نظر شما: ${error}`;
                            li.classList.add('text-danger');
                            ul.appendChild(li);
                        }
                    }
                }
                comment_error.appendChild(ul);
                comment_error.classList.remove("d-none");
            })
            .catch(error => {
                comment_error.innerHTML = '<span class="text-danger">خطا: خطایی در تجزیه و تحلیل پاسخ دریافتی رخ داده است. لطفاً بعداً امتحان کنید.</span>';
                comment_error.classList.remove("d-none");
            });
        }
    })
    .catch(error => {
        comment_error.innerHTML = '<span class="text-danger">خطا: خطایی در ارسال رخ داده، آیا به اینترنت متصل هستید؟</span>';
        comment_error.classList.remove("d-none");
    });
});
