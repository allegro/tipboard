function updateTileText(id, data, meta, tileType) {
    let tile = $("#" + id)[0];
    let containers = $(tile).find(id);
    if (containers.length !== 1) {
        console.log("tile " + tile + "does not include ONE: " + "span.text-container");
    }
    let nodeWithText = containers[0];
    $(nodeWithText).html(data["text"]);

    let textSelector = "#" + id + " .text-container";
    if (meta.font_size) {
        $(textSelector).css("font-size", meta.font_size);
    }
    if (meta.font_color) {
        $(textSelector).css(
            "color", Tipboard.DisplayUtils.replaceFromPalette(meta.font_color)
        );
    }
    if (meta.font_weight) {
        $(".text-container").css("font-weight", meta.font_weight);
    }
}
Tipboard.Dashboard.updateFunctions["text"] = updateTileText;
