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

        init: initWebSocket,

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

        /**
         * Test if server is back, when online starting again WS client
         */
        testApiAlive: function () {
            const Http = new XMLHttpRequest();
            const url = window.location.protocol + "/api/info";
            Http.open("GET", url);
            Http.onload = () => {
                if (Http.status === 200) {
                    Tipboard.WebSocketManager.init();
                    Tipboard.WebSocketManager.init.bind(Tipboard.WebSocketManager);
                }
            };
            Http.onerror = () => {
                setTimeout(Tipboard.WebSocketManager.testApiAlive, 5000)
            };
            Http.send();
        },

        onError: function (evt) {
            console.log("WebSocket error: " + evt.data);
        },

        onClose: function () {
            console.log("WebSocket closed: Waiting the API to be back, every 5s");
            setTimeout(Tipboard.WebSocketManager.testApiAlive, 5000)
        },

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
        title["display"] = true;
        title["color"] = ("color" in data) ? data["color"] : "#FFFFFF";
        title["text"] = data["title"]["text"];
    }
    return title
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
    initDashboard(Tipboard);
    initPalette(Tipboard);
    Tipboard.WebSocketManager = initWebsocketManager();
    $(document).ready(function () {
        console.log("Tipboard starting");
        Tipboard.WebSocketManager.init();
        Tipboard.WebSocketManager.init.bind(Tipboard.WebSocketManager);
        initTiles();
    });
}($));
