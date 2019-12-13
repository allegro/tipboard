let onMessage = function (evt) {
    let tileData = JSON.parse(evt.data);
    if (tileData == null) {
        console.log("Web socket received NULL data");
    } else {
        console.log("Web socket received data: ", tileData);
        Tipboard.Dashboard.updateTile(Tipboard.Dashboard.escapeId(tileData.id),
            tileData.tile_template, tileData.data, tileData.meta, tileData.modified);
    }
};

/**
 * Test in Loop if Api is alive, when alive start a new Websocket connection
 */
let testApiIsBack = function () {
    let Http = new XMLHttpRequest();
    Http.open("GET", window.location.protocol + "/api/info");
    Http.onload = () => {
        if (Http.status === 200) {
            Tipboard.WebSocketManager.init();
        }
    };
    Http.onerror = () => {
        setTimeout(Tipboard.WebSocketManager.waitForAPI, 5000)
    };
    Http.send();
};

let onClose = function () {
    console.log("WebSocket closed: Waiting the API to be back, every 5s");
    setTimeout(Tipboard.WebSocketManager.waitForAPI, 5000)
};

let onError = function (evt) {
    console.log("WebSocket error: " + evt.data);
};

/**
 * Config the WebSocket object
 */
let buildSocket = function () {
    let protocol = window.location.protocol === "https:" ? "wss://" : "ws://";
    let websocket = new WebSocket(protocol + window.location.host + "/communication/websocket");

    websocket.onopen = function () {
        websocket.send("first_connection:" + window.location.pathname);
        console.log("Websocket: " + "Asking data to server" + window.location.href)
    };
    websocket.onclose = onClose;
    websocket.onmessage = onMessage;
    websocket.onerror = onError;
};

/**
 * Config the WebSocket Object & start a connection
 */
function initWebsocketManager(Tipboard) {
    console.log("Initializing new WebSocket");
    let WebSocketManager = {
        init: buildSocket,
        waitForAPI: testApiIsBack
    };
    Tipboard.WebSocketManager = WebSocketManager;
    buildSocket();
    return WebSocketManager;
}
