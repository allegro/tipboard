/**
 * Update text tile, font, color & value
 * @param id
 * @param data
 * @param meta
 * @param tileType
 */
function updateTileText(tileId, data, meta, tileType) {
    console.log("updateTileText::updateTile::start" + tileId);
    let title = document.getElementById(tileId + '-title');
    let body = document.getElementById(tileId + '-body');
    if ("title" in data) {
        title.innerHTML = data["title"];
    }
    body.innerHTML = data["text"];
}

Tipboard.Dashboard.registerUpdateFunction('text', updateTileText);
