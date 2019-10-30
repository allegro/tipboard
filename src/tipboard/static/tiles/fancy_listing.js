function updateTileFancyListing(tileId, data, config, tileType) {
    let tile = Tipboard.Dashboard.id2node(tileId);
    let nodeToClone = FancyListing.initContainer(tile);
    if (typeof(nodeToClone) === 'undefined') {
        return false;
    }
    FancyListing.populateItems(tile, nodeToClone, data);
    FancyListing.applyConfig(tile, config);
    if (config['vertical_center'] === true) {
        FancyListing.verticalCenter(tile);
    }
}

Tipboard.Dashboard.registerUpdateFunction('fancy_listing', updateTileFancyListing);

FancyListing = {
    initContainer: function(tile) {
        let nodeToClone = $(tile).find('.fancy-listing-item')[0];
        if (typeof(nodeToClone) === 'undefined') {
            console.log('ABORTING - no node to clone');
            return false;
        }
        $(tile).find('.fancy-listing-item').slice(1).remove();
        return nodeToClone;
    },
    appendCloned: function(tile, nodeToClone) {
        let container = $(tile).find('.tile-content')[0];
        $(nodeToClone).clone().appendTo(container);
    },
    populateItems: function(tile, clonedNode, data) {
        $.each(data, function(idx, tileData) {
            FancyListing.appendCloned(tile, clonedNode);
            FancyListing.replaceData(tile, tileData);
        });
    },
    applyConfig: function(tile, config) {
        $.each(config, function(idx, tileConfig) {
            if (/\d+/.test(idx)) {
                let item = $(tile).find('.fancy-listing-item')[parseInt(idx)];
                let color = "#FFFFFF";
                $(item).find('.fancy-listing-label').css('background-color', color);
                // set centering
                if (tileConfig['center'] === true) {
                    $(item).find('.fancy-listing-def').css(
                        'text-align', 'center'
                    );
                }
            }
        });
    },
    verticalCenter: function(tile) {
        // TODO: replace it with css class and toggle the class
        let containerHeight = $(tile).find('.tile-content').height();
        let children = $(tile).find('.tile-content').children().slice(1);
        let childrensHeight = 0;
        $.each(children, function(idx, child) {
            childrensHeight += $(child).outerHeight(true);
        });
        let positionToSet = (containerHeight - childrensHeight) / 2;
        if (positionToSet > 0) {
            $(children[0]).css('padding-top', positionToSet);
        }
    },
    replaceData: function(tile, tileData) {
        let lastItem = $(tile).find('.fancy-listing-item:last-child')[0];
        $(lastItem).find('.fancy-listing-label-inside').html(tileData['label']);
        $(lastItem).find('.fancy-listing-term').html(tileData['text']);
        $(lastItem).find('.fancy-listing-desc').html(tileData['description']);
    }
};

