/**
 * Update text tile, font, color & value
 * @param tileId
 * @param data
 * @param meta
 * @param tileType
 */
function updateTileText(tileId, data, meta, tileType) {
    console.log("updateTileText::updateTile::start" + tileId);
    //let parser = new DOMParser();
    let body = document.getElementById(tileId + "-body");
    //let parsed = parser.parseFromString(data.text, `text/html`);
    //let tags = parsed.getElementsByTagName(`body`);
    body.innerHTML = '42';
    body.innerText = data.text;
}

Tipboard.Dashboard.registerUpdateFunction("text", updateTileText);
