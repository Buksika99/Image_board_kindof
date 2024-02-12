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

    lightboxContent.addEventListener('click', toggleZoom);
});
