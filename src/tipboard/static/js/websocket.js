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
    return Tipboard.updateFunctions[tileType.toString()];
}

/**
 * utils function to wait
 * @param ms time in millisecond
 */
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/**
 * Display button to inform user, server is diconnected
 * @param isRetry
 */
function serverDisconnected(isRetry) {
    let alert = $("#alertDeconnection");
    let decoMsg = alert.text();
    if (isRetry === false || decoMsg.includes("...")) {
        decoMsg = "Deconnected";
    } else {
        decoMsg = decoMsg + ".";
    }
    alert.text(decoMsg);
    alert.show();
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
        let stack = err.stack;
        let msg =
            "<div class=\"alert alert-danger\" role=\"alert\" style=\"height: 100%;\">" +
                "<b>Tile: " + tileId +  "</b>" +
                " configuration error: " + err.messages + "<br>" +
                " <p>error message:" + stack +  "</p><br>" +
            "</div>";
        $("#" + tileId).html(msg);
    });
};

/**
 * Destroy previous tile and create a new to refresh value
 * @param tileData
 * @param dashboardname
 */
function updateTile(tileData, dashboardname) {
    let chartId = `${dashboardname}-${tileData['id']}`;
    let tile = $("#" + chartId)[0];
    try {
        let tileFunction = getUpdateFunction(tileData["tile_template"]);
        tileFunction(tileData, dashboardname);
        $.each([".tile-content"], function (idx, klass) {
            let node = $(tile).find(klass);
            if (node.length > 1) {
                $(node[1]).remove();
                $(node[0]).show();
            }
        });
    } catch (err) {
        onTileError(err, tile, chartId);
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
            $("#alertDeconnection").hide();
            initWebSocketManager();
        }
    };
    Http.onerror = () => {
        serverDisconnected(true);
        setTimeout(testApiIsBack, 5000);
    };
    Http.send();
};

/**
 * Config the WebSocket Object & start a connection
 */
function initWebSocketManager() {
    let protocol = window.location.protocol === "https:" ? "wss://" : "ws://";
    let websocket = new WebSocket(protocol + window.location.host + "/communication/websocket");
    websocket.onopen = function () {
        Tipboard.log("[LOG] WEBSOCKET CONNECTION ONOPEN ");
    };
    websocket.onclose = function () { // Handler to detect when API is back alive to reset websocket connection every 5s
        serverDisconnected(false);
        if (Tipboard === "undefined") {
            Tipboard.log("[ERROR] Websocket Tipboard is not build");
        } else {
            setTimeout(testApiIsBack, 5000);
        }
    };
    websocket.sendmessage = async function(nextDashboardPath) {
        while (this.readyState === 0) {
            await sleep(200);
        }
        this.send("first_connection:" + nextDashboardPath);
        websocket.lastDashboard = nextDashboardPath.substring(1);
    };
    websocket.onmessage = function (evt) {
        let tileData = JSON.parse(evt.data);
        console.log("Web socket received data: ", tileData);
        updateTile(tileData, websocket.lastDashboard);
    };
    websocket.onerror = function (evt) {
        console.log("WebSocket error: ", evt.data);
    };
    return websocket;
}
