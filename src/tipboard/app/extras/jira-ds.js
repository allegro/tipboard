// If you want to use this script directly (i.e. without jira-ds.py), you can
// do it like this (remember to fill 'username' & 'password' in casper.start):
//
// casperjs jira-ds.js \
// (--project-key=P_KEY | --project-id=P_ID | --board-id=B_ID) --step=STEP

var utils = require('utils');
var casper = require('casper').create({
    verbose:  false,
    logLevel: 'info',
    pageSettings: {
        loadImages:  false,
        loadPlugins: false,
    },
    timeout: 10000,  // in milliseconds
    onTimeout: function () {
        this.echo('Timeout of 10 seconds has been reached');
        this.exit(1);
    },
});

// Uncomment if you need some additional diagnostic info.
// casper.on('remote.message', function (msg) {
//     this.echo('=== Remote message caught: ' + msg);
// });
// casper.on("page.error", function (msg, trace) {
//     this.echo("=== Page error: " + msg, "ERROR");
// });

// available steps: 'control-chart', 'summary', 'cvsr','velocity', 'issues-counts'
var step = casper.cli.options.step;
var project_key = casper.cli.options['project-key'];
var project_id = casper.cli.options['project-id'];
var board_id = casper.cli.options['board-id'];

var url_jira_login = '';  // needs to be filled in
var url_jira = '';  // needs to be filled in
var url_board = url_jira + '/secure/RapidBoard.jspa?rapidView=' + board_id;
var url_control = url_board + '&view=reporting&chart=controlChart&days=30';
var url_cumulative = url_jira + '/secure/ConfigureReport.jspa' +
    '?projectOrFilterId=project-' + project_id +
    '&periodName=daily&daysprevious=30&cumulative=true&versionLabels=major' +
    '&selectedProjectId=' + project_id + '&reportKey=' +
    'com.atlassian.jira.plugin.system.reports:createdvsresolved-report' +
    '&Next=Next';
var url_velocity = url_board + '&view=reporting&chart=velocityChart';
var url_summary = url_jira + '/browse/' + project_key;
var url_issues = url_summary + '?selectedTab=' +
    'com.atlassian.jira.plugin.system.project%3Aissues-panel';

casper.start(url_jira_login, function login() {
    "use strict";
    var form_selector = '#login-form',
        credentials = {};
    (function () {
        var system = require('system');
        credentials.user = system.env.JIRA_USER;
        credentials.password = system.env.JIRA_PASSWORD;
    }());
    this.fill(form_selector, {
        // 'os_username' and 'os_password' - names of the fields in login form
        'os_username': credentials.user,
        'os_password': credentials.password
    }, true);
});

casper.thenBypassUnless(step === 'control-chart', 2);
casper.thenOpen(url_control, function control_chart() {
    "use strict";

    var selector_data = '#ghx-chart-snapshot dt',
        selector_timeframe = '#ghx-chart-selector .js-chart-time-window',
        data = {};
    data = this.evaluate(function (selector_data, selector_timeframe) {
        var elems = document.querySelectorAll(selector_data),
            data = {},
            idxs = ['mean', 'median', 'min-time', 'max-time', 'issue-count'];
        for (i = 0; i < idxs.length; i += 1) {
            data[idxs[i]] = elems[i].textContent;
        };
        data.timeframe = document.querySelector(selector_timeframe).textContent;
        return data;
    }, selector_data, selector_timeframe);
    utils.dump(data);
});

casper.thenBypassUnless(step === 'summary', 2);
casper.thenOpen(url_summary, function summary() {
    "use strict";
    var selector_created = '#fragcreatedvsresolved span.created-issue-count',
        selector_resolved = '#fragcreatedvsresolved span.resolved-issue-count',
        data = {};
    data = this.evaluate(function (selector_created, selector_resolved) {
        var issues_created, issues_resolved, data = {};
        issues_created = document.querySelector(selector_created).textContent;
        issues_resolved = document.querySelector(selector_resolved).textContent;
        data = {
            'issues_created': issues_created,
            'issues_resolved': issues_resolved,
        };
        return data;
    }, selector_created, selector_resolved);
    utils.dump(data);
});

casper.thenBypassUnless(step === 'cvsr', 2);
casper.thenOpen(url_cumulative, function cvsr() {
    "use strict";
    var selector = '#createdvsresolved-report-datatable > tbody > tr',
        data = {};
    data = this.evaluate(function (selector) {
        var i, rows, data = {};
        rows = document.querySelectorAll(selector);
        for (i = 1; i < rows.length; i += 1) {
            data[rows[i].cells[0].textContent] = {
                'created': parseInt(rows[i].cells[1].textContent, 10),
                'resolved': parseInt(rows[i].cells[2].textContent, 10),
            };
        }
        return data;
    }, selector);
    utils.dump(data);
});

casper.thenBypassUnless(step === 'velocity', 2);
casper.thenOpen(url_velocity, function velocity() {
    "use strict";
    var selector = '#ghx-chart-data > table > tbody tr',
        data = {};
    data = this.evaluate(function (selector) {
        var i, rows = {}, data = {};
        rows = document.querySelectorAll(selector);
        for (i = 0; i < rows.length; i += 1) {
            data[rows[i].cells[0].textContent] = {
                'commitment': parseInt(rows[i].cells[1].textContent, 10),
                'completed': parseInt(rows[i].cells[2].textContent, 10),
            };
        }
        return data;
    }, selector);
    utils.dump(data);
});

casper.thenBypassUnless(step === 'issues-counts', 2);
casper.thenOpen(url_issues, function issues_counts() {
    // function that we gonna use in a loop to retrieve data from selectors
    "use strict";
    function get_data(selector) {
        var data = {};
        data = this.evaluate(function (selector) {
            var i, idx, rows = {}, data = {};
            rows = document.querySelectorAll(selector);
            // pack tr cells contents into more convenient structures
            for (i = 0; i < rows.length; i += 1) {
                idx = rows[i].cells[0].textContent.trim();
                if (rows[i].cells.length === 3) {
                    data[idx] = [
                        parseInt(rows[i].cells[1].textContent, 10),
                        rows[i].cells[2].textContent.trim(),
                    ];
                } else {
                    data[idx] = parseInt(rows[i].cells[1].textContent, 10);
                }
            }
            return data;
        }, selector);
        return data;
    }
    var i, issues = {}, selectors = [
        ['by_priority', '#fragunresolvedissuesbypriority div.mod-content table.aui > tbody > tr'],
        ['status_summary', '#fragstatussummary div.mod-content table.aui > tbody > tr'],
        ['by_issuetype', '#fragunresolvedissuesbyissuetype div.mod-content table.aui > tbody > tr'],
        ['by_assignee', '#fragunresolvedissuesbyassignee div.mod-content table.aui > tbody > tr'],
        ['by_component', '#fragunresolvedissuesbycomponent div.mod-content table.aui > tbody > tr'],
        //['by_version', '#fragunresolvedissuesbyfixversion div.mod-content table.aui > tbody > tr'],  // doesn't work (yet)
    ];
    for (i = 0; i < selectors.length; i += 1) {
        issues[selectors[i][0]] = get_data.call(this, selectors[i][1]);
    }
    utils.dump(issues);
});

// Prints all defined steps (useful for diagnostics). Please notice that
// both 'casper.thenOpen' and 'casper.start' contain 'casper.open', hence
// every on of these counts as two steps.
// Also, every 'casper.thenBypass' (and friends) counts as a separate step.
// utils.dump(casper.steps.map(function (step) {
//         return step.toString();
// }));

casper.run();
