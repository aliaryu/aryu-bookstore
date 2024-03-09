contact_form = document.getElementById('contact-form');
contact_success = document.getElementById('contact-success');
contact_error = document.getElementById('contact-error');
contact_form.addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    fetch('/contact/', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            this.reset();
            this.classList.add("d-none");
            contact_error.classList.add("d-none");
            contact_success.classList.remove("d-none");
        } else {
            response.json().then(data => {
                contact_error.innerHTML = '';
                contact_error.innerHTML = '<span class="text-danger">خطا(ها):</span>';
                const ul = document.createElement('ul');
                ul.classList.add("mb-0")

                for (const key in data) {
                    if (key === "full_name") {
                        for (let index = 0; index < data[key].length; index++) {
                            const error = data[key][index];
                            const li = document.createElement('li');
                            li.textContent = `نام و نام خانوادگی: ${error}`;
                            li.classList.add('text-danger');
                            ul.appendChild(li);
                        }
                    } else if (key === "email") {
                        console.log(data[key])
                        for (let index = 0; index < data[key].length; index++) {
                            const error = data[key][index];
                            const li = document.createElement('li');
                            li.textContent = `ایمیل: ${error}`;
                            li.classList.add('text-danger');
                            ul.appendChild(li);
                        }
                    } else if (key === "text") {
                        for (let index = 0; index < data[key].length; index++) {
                            const error = data[key][index];
                            const li = document.createElement('li');
                            li.textContent = `متن پیام: ${error}`;
                            li.classList.add('text-danger');
                            ul.appendChild(li);
                        }
                    }
                }
                contact_error.appendChild(ul);
                contact_error.classList.remove("d-none");
            });
        }
    })
});
