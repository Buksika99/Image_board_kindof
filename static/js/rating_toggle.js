document.addEventListener('DOMContentLoaded', function () {
    // Constants
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


    // Retrieve rating state from localStorage, if available
    var currentRating = localStorage.getItem("rating");
    if (currentRating) {
        $("#current-rating").text(currentRating);
    }
});
