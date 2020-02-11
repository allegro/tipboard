/**
 * Dynamicaly add Flipforward class to tile, regardind the dashboard.yml
 * @param flippingContainer
 */
function addFlipClasses(flippingContainer) {
    $.each($(flippingContainer).find(".tile"), function (idx, elem) {
        if (idx === 0) {
            $(elem).addClass("flippedforward");
        }
        $(elem).addClass("flippable");
    });
}

/**
 * Print a tile to indicate the type of error
 * @param err Exception Object
 * @param div tile_template
 * @param tileId id of tile
 */
let onTileError = function (err, div, tileId) {
    $.each([".tile-content"], function (idx, klass) {
        let nodes = $(div).find(klass);
        $(nodes[0]).hide();
        $(nodes[1]).show();
        let msg =
            "<div class=\"alert alert-danger text-center\" role=\"alert\" style=\"height: 100%;\">" +
                "<b>Tile: " + tileId +  "</b>" +
                " configuration error: " + err + "<br>" +
                "         error name: n/a <br>" +
                "         error message: n/a <br>" +
            "</div>";
        $('#' + tileId).html(msg);
    });
};

/**
 * return the flip time for every nodeHtml (representing tile)
 * @param node
 * @returns {number}
 */
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
        addFlipClasses(flippingContainer);
        let flipInterval = getFlipTime(flippingContainer);
        setInterval(function () {
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
        }, flipInterval); // let flipIntervalId =
        // Tipboard.flipIds.push(flipIntervalId);
    });
}

/**
 *
 * @param elementName
 * @param value
 * @param type
 */
function changeElements(elementName, value, type) {
    let Elements = null;
    switch (type) {
        case "tag":
            Elements = document.getElementsByTagName(elementName);
            for (let i = 0; i < Elements.length; i++) {
                Elements[i].style.color = value;
            }
            break;
        case "class":
            Elements = document.getElementsByClassName(elementName);
            for (let i = 0; i < Elements.length; i++) {
                Elements[i].style.backgroundColor = value;
            }
            break;
    }
}

function changeStyleColor(mode) {
    let body_style = document.getElementsByTagName("body")[0].style;
    if (mode === "black_mode") {
        body_style.backgroundImage = "url('/static/img/logo-tipboard_white.svg')";
        body_style.backgroundColor = "#212121";
        changeElements("tile", "#313131", "class");
        changeElements("card", "#313131", "class");
        changeElements("h1", "#ffffff", "tag");
        changeElements("h2", "#ffffff", "tag");
        changeElements("h3", "#ffffff", "tag");
        Chart.defaults.global.defaultFontColor = "rgba(255, 255, 255, 0.83)";
        Chart.defaults.global.elements.line.backgroundColor = "#FFFFFF";
        Chart.defaults.scale.gridLines.display = true;
        Chart.defaults.scale.gridLines.color = "#929292";
    } else {
        body_style.backgroundImage = "url('/static/img/logo-tipboard.svg')";
        body_style.backgroundColor = "#eceff1";
        changeElements("tile", "#f5f5f5", "class");
        changeElements("h1", "#000", "tag");
        changeElements("h2", "#000", "tag");
        changeElements("h3", "#000", "tag");
        Chart.defaults.global.defaultFontColor = "rgba(0, 0, 0, 0.83)";
        Chart.defaults.global.elements.line.backgroundColor = "#FFFFFF";
        Chart.defaults.scale.gridLines.display = true;
        Chart.defaults.scale.gridLines.color = "#525252";
    }
}

/**
 * show the next dashboard loaded from .yaml files
 * @returns {boolean}
 */
