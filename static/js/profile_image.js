const csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
const imgElement = document.getElementById('selected-image');
const image_success = document.getElementById('image-success');
const image_error = document.getElementById('image-error');
function previewImage(event) {                        
    const input = event.target;
    const reader = new FileReader();

    reader.onload = function(){
        const formData = new FormData();
        formData.append('image', input.files[0]);
        fetch("/user/uploadimage/", {
            method: "PUT",
            headers: {
                'X-CSRFToken': csrf_token
            },
            body: formData
        })
        .then(response => {
            if (response.ok) {
                image_success.innerHTML = `<span class="text-success">عکس تغییر کرد.</span>`
                image_success.classList.remove("d-none")
                image_error.classList.add("d-none")
                imgElement.src = reader.result;
            } else {
                image_error.innerHTML = `<span class="text-danger">عکس باید مربع باشد.</span>`
                image_error.classList.remove("d-none")
                image_success.classList.add("d-none")
            }
        })
        .catch(error => {
            image_error.innerHTML = `<span class="text-danger">خطا: بعدا امتحان کنید.</span>`
            image_error.classList.remove("d-none")
            image_success.classList.add("d-none")
        });
    }
    reader.readAsDataURL(input.files[0]);
}
