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
        resetZoom();
    }

    function resetZoom() {
        lightboxContent.style.transform = 'scale(1)';
        zoomed = false;
    }

    function toggleZoom(event) {
        zoomed ? resetZoom() : setZoom(event);
    }

    function setZoom(event) {
        const rect = lightboxContent.getBoundingClientRect();
        const offsetX = event.clientX - rect.left;
        const offsetY = event.clientY - rect.top;
        const scale = 3; // Adjust zoom level as needed
        lightboxContent.style.transformOrigin = `${offsetX}px ${offsetY}px`;
        lightboxContent.style.transform = `scale(${scale})`;
        zoomed = true;
    }

    lightboxTriggers.forEach(trigger => {
        trigger.addEventListener('click', function () {
            lightboxContent.setAttribute('src', this.getAttribute('src'));
            lightbox.classList.add('show');
            lightboxOverlay.classList.add('show');
            resetZoom();
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
        return secludedBox && (secludedBox.scrollTop + secludedBox.clientHeight >= secludedBox.scrollHeight);
    }


let currentPage = 2;
let debounceTimeout;

async function handleSecludedBoxScroll() {
    if (isAtBottomOfSecludedBox()) {
        console.log("You have reached the bottom of the secluded box!");
        currentPage++;
        const images = await fetchImages(currentPage);
        appendImages(images);
    }
}

function debounce(func, delay) {
    clearTimeout(debounceTimeout);
    debounceTimeout = setTimeout(func, delay);
}

async function fetchImages(page) {
    let character = "Keqing";
    const matches = window.location.href.match(/\/named_characters\/([^\/]+)/);
    if (matches && matches[1]) {
        character = matches[1];
    }

    const response = await fetch(`https://danbooru.donmai.us/posts.json/?tags=${character}+rating%3As+-nude&page=${page}&limit=5`);
    if (response.ok) {
        const data = await response.json();
        return data.map(image => image.file_url ? { url: `/proxy-image/${encodeURIComponent(image.file_url)}` } : null)
                   .filter(image => image !== null);
    } else {
        console.error("Failed to fetch images:", response.statusText);
        return [];
    }
}

function appendImages(images) {
    const imageContainer = document.querySelector('.image-inside_secluded_box');
    if (imageContainer) {
        images.forEach(image => {
            const imgElement = document.createElement('img');
            imgElement.src = image.url;
            imgElement.alt = "Image";
            imgElement.classList.add('lightbox-trigger');
            imageContainer.appendChild(imgElement);
            imgElement.addEventListener('click', () => {
                const imgSrc = imgElement.getAttribute('src');
                lightboxContent.setAttribute('src', imgSrc);
                lightbox.classList.add('show');
                lightboxOverlay.classList.add('show');
                zoomed = false;
            });
        });
    }
}

const secludedBox = document.querySelector('.secluded-box');
if (secludedBox) {
    secludedBox.addEventListener('scroll', () => debounce(handleSecludedBoxScroll, 200));
} else {
    console.error("Secluded box not found!");
}
});