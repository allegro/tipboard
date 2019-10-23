function updateWidgetMatomo(tileId, data, meta, tileType) {
    console.log("HelloWorld! " + data);
    var ctx = document.getElementById(tileId + "-widget");
    console.log(ctx);
    ctx.src = data["url"];
    console.log("matomo_widget::type(" + tileType +")::updateWidget" + tileId);
}
console.log('I registered sir!');
Tipboard.Dashboard.registerUpdateFunction("matomo_widget", updateWidgetMatomo);

