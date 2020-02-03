/**
 * Return the Js func for a specific tile_template
 * @param tileType tile_template name
 * @returns {Function} js func to update html tile
 */
function getUpdateFunction(tileType) {
    switch (tileType) {
        case "vbar_chart":
            tileType = "bar_chart";
            break;
        case "doughnut_chart":
            tileType = "radar_chart";
            break;
        case "half_doughnut_chart":
            tileType = "radar_chart";
            break;
        case "cumulative_flow":
            tileType = "line_chart";
            break;
    }
    return Tipboard.Dashboard.updateFunctions[tileType.toString()];
}

/**
 * Destroy previous tile and create a new to refresh value
 * @param tileId
 * @param tileType
 * @param data
 * @param meta
 */
function updateTile(tileId, tileType, data, meta) {
    let tile = $("#" + tileId)[0];
    try {
        let chartObj = Tipboard.Dashboard.chartsIds[tileId.toString()];
        if (typeof chartObj === "object") {
            Tipboard.Dashboard.chartsIds[tileId.toString()].destroy();// destroy old graph
        }
        // ptr to function, call the tile update function
        getUpdateFunction(tileType)(tileId, data, meta, tileType);
        $.each([".tile-content"], function (idx, klass) {
            let node = $(tile).find(klass);
            if (node.length > 1) {
                $(node[1]).remove();
                $(node[0]).show();
            }
        });
    } catch (err) {
        onTileError(err, tile, tileId);
    }
}

/**
 * Test in Loop if Api is alive, when alive start a new Websocket connection
 */
let testApiIsBack = function () {
    let Http = new XMLHttpRequest();
    Http.open("GET", window.location.protocol + "/api/info");
    Http.onload = () => {
        if (Http.status === 200) {
            buildWebSocketManager();
        }
    };
    Http.onerror = () => {
        setTimeout(testApiIsBack, 5000);
    };
    Http.send();
};

/**
 * Config the WebSocket Object & start a connection
 */
function buildWebSocketManager() {
    let protocol = window.location.protocol === "https:" ? "wss://" : "ws://";
    let websocket = new WebSocket(protocol + window.location.host + "/communication/websocket");
    websocket.onopen = function () {
        websocket.send("first_connection:" + window.location.pathname);
    };
    websocket.onclose = function () { // Handler to detect when API is back alive to reset websocket connection every 5s
        setTimeout(testApiIsBack, 5000);
    };
    websocket.onmessage = function (evt) {
    let tileData = JSON.parse(evt.data);
        console.log("Web socket received data: ", tileData);
        updateTile(tileData.id, tileData.tile_template, tileData.data, tileData.meta, tileData.modified);
    };
    websocket.onerror = function (evt) {
        console.log("WebSocket error: ", evt.data);
    };
}
