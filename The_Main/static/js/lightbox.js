document.addEventListener('DOMContentLoaded', function () {
    // Constants
    const lightboxTriggers = document.querySelectorAll('.lightbox-trigger');
    const lightbox = document.querySelector('.lightbox');
    const lightboxContent = document.querySelector('.lightbox-content');
    const lightboxOverlay = document.querySelector('.lightbox-overlay');
    const closeBtn = document.querySelector('.close');
    let zoomed = false;
    let currentPage = 2;

    // Event listeners setup
    setupEventListeners();

    // Functions
    function setupEventListeners() {
        lightboxTriggers.forEach(trigger => {
            trigger.addEventListener('click', openLightbox);
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

        const secludedBox = document.querySelector('.secluded-box');
        if (secludedBox) {
            secludedBox.addEventListener('scroll', handleSecludedBoxScroll);
        } else {
            console.error("Secluded box not found!");
        }


    function openLightbox() {
        // Add class to body to disable scrolling
        document.body.classList.add('no-scroll');
        lightboxContent.setAttribute('src', this.getAttribute('src'));
        lightbox.classList.add('show');
        lightboxOverlay.classList.add('show');
        resetZoom();
    }

    function closeLightbox() {
        // Remove class from body to enable scrolling
        document.body.classList.remove('no-scroll');
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

    async function handleSecludedBoxScroll() {
        if (isAtBottomOfSecludedBox()) {
            console.log("You have reached the bottom of the secluded box!");
            currentPage++;
            const images = await fetchImages(currentPage);
            appendImages(images);
        }
    }

    function isAtBottomOfSecludedBox() {
        const secludedBox = document.querySelector('.secluded-box');
        return secludedBox && (secludedBox.scrollTop + secludedBox.clientHeight >= secludedBox.scrollHeight);
    }

    async function fetchImages(page) {
        let character = secludedCharacter; // Use the value obtained from HTML
        let ratingToggle = $("#current-rating").text(); // Get the current rating from the button
        let rating = "";
        const matches = window.location.href.match(/\/named_characters\/([^\/]+)/);
        if (matches && matches[1]) {
            character = matches[1];
        }

        if (ratingToggle === "disable_rating") {
            rating = "+nude";
        } else if (ratingToggle === "safe") {
            rating = "+rating%3As+-nude";
        }

        const response = await fetch(`https://danbooru.donmai.us/posts.json/?tags=${character}${rating}&page=${page}&limit=5`);
        console.log(`https://danbooru.donmai.us/posts.json/?tags=${character}${rating}&page=${page}&limit=5\``)
        console.log(rating)
        if (response.ok) {
            const data = await response.json();
            return data.map(image => image.file_url ? { url: `/proxy-image/${encodeURIComponent(image.file_url)}` } : null)
                       .filter(image => image !== null && !image.url.endsWith('.mp4'));
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
                imgElement.addEventListener('click', openLightbox);
            });
        }
    }}
});