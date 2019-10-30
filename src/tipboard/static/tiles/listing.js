function appendListingItem(container, itemText) {
    let htmlLabel = [
        "<li class=\"list-group-item text-white\" style=\"background: #212121\">",
        itemText,
        "</li>"
    ].join("\n");
    $(container).append(htmlLabel);
}

function updateTileListing(id, data, meta, tileType) {
    let MAX_ITEMS = 7;
    let tile = $("#" + id)[0];
    let container = $(tile).find(".list-group")[0];
    $(container).children().remove();
    for (let idx in data.items) {
        if ({}.hasOwnProperty.call(idx, data.items)) {
            if (idx > MAX_ITEMS) {
                console.log(["ERROR: more then", MAX_ITEMS, "items passed - RENDERING STOPPED"].join(" "));
                break;
            }
            appendListingItem(container, data.items[parseInt(idx, 10)]);
        }
    }
}

Tipboard.Dashboard.registerUpdateFunction('listing', updateTileListing);



