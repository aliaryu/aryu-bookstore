const user_id = document.getElementById('user-id').value;
const userinfo_error = document.getElementById('userinfo-error');
const userinfo_success = document.getElementById('userinfo-success');
const userinfo_form = document.getElementById("userinfo-form");
userinfo_form.addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    fetch(`/user/userinfo/${user_id}/`, {
        method: 'PUT',
        headers: {
            'X-CSRFToken': csrf_token
        },
        body: formData
    })
    .then(response => {
        if (response.ok) {
            userinfo_error.classList.add("d-none");
            userinfo_success.classList.remove("d-none");
        } else {
            response.json().then(data => {
                userinfo_error.innerHTML = '<span class="text-danger">خطا(ها):</span>';
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
                    } else if (key === "birth_date") {
                        for (let index = 0; index < data[key].length; index++) {
                            const error = data[key][index];
                            const li = document.createElement('li');
                            li.textContent = `تاریخ تولد: ${error}`;
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
                    } else if (key === "email") {
                        for (let index = 0; index < data[key].length; index++) {
                            const error = data[key][index];
                            const li = document.createElement('li');
                            li.textContent = `ایمیل: ${error}`;
                            li.classList.add('text-danger');
                            ul.appendChild(li);
                        }
                    }
                }
                userinfo_error.appendChild(ul);
                userinfo_error.classList.remove("d-none");
            })
            .catch(error => {
                userinfo_error.innerHTML = '<span class="text-danger">خطا: خطایی در تجزیه و تحلیل پاسخ دریافتی رخ داده است. لطفاً بعداً امتحان کنید.</span>';
                userinfo_error.classList.remove("d-none");
            });
        }
    })
    .catch(error => {
        userinfo_error.innerHTML = '<span class="text-danger">خطا: خطایی در ارسال رخ داده، آیا به اینترنت متصل هستید؟</span>';
        userinfo_error.classList.remove("d-none");
    });
});
