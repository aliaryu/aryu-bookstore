document.querySelectorAll('.scrollbar').forEach(function(element) {
    element.addEventListener('wheel', function(event) {
        let scrollAmount = 7;
        let scrollDirection = event.deltaY > 0 ? -1 : 1;
        let startTime = null;

        function animateScroll(timestamp) {
            if (!startTime) startTime = timestamp;
            let deltaTime = timestamp - startTime;
            let progress = Math.min(deltaTime / 100, 1);
            element.scrollLeft += scrollDirection * scrollAmount * progress;

            if (progress < 1) {
                requestAnimationFrame(animateScroll);
            }
        }

        requestAnimationFrame(animateScroll);
        event.preventDefault();
    });
});
