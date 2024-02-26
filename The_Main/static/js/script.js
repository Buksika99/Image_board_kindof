document.addEventListener('DOMContentLoaded', function () {
    // Constants
    const lightboxTriggers = document.querySelectorAll('.lightbox-trigger');
    const lightbox = document.querySelector('.lightbox');
    const lightboxContent = document.querySelector('.lightbox-content');
    const lightboxOverlay = document.querySelector('.lightbox-overlay');
    const closeBtn = document.querySelector('.close');
    let zoomed = false;
    let currentPage = 2;
    let debounceTimeout;

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

        // Toggle rating button click event
        $("#toggle-rating-btn").click(function() {
            var currentRating = $("#current-rating").text();
            var newRating = currentRating === "safe" ? "disable_rating" : "safe";

            // Obtain CSRF token
            var csrftoken = $("[name=csrfmiddlewaretoken]").val();

            // Assuming you want to send a POST request to a specific endpoint
            $.ajax({
                type: "POST",
                data: {
                    rating: newRating,
                    csrfmiddlewaretoken: csrftoken  // Include CSRF token in data
                },
                success: function(response) {
                    console.log("Rating successfully toggled to: " + newRating);
                    $("#current-rating").text(newRating);
                    // Store the new rating state in localStorage
                    localStorage.setItem("rating", newRating);
                },
                error: function(xhr, textStatus, errorThrown) {
                    console.error("Failed to toggle rating");
                }
            });
        });
    }

    function openLightbox() {
        lightboxContent.setAttribute('src', this.getAttribute('src'));
        lightbox.classList.add('show');
        lightboxOverlay.classList.add('show');
        resetZoom();
    }

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

    function debounce(func, delay) {
        clearTimeout(debounceTimeout);
        debounceTimeout = setTimeout(func, delay);
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
                imgElement.addEventListener('click', openLightbox);
            });
        }
    }

    // Retrieve rating state from localStorage, if available
    var currentRating = localStorage.getItem("rating");
    if (currentRating) {
        $("#current-rating").text(currentRating);
    }
});
