// Global variables for reference
var tileCount = 6;
var colors;
var correctColor;

// Get the required selectors
var tiles = document.querySelectorAll(".tile");
var colorDisplay = document.querySelector("#colorDisplay");
var result = document.querySelector("#result");
var resetButton = document.querySelector("#reset");
var easyButton = document.querySelector("#easy");
var hardButton = document.querySelector("#hard");

// Initializes the click events for all the tiles
function initTilesListener() {
    for(var i = 0; i < tiles.length; i++) {
        tiles[i].addEventListener("click", function() {
            var selectedColor = this.style.backgroundColor;

            if (selectedColor === correctColor) {
                assignOneColor(correctColor);
                result.innerHTML = "<i class=\"far fa-grin-hearts\"></i><i class=\"far fa-grin-hearts\"></i><i class=\"far fa-grin-hearts\"></i>";
                resetButton.textContent = "Play Again?";

            } else {
                this.style.backgroundColor = "#e9d9d9";
                result.innerHTML = "<i class=\"far fa-grimace\"></i><i class=\"far fa-grimace\"></i><i class=\"far fa-grimace\"></i>";
            }
        });
    }
}

// Initializes the click events for all buttons
function initButtonListener() {
    resetButton.addEventListener("click", reset);

    easyButton.addEventListener("click", function() {
        tileCount = 3;
        toggleTiles();
        easyButton.classList.add("selected");
        hardButton.classList.remove("selected");
        reset();
    });

    hardButton.addEventListener("click", function() {
        tileCount = 6;
        toggleTiles();
        hardButton.classList.add("selected");
        easyButton.classList.remove("selected");
        reset();
    });
}

// Returns a random color
function generateColor() {
    var r = Math.floor(Math.random() * 256);
    var g = Math.floor(Math.random() * 256);
    var b = Math.floor(Math.random() * 256);

    return "rgb(" + r + ", " + g + ", " + b + ")";
}

// Assigns `color` to all tiles
function assignOneColor(color) {
    for(var i = 0; i < tileCount; i++) {
        tiles[i].style.backgroundColor = color;
    }
}

// Assigns colors to tiles according to `tileCount` and also picks out one of them for `correctColor`
function assignColors() {
    colors = [];
    var correctIndex;

    correctIndex = Math.floor(Math.random() * tileCount);
    for (var i = 0; i < tileCount; i++) {
        var color = generateColor()
        colors.push(color);
    }
    correctColor = colors[correctIndex];
    colorDisplay.textContent = correctColor;

    for (var j = 0; j < tileCount; j++) {
        tiles[j].style.backgroundColor = colors[j];
    }
}

// Toggles the last 3 tiles according to `tileCount`
function toggleTiles() {
    for(var i = 3; i < tiles.length; i++) {
        if (tileCount === 3) {
            tiles[i].style.display = "none";
        } else if (tileCount === 6) {
            tiles[i].style.display = "block";
        }
    }
}

// Called when `Play Again` or `New Colors` button is clicked
// Resets the game according to current difficulty
function reset() {
    result.textContent = "";
    resetButton.textContent = "New Colors";
    assignColors();
}

// An init function that is called at the start of the script
function init() {
    assignColors();
    initTilesListener();
    initButtonListener();
}

// Run script
init();
