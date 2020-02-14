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
        }, flipInterval);
    });
}

/**
 * Change html value to easily change color regarding color_mode
 * @param elementName div element type
 * @param value value to change in elementName
 * @param type to be generic with tag / class / id
 */
function changeElements(elementName, value, type) {
    let Elements = null;
    let copyElements = null;
    let size = null;
    switch (type) {
        case "tag":
            Elements = document.getElementsByTagName(elementName);
            for (let i = 0; i < Elements.length; i++) {
                Elements[i].style.color = value;
            }
            break;
        case "class-backgroundColor":
            Elements = document.getElementsByClassName(elementName);
            for (let i = 0; i < Elements.length; i++) {
                Elements[i].style.backgroundColor = value;
            }
            break;
        case "class-class":
            Elements = document.getElementsByClassName(elementName);
            copyElements = Array.prototype.slice.call(Elements);
            size = copyElements.length;
            for (let i = 0; i < size; i++) {
                copyElements[i].setAttribute("class", value);
            }
            break;
    }
}

/**
 * Change color of html element regarding color_mode
 */
function loadStyleColor() {
    // little hack to quick see what color_mode is on dashboard
    let mode___titleDashboard = document.getElementsByClassName("grid")[0].id.split("___");
    let mode = mode___titleDashboard[0];
    document.title = mode___titleDashboard[1];
    let body_style = document.getElementsByTagName("body")[0].style;
    if (mode === "black") {
        body_style.backgroundImage = "url('/static/img/logo-tipboard_white.svg')";
        body_style.backgroundColor = "#212121";
        changeElements("tile", "#313131", "class-backgroundColor");
        changeElements("card", "#313131", "class-backgroundColor");
        changeElements("mx-auto text", "mx-auto text-white", "class-class");
        changeElements(".row text", ".row text-white", "class-class");
        changeElements(".row center text", ".row center text-white", "class-class");
        changeElements("display-3 text", "display-3 text-white", "class-class");
        changeElements("h1 display-1 text", "h1 display-1 text-white", "class-class");
        changeElements("text", "text-white", "class-class");
        changeElements("h1", "#ffffff", "tag");
        changeElements("h2", "#ffffff", "tag");
        changeElements("h3", "#ffffff", "tag");
        changeElements("h6", "#ffffff", "tag");
        Chart.defaults.global.defaultFontColor = "rgba(255, 255, 255, 0.83)";
        Chart.defaults.global.elements.line.backgroundColor = "#FFFFFF";
        Chart.defaults.scale.gridLines.display = true;
        Chart.defaults.scale.gridLines.color = "#929292";
    } else {
        body_style.backgroundImage = "url('/static/img/logo-tipboard.svg')";
        body_style.backgroundColor = "#eceff1";
        changeElements("tile", "#f5f5f5", "class-backgroundColor");
        changeElements("card", "#f5f5f5", "class-backgroundColor");
        changeElements("mx-auto text-white", "mx-auto text", "class-class");
        changeElements(".row text-white", ".row text", "class-class");
        changeElements(".row center text", ".row center text-white", "class-class");
        changeElements("display-3 text", "display-3 text-white", "class-class");
        changeElements("h1 display-1 text-white", "h1 display-1 text", "class-class");
        changeElements("text-white", "text", "class-class");
        changeElements("h1", "#000", "tag");
        changeElements("h2", "#000", "tag");
        changeElements("h3", "#000", "tag");
        changeElements("h6", "#000", "tag");
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
        success(data) {
            Tipboard.chartJsTile = {};
            $("#tipboardIframe").html(data);
            loadStyleColor();
            initTiles();
            Tipboard.websocket.sendmessage(nextDashboardPath);
        },
        error(request, textStatus, error) {
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
        success(data) {
            let flipInterval = $("#tipboardIframe").attr("data-fliptime-interval");
                Flipboard.init(data.paths, data.names);
                showNextDashboard(Flipboard.getNextDashboardPath(), Flipboard.getNextDashboardName());
                if (data.paths.length > 1 && parseInt(flipInterval, 10) > 0) {
                    setInterval(function () { // start the flipping
                        showNextDashboard(Flipboard.getNextDashboardPath(), Flipboard.getNextDashboardName());
                    }, flipInterval  * 1000);
                }
        },
        error(request, textStatus, error) {
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
    Tipboard.updateFunctions["iframe"] = updateTileTextValue;
}

/**
 * Init Tipboard object & Tipboard.Dashboard object
 */
function initTipboardObject() {
    window.Tipboard = {
        DEBUG_MODE: true,  // TOFIX: with value from tipboard
        updateFunctions: {},
        chartJsTile: {},
        websocket: initWebSocketManager(),
        log(msg) {
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
        initChartjs();
        if (window.location.pathname === "/") {
            initFlipboard();
            getDashboardsByApi();
        } else { // No dashboard rotation
            showNextDashboard(window.location.pathname, window.location.pathname);
        }
    });
}($));
