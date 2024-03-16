signup_error = document.getElementById('signup-error');
signup_form = document.getElementById("signup-form");
signup_form.addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    fetch('/user/usersignup/', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            window.location.href = "/user/login/?signup=true"
        } else {
            response.json().then(data => {
                signup_error.innerHTML = '';
                signup_error.innerHTML = '<span class="text-danger">خطا(ها):</span>';
                const ul = document.createElement('ul');
                ul.classList.add("mb-0")

                for (const key in data) {
                    if (key === "first_name") {
                        for (let index = 0; index < data[key].length; index++) {
                            const error = data[key][index];
                            const li = document.createElement('li');
                            li.textContent = `نام: ${error}`;
                            li.classList.add('text-danger');
                            ul.appendChild(li);
                        }
                    } else if (key === "last_name") {
                        for (let index = 0; index < data[key].length; index++) {
                            const error = data[key][index];
                            const li = document.createElement('li');
                            li.textContent = `نام خانوادگی: ${error}`;
                            li.classList.add('text-danger');
                            ul.appendChild(li);
                        }
                    } else if (key === "username") {
                        for (let index = 0; index < data[key].length; index++) {
                            const error = data[key][index];
                            const li = document.createElement('li');
                            li.textContent = `نام کاربری: ${error}`;
                            li.classList.add('text-danger');
                            ul.appendChild(li);
                        }
                    } else if (key === "password") {
                        for (let index = 0; index < data[key].length; index++) {
                            const error = data[key][index];
                            const li = document.createElement('li');
                            li.textContent = `رمز عبور: ${error}`;
                            li.classList.add('text-danger');
                            ul.appendChild(li);
                        }
                    } else if (key === "password_confirm") {
                        for (let index = 0; index < data[key].length; index++) {
                            const error = data[key][index];
                            const li = document.createElement('li');
                            li.textContent = `تکرار رمز: ${error}`;
                            li.classList.add('text-danger');
                            ul.appendChild(li);
                        }
                    } else if (key === "email") {
                        for (let index = 0; index < data[key].length; index++) {
                            const error = data[key][index];
                            const li = document.createElement('li');
                            li.textContent = `ایمیل: ${error}`;
                            li.classList.add('text-danger');
                            ul.appendChild(li);
                        }
                    } else {
                        signup_error.innerHTML = `<span class="text-danger">خطا: ${data[key]}</span>`;
                    }

                }
                signup_error.appendChild(ul);
                signup_error.classList.remove("d-none");
            })
            .catch(error => {
                signup_error.innerHTML = '<span class="text-danger">خطا: خطایی در تجزیه و تحلیل پاسخ دریافتی رخ داده است. لطفاً بعداً امتحان کنید.</span>';
                signup_error.classList.remove("d-none");
            });
        }
    })
    .catch(error => {
        signup_error.innerHTML = '<span class="text-danger">خطا: خطایی در ارسال رخ داده، آیا به اینترنت متصل هستید؟</span>';
        signup_error.classList.remove("d-none");
    });
});
