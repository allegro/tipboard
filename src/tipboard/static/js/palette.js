function initGlobalColor() {
    Chart.defaults.global.defaultFontColor = "rgba(255, 255, 255, 0.83)";
}

/**
 * Choose mode: Blind / Material / Tipboard / FromXml
 * @param Palette
 */
function chooseMode(Palette) {
    Palette["color"] = {
        "colorPrimary": "#313131",
        "colorPrimaryDark": "#212121",
        "colorAccent": "#414141",
        "colorFontPrimary": "#FFFFFF",
        "colorFontSecondary": "#b4b4b4",
        "colorChart1": "#303F9F",
        "colorChart2": "#8BC34A",
        "colorChart3": "#0288D1",
        "colorChart4": "#E040FB",
        "colorChart5": "#FF5722",
    };
    Palette["tabColor"] = ["#303F9F", "#8BC34A", "#0288D1", "#E040FB", "#FF5722"];
}

function getGenericColor(Palette) {
    Palette["generic"] = {
        "black": "#000000",
        "white": "#FFFFFF",
        "tile_background": "#15282d",
        "red": "#d50000",
        "yellow": "#ffea00",
        "green": "#00c853",
        "blue": "#0091ea",
        "violet": "#aa00ff",
        "orange": "#ff6d00",
        "naval": "#00bfa5",
    };
}

/**
 * Add fading class to the tile
 * @param node
 * @param color
 * @param fading
 */
initFading = function (node, color, fading) {
    if (typeof color === "undefined" && typeof fading === "undefined") {
        node.style.backgroundColor = "rgba(0, 0, 0, 0)";
        node.classList.remove("fading-background-color");
    } else {
        if (typeof color === "undefined") {
            color = node.style.backgroundColor;
        }
        node.style.backgroundColor = color;
        if (fading === true) {
            node.classList.add("fading-background-color");
        }
        if (fading === false) {
            node.classList.remove("fading-background-color");
        }
    }
};

/**
 * Get generic Color || get Custom color from parser
 * ChartJS generic color
 * @param Tipboard
 */
function initPalette(Tipboard) {
    initGlobalColor();
    Tipboard.Palette = {};
    getGenericColor(Tipboard.Palette);
    chooseMode(Tipboard.Palette);
        Tipboard.Palette.applyFading = initFading;
}

/**
 ** Tu as ajouté la le fading et construit la base de la palette
 ** la big_value marche, mais pas les autres
 **
**/
