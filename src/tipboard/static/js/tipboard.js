/**
 * Dynamicaly add Flipforward class to tile, regardind the dashboard.yml
 * @param flippingContainer
 */
let autoAddFlipClasses = function (flippingContainer) {
    $.each($(flippingContainer).find(".tile"), function (idx, elem) {
        if (idx === 0) {
            $(elem).addClass("flippedforward");
        }
        $(elem).addClass("flippable");
    });
};

/**
 * Print a tile to indicate the type of error
 * @param err Exception Object
 * @param tile tile_template
 * @param tileId id of tile
 */
let onTileError = function (err, tile, tileId) {
    $.each([".tile-content"], function (idx, klass) {
        let nodes = $(tile).find(klass);
        $(nodes[0]).hide();
        $(nodes[1]).show();
        nodes = $(tile).find(".tile-content");
        $(nodes[1]).html(["Tile " + tileId + " configuration error:",
            err.name || "error name: n/a",
            err.message || "error message: n/a",].join("<br>"));
    });
};

/**
 * Add fading class to the tile
 * @param node
 * @param color
 * @param fading
 */
initFading = function (node, color, fading) {
    node.style.backgroundColor = color;
    if (fading === true) {
        node.classList.add("fading-background-color");
    } else {
        node.classList.remove("fading-background-color");
    }
};

function getFlipTime(node) {
    let classStr = $(node).attr("id");
    let flipTime = 10000;
    $.each(classStr.split(" "), function (idx, val) {
        let groups = /flip-time-(\d+)/.exec(val);
        if (Boolean(groups) && groups.length > 1) {
            flipTime = groups[1];
            flipTime = parseInt(flipTime, 10) * 1000;
            return false;
        }
    });
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

function initChartjsDefault() {
    Chart.defaults.global.defaultFontColor = "rgba(0, 0, 0, 0.83)";
    Chart.defaults.global.elements.line.backgroundColor = "#FFFFFF";
    Chart.defaults.scale.gridLines.display = true;
    Chart.defaults.scale.gridLines.color = "#929292";
}

/**
 * Update the html of tile regarding the key to update
 * @param tileId id of tile in redis
 * @param dataToPut data to update
 * @param keysToUse list of key in tile, to update with dataToPut
 */
let updateKeyOfTiles = function updateKeyOfTiles(tileId, dataToPut, keysToUse) {
    if (keysToUse === "all") { // keysToUse*: list of keys, or string 'all', if 'all' then all keys used from *dataToPut*
        keysToUse = [];
        for (let data in dataToPut) {
            if ({}.hasOwnProperty.call(dataToPut, data)) {
                keysToUse.push(data);
            }
        }
    }
    $.each(keysToUse, function (idx, key) {
        let value = dataToPut[key.toString()];
        if (typeof (value) !== "undefined") {
            let dst = $($("#" + tileId)[0]).find("#" + tileId + "-" + key)[0];
            if (typeof dst !== "undefined") {
                $(dst).text(value);
            }
        }
    });
};

/**
 * Update dataset data & option recursivly
 * @param chart
 * @param newDict
 */
function updateDataset(chart, newDict) {
    let rcx = 0;
    for (; rcx < newDict.datasets.length; rcx++) {
        for (let keyDataset in newDict.datasets[rcx]) {
            if ({}.hasOwnProperty.call(newDict.datasets[rcx], keyDataset)) {
                if (chart.data.datasets.length <= rcx) {
                    chart.data.datasets.push({});
                }
                keyDataset = keyDataset.toString();
                chart.data.datasets[rcx][keyDataset.toString()] = newDict.datasets[rcx][keyDataset.toString()];
            }
        }
    }
    if (chart.data.datasets.length > newDict.datasets.length) {
        chart.data.datasets.splice(rcx, chart.data.datasets.length); // delete previous dataset
    }
}

/**
 * Update all option(also called meta) inside chart object
 * @param actualOptions
 * @param newOptions
 */
function updateOptions(actualOptions, newOptions) {
    for (let key in newOptions) {
        if ({}.hasOwnProperty.call(newOptions, key)) {
            if (newOptions[key.toString()].constructor === Object && key.toString() in actualOptions) {
                updateOptions(actualOptions[key.toString()], newOptions[key.toString()]);
            } else {
                if (Array.isArray(actualOptions[key.toString()])) {
                    for (let rcx = 0; rcx < actualOptions[key.toString()].length; rcx++) {
                        updateOptions(actualOptions[key.toString()][rcx], newOptions[key.toString()][rcx]);
                    }
                } else {
                    actualOptions[key.toString()] = newOptions[key.toString()];
                }
            }
        }
    }
}

/**
 * Update all data inside chart object
 * @param chart
 * @param chartNewValue
 */
function updateData(chart, chartNewValue) {
    for (let key in chartNewValue) {
        if ({}.hasOwnProperty.call(chartNewValue, key)) {
            key = key.toString();
            if (key === "datasets") {
                updateDataset(chart, chartNewValue);
            } else if (key === "title" || key === "legend") {
                chart.options[key.toString()] = chartNewValue[key.toString()];
            } else {
                chart.data[key.toString()] = chartNewValue[key.toString()];
            }
        }
    }
}

let updateDataOfChartJS = function (chart, data, meta) {
    if ("labels" in chart.data) {
        chart.data.labels = [];
    }
    updateData(chart, data);
    if (meta !== "undefined") {
        updateOptions(chart.config.options, meta.options);
    }
    chart.update();
};

function buildTipboardObject() {
    window.Tipboard = {};
    Tipboard.Dashboard = {
        flipIds: [],
        updateFunctions: {},
        chartsIds: {},
        applyFading: initFading
    };
    Tipboard.chartJsTile = {};
    Tipboard.Dashboard.setDataByKeys = updateKeyOfTiles;
    Tipboard.Dashboard.autoAddFlipClasses = autoAddFlipClasses;
    Tipboard.Dashboard.updateDataOfChartJS = updateDataOfChartJS;
}

/**
 * Main function of tipboard.js
 * Define the $(document).ready(function()
 */
(function () {
    buildTipboardObject();
    initChartjsDefault();
    setTimeout(function () {
        initTiles();
        buildWebSocketManager();
    }, 420); // delay to let server start
}());
