document.addEventListener("DOMContentLoaded", function() {
    var categoryBoxes = document.querySelectorAll(".category_box");

    categoryBoxes.forEach(function(categoryBox) {
        var img = categoryBox.querySelector("img");
        var canvas = document.createElement('canvas');
        var ctx = canvas.getContext('2d');

        img.onload = function() {
            canvas.width = img.width;
            canvas.height = img.height;
            ctx.drawImage(img, 0, 0, img.width, img.height);
            var imageData = ctx.getImageData(0, 0, img.width, img.height);
            var data = imageData.data;

            var r = 0, g = 0, b = 0, count = 0;
            for (var i = 0; i < data.length; i += 4) {
                var brightness = (data[i] + data[i + 1] + data[i + 2]) / 3;
                var saturation = 1 - Math.min(data[i], data[i + 1], data[i + 2]) / brightness;
                if (brightness > 100 && saturation > 0.2) { // Adjust the thresholds as needed
                    r += data[i];
                    g += data[i + 1];
                    b += data[i + 2];
                    count++;
                }
            }

            r = Math.floor(r / count);
            g = Math.floor(g / count);
            b = Math.floor(b / count);

            var dominantColor = rgbToHex(r, g, b);

            categoryBox.style.backgroundColor = dominantColor;
        };
    });
});

function rgbToHex(r, g, b) {
    return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
}

function componentToHex(c) {
    var hex = c.toString(16);
    return hex.length == 1 ? "0" + hex : hex;
}
