window.Tipboard = {};

function getFlipTime(node) {
    let classStr = $(node).attr("class");
    // TODO: make this flip time CUSTOM
    let flipTime = 4200;
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
 * Config the WebSocket Object
 */
let initWebSocket = function initWebSocket() {
    console.log("Initializing a new Web socket manager.");

    let protocol = window.location.protocol === "https:" ? "wss://" : "ws://";

    let websocket = new WebSocket(protocol + window.location.host + "/communication/websocket");
    websocket.onopen = function (evt) {
        websocket.send("first_connection:" + window.location.pathname);
        console.log("Websocket: " + "first_connection:" + window.location.href)
    };
    websocket.onclose = function (evt) {
        Tipboard.WebSocketManager.onClose(evt);
    };
    websocket.onmessage = function (evt) {
        Tipboard.WebSocketManager.onMessage(evt);
    };
    websocket.onerror = function (evt) {
        Tipboard.WebSocketManager.onError(evt);
    };
};

/**
 * Init the WebSocket Interface
 * @returns {init: init, onClose: onClose, onError: onError, onMessage: onMessage}
 */
function initWebsocketManager() {
    return {
        onClose: function () {
            setTimeout(Tipboard.WebSocketManager.init.bind(this), 1000);
        },

        onMessage: function (evt) {
            let tileData = JSON.parse(evt.data);
            if (tileData == null) {
                console.log("Web socket received NULL data");
            } else {
                console.log("Web socket received data: ", tileData);
                Tipboard.Dashboard.updateTile(Tipboard.Dashboard.escapeId(tileData.id),
                    tileData.tile_template, tileData.data, tileData.meta, tileData.modified);
            }
        },

        onError: function (evt) {
            console.log("WebSocket error: " + evt.data);
        },

        init: initWebSocket
    };
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

// function getTitleForChartJSTitleAsString(data) {
//     if (!((!("title" in data)) || (!("text" in data["title"])))) { // # Codacy quality
//         return {
//             display: false
//         };
//     }
//     return {
//         display: true,
//         text: data["title"]["text"],
//         borderColor: ("borderColor" in data) ? data["borderColor"] : "rgba(255, 255, 255, 1)",
//         color: ("color" in data) ? data["color"] : "#FFFFFF"
//     };
// }

/**
 * detect when no title & when title is in dict: affect values on specific tiles template type
 * @param data: value from redis for tile
 */
function getTitleForChartJSTitleAsString(data) {
    let isTitle = ((!("title" in data)) || (!("text" in data["title"])));
    return {
        display: !isTitle,
        text: (isTitle ? '' : data["title"]["text"]),
        borderColor: (isTitle ? '': ("borderColor" in data) ? data["borderColor"] : "rgba(255, 255, 255, 1)"),
        color: (isTitle ? '' : ("color" in data) ? data["color"] : "#FFFFFF")
    };
}

/**
 * Extract tile depending the type of the data
 * @param data
 * @returns {*}
 */
const getTitleForChartJSTitle = function (data) {
    try {
        getTitleForChartJSTitleAsString(data);
    } catch (e) { // catch start if data["title"] != dict in check (!("text" in data["title"]))
        return {
            display: true,
            text: data["title"],
            color: ("color" in data) ? data["color"] : "#FFFFFF"
        };
    }
};

/**
 * Main function of tipboard.js
 * Define the $(document).ready(function()
 */
(function ($) {

    Tipboard.Dashboard = {
        wsSocketTimeout: 900000,
        flipIds: [],
        updateFunctions: {},
        chartsIds: {},
    };
    Tipboard.WebSocketManager = initWebsocketManager();
    initDashboard(Tipboard);
    initPalette(Tipboard);
    $(document).ready(function () {
        console.log("Tipboard starting");
        //TODO: resize event
        Tipboard.WebSocketManager.init();
        setInterval(Tipboard.WebSocketManager.init.bind(Tipboard.WebSocketManager), Tipboard.Dashboard.wsSocketTimeout);
        initTiles();
    });
}($));
    // var x = window.matchMedia("(max-width: 500px)");
    // if (x.matches) { // If media query matches
    //     document.body.style.backgroundColor = "yellow";
    // } else {
    //     document.body.style.backgroundColor = "pink";
    //
    // }
    //     addEvent(window, "resize", function (event) {
    //         location.href = location.href; // location.reload(); is not working on firefox...
    //     });
