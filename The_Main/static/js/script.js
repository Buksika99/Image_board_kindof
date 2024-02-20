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

let currentPage = 2; // Initialize the current page number
let debounceTimeout;

async function handleSecludedBoxScroll() {
    if (isAtBottomOfSecludedBox()) {
        console.log("You have reached the bottom of the secluded box!");

        // Increment the current page number
        currentPage++;

        // Fetch new images for the updated page number
        const images = await fetchImages(currentPage);

        // Append the new images to the secluded box
        appendImages(images);
    }
}

function debounce(func, delay) {
    clearTimeout(debounceTimeout);
    debounceTimeout = setTimeout(func, delay);
}

async function fetchImages(page) {
    let character = "Keqing"; // Default character
    const url = window.location.href;

    // Extract character name from URL
    const matches = url.match(/\/named_characters\/([^\/]+)/);
    if (matches && matches[1]) {
        character = matches[1];
    }

    const response = await fetch(`https://danbooru.donmai.us/posts.json/?tags=${character}+rating%3As+-nude&page=${page}&limit=5`);
    if (response.ok) {
        const data = await response.json();
        console.log(data); // Log the data to inspect it
        return data.map(image => {
            if (image.file_url) { // Check if file_url exists
                return {
                    url: `/proxy-image/${encodeURIComponent(image.file_url)}`
                };
            } else {
                // You can choose to skip this image or handle it differently
                // Here, we are returning null for images without file_url
                return null;
            }
        }).filter(image => image !== null); // Filter out null entries
    } else {
        console.error("Failed to fetch images:", response.statusText);
        return [];
    }
}


// Function to append images to the secluded box
function appendImages(images) {
    const imageContainer = document.querySelector('.image-inside_secluded_box');
    if (imageContainer) {
        images.forEach(image => {
            // Create an image element and append it to the image container
            const imgElement = document.createElement('img');
            imgElement.src = image.url; // Assuming your image object has a 'url' property
            imgElement.alt = "Image"
            imgElement.classList.add('lightbox-trigger'); // Adding the class 'lightbox-trigger'
            imageContainer.appendChild(imgElement);

            // Attach event listener to the newly created image element
            imgElement.addEventListener('click', function() {
                const imgSrc = this.getAttribute('src');
                lightboxContent.setAttribute('src', imgSrc);
                lightbox.classList.add('show');
                lightboxOverlay.classList.add('show');
                zoomed = false; // Reset zoom state when opening lightbox
            });
        });
    }
}

// Add event listener for scroll event on the secluded box
const secludedBox = document.querySelector('.secluded-box');
if (secludedBox) {
    secludedBox.addEventListener('scroll', function() {
        debounce(handleSecludedBoxScroll, 200); // Adjust delay as needed
    });
} else {
    console.error("Secluded box not found!");
}
});

