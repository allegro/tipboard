(function ($) {
    'use strict';

    var showError = function (msg) {
        $('.error-message').html(msg);
        $('iframe').hide();
        $('.error-wrapper').show();
    };

    var Flipboard = {
        currentPathIdx: -1,
        dashboardsPaths: [],

        init: function (paths) {
            this.dashboardsPaths = paths;
        },

        getNextDashboardPath: function () {
            this.currentPathIdx += 1;
            var lastIdx = this.dashboardsPaths.length - 1;
            if (this.currentPathIdx > lastIdx) {
                this.currentPathIdx = 0;
            }
            var path = this.dashboardsPaths[this.currentPathIdx];
            return path;
        },

        showNextDashboard: function () {
            var nextDashboardPath = this.getNextDashboardPath();
            $('.error-wrapper').hide();
            var activeIframe = $($('iframe')[0]);
            if (nextDashboardPath === $(activeIframe).attr('src')) {
                console.log('same dashboard - SKIPPING');
                return false;
            }
            var clonedIframe = $(activeIframe.clone());
            clonedIframe.attr('src', nextDashboardPath);
            $('body').append(clonedIframe);
            $(clonedIframe).on('load', function() {
                $(activeIframe).remove();
                $(clonedIframe).addClass('fadeIn');
            });
        },

    };

    window.Flipboard = Flipboard;

    $(document).ready(function () {
        console.log('Flipboard starting:');
        $.ajax({
            method: 'post',
            url: "/flipboard/getDashboardsPaths",
            success: function(data) {
                console.log('loading layout:' + data.paths);
                Flipboard.init(data.paths);
                Flipboard.showNextDashboard();
                var flipInterval = $('iframe').attr('data-fliptime-interval');
                if (parseInt(flipInterval, 10) > 0) {
                    setInterval(function () {
                        Flipboard.showNextDashboard();
                    }, flipInterval * 1000);
                }
            }, 
            error: function(request, textStatus, error) {
                console.log(request, textStatus, error);
                var msg = [
                    'Error occured.',
                    'For more details check javascript logs.'
                ].join('<br>');
                showError(msg);
            }
        });
    });
}($));
