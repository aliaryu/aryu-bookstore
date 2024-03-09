function previewImage(event) {                        
    const input = event.target;
    const reader = new FileReader();

    reader.onload = function(){
      const imgElement = document.getElementById('selected-image');
      imgElement.src = reader.result;
    }

    reader.readAsDataURL(input.files[0]);
}