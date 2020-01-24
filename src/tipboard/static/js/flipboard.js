/**
 * show the next dashboard loaded from .yaml files
 * @returns {boolean}
 */
let showNext = function showNextDashboard() {
    $(".error-wrapper").hide();
    let nextDashboardPath = this.getNextDashboardPath();
    let activeIframe = $($("iframe")[0]);
    if (nextDashboardPath === $(activeIframe).attr("src")) {
        console.log("same dashboard - SKIPPING");
        return false;
    }
    let clonedIframe = $(activeIframe.clone());
    clonedIframe.attr("src", nextDashboardPath);
    $("body").append(clonedIframe);
    $(clonedIframe).on("load", function () {
        $(activeIframe).remove();
        $(clonedIframe).addClass("fadeIn");
    });
    return true;
};

/**
 * Init Flipboard object
 */
function initFlipboard() {
    window.Flipboard = {
        currentPathIdx: -1,
        dashboardsPaths: [],

        init: function (paths) {
            this.dashboardsPaths = paths;
        },

        getNextDashboardPath: function () {
            this.currentPathIdx += 1;
            let lastIdx = this.dashboardsPaths.length - 1;
            if (this.currentPathIdx > lastIdx) {
                this.currentPathIdx = 0;
            }
            return this.dashboardsPaths[this.currentPathIdx];
        },

        showNextDashboard: showNext,
    };
}

(function ($) {
    initFlipboard();
    $(document).ready(
        function () {
            $.ajax({
                method: "post",
                url: "/flipboard/getDashboardsPaths",
                success: function (data) {
                    console.log("loading layout:" + data.paths);
                    Flipboard.init(data.paths);
                    Flipboard.showNextDashboard();
                    let flipInterval = $("iframe").attr("data-fliptime-interval");
                    if (parseInt(flipInterval, 10) > 0) {
                        setInterval(function () { Flipboard.showNextDashboard();}, flipInterval * 1000);
                    }
                },
                error: function (request, textStatus, error) {
                    console.log(request, textStatus, error);
                    $(".error-message").html(["Error occured.", "For more details check javascript logs."].join("<br>"));
                    $("iframe").hide();
                    $(".error-wrapper").show();
                }
            });
        }
    );
}($));
