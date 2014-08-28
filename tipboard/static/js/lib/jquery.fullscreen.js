(function($, window, documentElement, height, width) {
    
    // browser detection code courtesy of quirksmode, http://www.quirksmode.org/js/detect.html
    // slightly simplified, as well as minor changes for readability purposes

    var BrowserDetect = {
        init: function () {
            this.browser = this.searchString(this.dataBrowser) || "An unknown browser";
            this.version = this.searchVersion(navigator.userAgent)
                || this.searchVersion(navigator.appVersion)
                || "an unknown version";
            this.OS = this.searchString(this.dataOS) || "an unknown OS";
        },

        searchString: function (data) {
            for (var i=0;i<data.length;i++)    {
                var dataString = data[i].string;
                var dataProp = data[i].prop;
                this.versionSearchString = data[i].versionSearch || data[i].identity;
                if (dataString) {
                    if (dataString.indexOf(data[i].subString) != -1)
                        return data[i].identity;
                }
                else if (dataProp)
                    return data[i].identity;
            }
        },

        searchVersion: function (dataString) {
            var index = dataString.indexOf(this.versionSearchString);
            if (index == -1) return;
            return parseFloat(dataString.substring(index+this.versionSearchString.length+1));
        },

        dataBrowser: [
            { string: navigator.userAgent, subString: "Chrome",  identity: "Chrome"                            },
            { string: navigator.vendor,    subString: "Apple",   identity: "Safari",  versionSearch: "Version" },
            { prop: window.opera,                                identity: "Opera",   versionSearch: "Version" },
            { string: navigator.userAgent, subString: "Firefox", identity: "Firefox"                           },
            { string: navigator.userAgent, subString: "MSIE",    identity: "Explorer", versionSearch: "MSIE"   }
        ],

        dataOS : [
            { string: navigator.platform,  subString: "Win",    identity: "Windows"     },
            { string: navigator.platform,  subString: "Mac",    identity: "Mac"         },
            { string: navigator.platform,  subString: "Linux",  identity: "Linux"       }
        ]

    };

    BrowserDetect.init();
    // Browser name: BrowserDetect.browser
    // Browser version: BrowserDetect.version
    // OS name: BrowserDetect.OS
    
    // here are major browsers' keyboard mapping for triggering fullscreen on/off
    var keys = {
        "MSIE": {
            "Windows": { ctrlKey: false, altKey: false, metaKey: false, shiftKey: false, which: 122, string: "F11",               alt: "F11"               }
        },
        "Firefox": {
            "Windows": { ctrlKey: false, altKey: false, metaKey: false, shiftKey: false, which: 122, string: "F11",               alt: "F11"               },
            "Linux":   { ctrlKey: false, altKey: false, metaKey: false, shiftKey: false, which: 122, string: "F11",               alt: "F11"               },
            "Mac":     { ctrlKey: false, altKey: false, metaKey: true,  shiftKey: true,  which:  70, string: "&#x21E7;&#x2318;F", alt: "Shift+Command+F"   }
        },
        "Chrome": {
            "Windows": { ctrlKey: false, altKey: false, metaKey: false, shiftKey: false, which: 122, string: "F11",               alt: "F11"               },
            "Linux":   { ctrlKey: false, altKey: false, metaKey: false, shiftKey: false, which: 122, string: "F11",               alt: "F11"               },
            "Mac":     { ctrlKey: false, altKey: false, metaKey: true,  shiftKey: true,  which:  70, string: "&#x21E7;&#x2318;F", alt: "Shift+Command+F"   }
        },
        "Safari": { // still missing Safari on Windows... help!
            "Mac":     { ctrlKey: true,  altKey: false, metaKey: false, shiftKey: true,  which:  70, string: "^&#x2318;F",        alt: "Control+Command+F" }
        },
        "Opera": {
            "Windows": { ctrlKey: false, altKey: false, metaKey: false, shiftKey: false, which: 122, string: "F11",               alt: "F11"               },
            "Linux":   { ctrlKey: false, altKey: false, metaKey: false, shiftKey: false, which: 122, string: "F11",               alt: "F11"               },
            "Mac":     { ctrlKey: false, altKey: false, metaKey: true,  shiftKey: true,  which:  70, string: "&#x21E7;&#x2318;F", alt: "Shift+Command+F"   }
        },

    };

    var 
        isFullScreen = function() {
            return (documentElement.clientHeight == height && documentElement.clientWidth == width) ||
                window.fullScreen ||
                (window.outerHeight == height && window.outerWidth == width) ||
                (BrowserDetect.browser == "Safari" && window.outerHeight == (height - 40) && window.outerWidth == width)
            ;
        }
        ,$window = $(window)
    ;
    
    var thisKeys = keys[BrowserDetect.browser][BrowserDetect.OS];
    var shortcut = { shortcut: thisKeys.string, longform: thisKeys.alt };

    $window
        .data('fullscreen-state', isFullScreen())
        .data('fullscreen-key',   shortcut)
        .resize(function() {
            var fullscreenState = isFullScreen();
            
            if ($window.data('fullscreen-state') && !fullscreenState) {
                $window
                    .data('fullscreen-state', fullscreenState)
                    .trigger('fullscreen-toggle', [false])
                    .trigger('fullscreen-off')
                ;
            }
            else if (!$window.data('fullscreen-state') && fullscreenState) {
                $window
                    .data('fullscreen-state', fullscreenState)
                    .trigger('fullscreen-toggle', [true])
                    .trigger('fullscreen-on')
                ;
            }
        })
        .keydown(function(e) {
            if (thisKeys && e.ctrlKey == thisKeys.ctrlKey && e.altKey == thisKeys.altKey && e.metaKey == thisKeys.metaKey && e.shiftKey == thisKeys.shiftKey && e.which == thisKeys.which)
                $window.trigger('fullscreen-key', [thisKeys.string, thisKeys.alt]);
        })
    ;

})(jQuery, this, document.documentElement, screen.height, screen.width);
