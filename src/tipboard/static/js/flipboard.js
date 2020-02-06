function test() {
    Tipboard.websocket.send("first_connection:" + window.location.pathname);
}
/**
 * show the next dashboard loaded from .yaml files
 * @returns {boolean}
 */
let showNext = function showNextDashboard() {
    // $(".error-wrapper").hide();
    let nextDashboardPath = this.getNextDashboardPath();
    let activeIframe = $("#tipboardIframe"); // TODO:
    console.log("Contacting API: " + nextDashboardPath);
    $.ajax({
        method: "get",
        url: nextDashboardPath,
        success: function (data) {
            activeIframe.html(data);
            console.log("update div API: " + nextDashboardPath);
            test();
            //TODO: add fadeIn effect but fadeIn effect is based on name class, but jquery #tipboardIframe need it
        },
        error: function (request, textStatus, error) {
            console.log(request, textStatus, error);
        }
    });
    document.title = this.getNextDashboardName();
    return true;
};

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
        },

        showNextDashboard: showNext,
    };
}

function ajax() {
    $.ajax({
        method: "post",
        url: "/flipboard/getDashboardsPaths",
        success: function (data) {
            Flipboard.init(data.paths, data.names);
            Flipboard.showNextDashboard();
            let flipInterval = $("#tipboardIframe").attr("data-fliptime-interval");
            if (data.paths.length > 1 && parseInt(flipInterval, 10) > 0) {
                setInterval(function () { Flipboard.showNextDashboard();}, flipInterval * 1000);
            }
        },
        error: function (request, textStatus, error) {
            console.log(request, textStatus, error);
            $(".error-message").html(["Error occured.", "For more details check javascript logs."].join("<br>"));
            $("#tipboardIframe").hide();
            $(".error-wrapper").show();
        }
    });
}

(function ($) {
    $(document).ready(function () {
        console.log("Build Tipboard object start");
        buildTipboardObject();
        initChartjsDefault();
        buildWebSocketManager(this);
        setTimeout(function () {
            initTiles();
        }, 420); // delay to let server start
        initFlipboard();
        ajax()
    })
}($));
