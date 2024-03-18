const userpass_error = document.getElementById('userpass-error');
const userpass_form = document.getElementById("userpass-form");
userpass_form.addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    fetch('/user/userpass/', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            window.location.href = this.querySelector('input[name="next"]').value
        } else {
            response.json().then(data => {
                console.log(data)
                userpass_error.innerHTML = '<span class="text-danger">خطا(ها):</span>';
                const ul = document.createElement('ul');
                ul.classList.add("mb-0");
                for (const key in data) {
                    if (key === "username") {
                        for (let index = 0; index < data[key].length; index++) {
                            const error = data[key][index];
                            const li = document.createElement('li');
                            li.textContent = `نام کاربری : ${error}`;
                            li.classList.add('text-danger');
                            ul.appendChild(li);
                        }
                    } else if (key === "password") {
                        for (let index = 0; index < data[key].length; index++) {
                            const error = data[key][index];
                            const li = document.createElement('li');
                            li.textContent = `رمز عبور : ${error}`;
                            li.classList.add('text-danger');
                            ul.appendChild(li);
                        }
                    } else {
                        userpass_error.innerHTML = `<span class="text-danger">خطا: ${data[key]}</span>`;
                    }
                }
                userpass_error.appendChild(ul);
                userpass_error.classList.remove("d-none");
            })
            .catch(error => {
                userpass_error.innerHTML = '<span class="text-danger">خطا: خطایی در تجزیه و تحلیل پاسخ دریافتی رخ داده است. لطفاً بعداً امتحان کنید.</span>';
                userpass_error.classList.remove("d-none");
            });
        }
    })
    .catch(error => {
        userpass_error.innerHTML = '<span class="text-danger">خطا: خطایی در ارسال رخ داده، آیا به اینترنت متصل هستید؟</span>';
        userpass_error.classList.remove("d-none");
    });
});