function showNextDashboard(nextDashboardPath, nextDashboardName) {
    $.ajax({
        method: "get",
        url: "/dashboard" + nextDashboardPath,
        success: function (data) {
            $("#tipboardIframe").html(data);
            changeStyleColor("black_mode");
            Tipboard.log("update div(tiles) for dashboard: " + nextDashboardPath);
            Tipboard.websocket.sendmessage(nextDashboardPath);
            Tipboard.log("Websocket asking info for dashboard:" + nextDashboardPath);
            document.title = nextDashboardName;
            initTiles();
        },
        error: function (request, textStatus, error) {
            Tipboard.log(request, textStatus, error);
            document.title = "Error loading: " + nextDashboardName;
        }
    });
    return true;
}

/**
 * Start the flip beetween dashboard
 * @param isFlipingMode
 */
function getDashboardsByApi() {
    $.ajax({
        method: "post",
        url: "/flipboard/getDashboardsPaths",
        success: function (data) {
            let flipInterval = $("#tipboardIframe").attr("data-fliptime-interval");
                Flipboard.init(data.paths, data.names);
                showNextDashboard(Flipboard.getNextDashboardPath(), Flipboard.getNextDashboardName());
                if (data.paths.length > 1 && parseInt(flipInterval, 10) > 0) {
                    setInterval(function () { // start the flipping
                        showNextDashboard(Flipboard.getNextDashboardPath(), Flipboard.getNextDashboardName());
                    }, flipInterval * 1000);
                }
        },
        error: function (request, textStatus, error) {
            Tipboard.log(request, textStatus, error);
            $(".error-message").html(["Error occured.", "For more details check javascript logs."].join("<br>"));
            $("#tipboardIframe").hide();
            $(".error-wrapper").show();
        }
    });
}

/**
 * Init Flipboard object
 */
function initFlipboard() {
    window.Flipboard = {
        currentPathIdx: -1,
        dashboardsPaths: [],
        dashboardsNames: [],

        init(paths, names) {
            this.dashboardsPaths = paths;
            this.dashboardsNames = names;
        },

        getNextDashboardPath() {
            this.currentPathIdx += 1;
            let lastIdx = this.dashboardsPaths.length - 1;
            if (this.currentPathIdx > lastIdx) {
                this.currentPathIdx = 0;
            }
            return this.dashboardsPaths[this.currentPathIdx];
        },

        getNextDashboardName() {
            return this.dashboardsNames[this.currentPathIdx];
        }
    };
}

/**
 * Init Global ChartJS value + build updateFunctions array
 */
function initChartjs() {
    Tipboard.updateFunctions["line_chart"] = updateChartjs;
    Tipboard.updateFunctions["radar_chart"] = updateChartjs;
    Tipboard.updateFunctions["norm_chart"] = updateChartjs;
    Tipboard.updateFunctions["pie_chart"] = updateChartjs;
    Tipboard.updateFunctions["polararea_chart"] = updateChartjs;
    Tipboard.updateFunctions["bar_chart"] = updateChartjs;
    Tipboard.updateFunctions["just_value"] = updateTileTextValue;
    Tipboard.updateFunctions["simple_percentage"] = updateTileTextValue;
    Tipboard.updateFunctions["big_value"] = updateTileTextValue;
    Tipboard.updateFunctions["listing"] = updateTileTextValue;
    Tipboard.updateFunctions["text"] = updateTileTextValue;
}

/**
 * Init Tipboard object & Tipboard.Dashboard object
 */
function initTipboardObject() {
    window.Tipboard = {
        DEBUG_MODE: true,  // TOFIX: with value from tipboard
        updateFunctions: {},
        chartJsTile: {},
        log: function (msg) {
            if (this.DEBUG_MODE) {
                console.log(msg);
            }
        }
    };
    Tipboard.log("Build Tipboard object start");
}

(function ($) {
    $(document).ready(function () {
        initTipboardObject();
        initWebSocketManager();
        initChartjs();
        if (window.location.pathname === '/') {
            initFlipboard();
            getDashboardsByApi(window.location.pathname === '/');
        } else { // No dashboard rotation
            showNextDashboard(window.location.pathname, window.location.pathname)
        }
    })
}($));
