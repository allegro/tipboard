function appendListingItem(container, itemText) {
    let htmlLabel = [
        "<li class=\"list-group-item text-white\" style=\"background: #212121\">",
        itemText,
        "</li>"
    ].join("\n");
    $(container).append(htmlLabel);
}

function updateTileListing(id, data, meta, tileType) {
    console.log("UPTADING LISTING");
    let MAX_ITEMS = 7;
    let tile = $("#" + id)[0];

    let container = $(tile).find(".list-group")[0];
    $(container).children().remove();
    for (let idx in data.items) {
        if ({}.hasOwnProperty.call(idx, data.items)) {
            if (idx > MAX_ITEMS) {
                console.log("BREAK CAUSE ITS TOO MUCH");
                break;
            }
                console.log("JAPPEND");
            appendListingItem(container, data.items[parseInt(idx, 10)]);
        } else {
            console.log("UPTADING LISTING ERROR NOT FOUNG");
        }
    }
    console.log("UPTADING LISTING END");
}

Tipboard.Dashboard.registerUpdateFunction('listing', updateTileListing);



