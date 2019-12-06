/**
 * Update text tile, font, color & value
 * @param tileId
 * @param data
 * @param meta
 * @param tileType
 */
function updateTileText(tileId, data, meta, tileType) {
    console.log("updateTileText::updateTile::start" + tileId);
    let parser = new DOMParser();
//    let title = document.getElementById(tileId + "-title");
    let body = document.getElementById(tileId + "-body");
//    if ("title" in data) {
//        title.innerHTML = data["title"];
//    }
    let parsed = parser.parseFromString(data["text"], `text/html`);
    let tags = parsed.getElementsByTagName(`body`);
    body.innerHTML = '';
    for (const tag of tags) {
        body.appendChild(tag);
    }

}

Tipboard.Dashboard.registerUpdateFunction("text", updateTileText);
