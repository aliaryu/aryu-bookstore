function delete_address(event) {
    event.preventDefault();
    var url = event.target.parentNode.getAttribute('href');
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


const address_form = document.getElementById('address-form');
const address_success = document.getElementById('address-success');
const address_error = document.getElementById('address-error');
address_form.addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    fetch('/user/useraddress/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrf_token
        }
    })
    .then(response => {
        if (response.ok) {
            this.reset();
            address_error.classList.add("d-none");
            address_success.classList.remove("d-none");
        } else {
            response.json().then(data => {
                address_error.innerHTML = '<span class="text-danger">خطا(ها):</span>';
                const ul = document.createElement('ul');
                ul.classList.add("mb-0")

                for (const key in data) {
                    if (key === "province") {
                        for (let index = 0; index < data[key].length; index++) {
                            const error = data[key][index];
                            const li = document.createElement('li');
                            li.textContent = `استان: ${error}`;
                            li.classList.add('text-danger');
                            ul.appendChild(li);
                        }
                    } else if (key === "postal_code") {
                        for (let index = 0; index < data[key].length; index++) {
                            const error = data[key][index];
                            const li = document.createElement('li');
                            li.textContent = `کد پستی: ${error}`;
                            li.classList.add('text-danger');
                            ul.appendChild(li);
                        }
                    } else if (key === "address_path") {
                        for (let index = 0; index < data[key].length; index++) {
                            const error = data[key][index];
                            const li = document.createElement('li');
                            li.textContent = `آدرس: ${error}`;
                            li.classList.add('text-danger');
                            ul.appendChild(li);
                        }
                    } else if (key === "user") {
                        for (let index = 0; index < data[key].length; index++) {
                            const error = data[key][index];
                            const li = document.createElement('li');
                            li.textContent = `یوز: ${error}`;
                            li.classList.add('text-danger');
                            ul.appendChild(li);
                        }
                    }
                }
                address_error.appendChild(ul);
                address_error.classList.remove("d-none");
            })
            .catch(error => {
                address_error.innerHTML = '<span class="text-danger">خطا: خطایی در تجزیه و تحلیل پاسخ دریافتی رخ داده است. لطفاً بعداً امتحان کنید.</span>';
                address_error.classList.remove("d-none");
            });
        }
    })
    .catch(error => {
        address_error.innerHTML = '<span class="text-danger">خطا: خطایی در ارسال رخ داده، آیا به اینترنت متصل هستید؟</span>';
        address_error.classList.remove("d-none");
    });
});
