window.Tipboard = {};

function getFlipTime(node) {
    let classStr = $(node).attr("class");
    // TODO: make this flip time CUSTOM
    let flipTime = 10000;
    return flipTime;
}

/**
 * Init flip behavior for every tiles
 */
function initTiles() {
    let flipContainers = $("div[id*=\"flip-time-\"]");
    $.each(flipContainers, function (idx, flippingContainer) {
        Tipboard.Dashboard.autoAddFlipClasses(flippingContainer);
        let flipInterval = getFlipTime(flippingContainer);
        let flipIntervalId = setInterval(function () {
            let nextFlipIdx;
            let containerFlips = $(flippingContainer).find(".flippable");
            $(containerFlips).each(function (index, tile) {
                if ($(tile).hasClass("flippedforward")) {
                    nextFlipIdx = (index + 1) % containerFlips.length;
                    $(tile).removeClass("flippedforward");
                    return false; // break
                }
            });
            if (typeof (nextFlipIdx) !== "undefined") {
                let tileToFlip = containerFlips[parseInt(nextFlipIdx, 10)];
                $(tileToFlip).addClass("flippedforward");
            }
        }, flipInterval);
        Tipboard.Dashboard.flipIds.push(flipIntervalId);
    });
}

/**
 * Extract tile depending the type of the data
 * @param data
 * @returns {*}
 */
const getTitleForChartJSTitle = function (data) {
    let title = {
        display: false,
        text: "",
    };
    if (data !== null) {
        title.display = true;
        title.color = ("color" in data) ? data.color : "#FFFFFF";
        title.text = data.title.text;
    }
    return title
};

function startClientConnection() {
    initTiles();
    initWebsocketManager(Tipboard);
}

/**
 * Main function of tipboard.js
 * Define the $(document).ready(function()
 */
(function ($) {
    Tipboard.Dashboard = {
        flipIds: [],
        updateFunctions: {},
        chartsIds: {},
    };
    Tipboard.chartJsTile = {};
    initDashboard(Tipboard);
    initPalette(Tipboard);
    setTimeout(startClientConnection, 420); // to let server start
    console.log("Tipboard starting");
}($));
