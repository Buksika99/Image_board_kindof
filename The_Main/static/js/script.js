document.addEventListener('DOMContentLoaded', function () {
    const lightboxTriggers = document.querySelectorAll('.lightbox-trigger');
    const lightbox = document.querySelector('.lightbox');
    const lightboxContent = document.querySelector('.lightbox-content');
    const lightboxOverlay = document.querySelector('.lightbox-overlay');
    const closeBtn = document.querySelector('.close');

    let zoomed = false;

    function closeLightbox() {
        lightbox.classList.remove('show');
        lightboxOverlay.classList.remove('show');
        lightboxContent.style.transform = 'scale(1)';
        zoomed = false;
    }

    function toggleZoom(event) {
        if (zoomed) {
            lightboxContent.style.transform = 'scale(1)';
            zoomed = false;
        } else {
            const rect = lightboxContent.getBoundingClientRect();
            const offsetX = event.clientX - rect.left;
            const offsetY = event.clientY - rect.top;
            const scale = 3; // You can adjust the zoom level as needed
            lightboxContent.style.transformOrigin = `${offsetX}px ${offsetY}px`;
            lightboxContent.style.transform = `scale(${scale})`;
            zoomed = true;
        }
    }

    lightboxTriggers.forEach(trigger => {
        trigger.addEventListener('click', function () {
            const imgSrc = this.getAttribute('src');
            lightboxContent.setAttribute('src', imgSrc);
            lightbox.classList.add('show');
            lightboxOverlay.classList.add('show');
            zoomed = false; // Reset zoom state when opening lightbox
        });
    });

    closeBtn.addEventListener('click', closeLightbox);

    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape') {
            closeLightbox();
        }
    });

    lightbox.addEventListener('click', function (event) {
        if (!event.target.closest('.lightbox-content')) {
            closeLightbox();
        }
    });

    lightboxContent.addEventListener('click', toggleZoom);

    function isAtBottomOfSecludedBox() {
    const secludedBox = document.querySelector('.secluded-box');
    if (!secludedBox) return false; // Return false if the secluded box is not found
    return secludedBox.scrollTop + secludedBox.clientHeight >= secludedBox.scrollHeight;
}

    // Function to handle scrolling event for the secluded box
    function handleSecludedBoxScroll() {
        if (isAtBottomOfSecludedBox()) {
            console.log("You have reached the bottom of the secluded box!");
        }
    }

    // Add event listener for scroll event on the secluded box
    const secludedBox = document.querySelector('.secluded-box');
    if (secludedBox) {
        secludedBox.addEventListener('scroll', handleSecludedBoxScroll);
    } else {
        console.error("Secluded box not found!");
}
});

