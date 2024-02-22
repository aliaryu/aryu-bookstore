window.onload = function() {
    setCarouselHeight();
}

window.onresize = function() {
    setCarouselHeight();
}

function setCarouselHeight() {
    var carouselItems = document.getElementsByClassName('carousel-item');
    var maxHeight = 0;
    var currentIndex = null;
    for (var i = 0; i < carouselItems.length; i++) {
        if (carouselItems[i].classList.contains('active')) {
            currentIndex = i;
            carouselItems[i].classList.remove('active');
        } else {
            carouselItems[i].classList.add('active');
        }
        var height = carouselItems[i].clientHeight;
        console.log(height)
        if (height > maxHeight) {
            maxHeight = height;
        }
        carouselItems[i].classList.remove('active');
    }
    document.getElementsByClassName('carousel-inner')[0].style.height = maxHeight + 'px';
    carouselItems[currentIndex].classList.add('active');
}
