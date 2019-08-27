function updateTileListing(id, data, meta, tipboard) {
    var MAX_ITEMS = 7;
    var tile = $('#' + id)[0];
    var container = $(tile).find('.list-group')[0];
    $(container).children().remove();
    for (idx in data.items) {
        if (idx > MAX_ITEMS) {
            console.log([
                'ERROR: more then',
                MAX_ITEMS,
                'items passed - RENDERING STOPPED'
            ].join(' '))
            break;
        }
        var textContent =  data.items[idx];
        appendListingItem(container, textContent);
    }
    Tipboard.TileDisplayDecorator.runAllDecorators(tile);
}

Tipboard.Dashboard.registerUpdateFunction('listing', updateTileListing);


function appendListingItem(container, itemText) {
    var htmlLabel = [
        '<li class="list-group-item text-white" style="background: #212121">',
        itemText,
        '</li>'
    ].join('\n');
    $(container).append(htmlLabel);
}

