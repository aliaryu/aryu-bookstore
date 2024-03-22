const csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
function previewImage(event) {                        
    const input = event.target;
    const reader = new FileReader();

    reader.onload = function(){
        const imgElement = document.getElementById('selected-image');
        // imgElement.src = reader.result;

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
                // Image uploaded successfully
                imgElement.src = reader.result;
                console.log('Image uploaded successfully');
            } else {
                // Image upload failed
                console.error('Image upload failed');
            }
        })
        .catch(error => {
            console.error('Error uploading image:', error);
        });
    }

    reader.readAsDataURL(input.files[0]);
}
