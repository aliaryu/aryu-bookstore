const password_form = document.getElementById('password-form');
const password_success = document.getElementById('password-success');
const password_error = document.getElementById('password-error');
password_form.addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    fetch('/user/userchangepass/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrf_token
        }
    })
    .then(response => {
        if (response.ok) {
            window.location.href = "/user/login/?changepass=true"
        } else {
            response.json().then(data => {
                console.log(data)
                password_error.innerHTML = '<span class="text-danger">خطا(ها):</span>';
                const ul = document.createElement('ul');
                ul.classList.add("mb-0")

                for (const key in data) {
                    if (key === "old_password") {
                        for (let index = 0; index < data[key].length; index++) {
                            const error = data[key][index];
                            const li = document.createElement('li');
                            li.textContent = `رمز فعلی: ${error}`;
                            li.classList.add('text-danger');
                            ul.appendChild(li);
                        }
                    } else if (key === "new_password1") {
                        for (let index = 0; index < data[key].length; index++) {
                            const error = data[key][index];
                            const li = document.createElement('li');
                            li.textContent = `رمز جدید: ${error}`;
                            li.classList.add('text-danger');
                            ul.appendChild(li);
                        }
                    } else if (key === "new_password2") {
                        for (let index = 0; index < data[key].length; index++) {
                            const error = data[key][index];
                            const li = document.createElement('li');
                            li.textContent = `تکرار رمز جدید: ${error}`;
                            li.classList.add('text-danger');
                            ul.appendChild(li);
                        }
                    } else if (key === "non_field_errors") {
                        for (let index = 0; index < data[key].length; index++) {
                            const error = data[key][index];
                            const li = document.createElement('li');
                            li.textContent = `${error}`;
                            li.classList.add('text-danger');
                            ul.appendChild(li);
                        }
                    }
                }
                password_error.appendChild(ul);
                password_error.classList.remove("d-none");
            })
            .catch(error => {
                password_error.innerHTML = '<span class="text-danger">خطا: خطایی در تجزیه و تحلیل پاسخ دریافتی رخ داده است. لطفاً بعداً امتحان کنید.</span>';
                password_success.classList.add("d-none");
                password_error.classList.remove("d-none");
            });
        }
    })
    .catch(error => {
        password_error.innerHTML = '<span class="text-danger">خطا: خطایی در ارسال رخ داده، آیا به اینترنت متصل هستید؟</span>';
        password_success.classList.add("d-none");
        password_error.classList.remove("d-none");
    });
});
