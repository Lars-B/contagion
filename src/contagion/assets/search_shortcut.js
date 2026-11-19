document.addEventListener("keydown", function (e) {
    const popup = document.getElementById("node-search-popup");
    const input = document.getElementById("node-search");
    if (!popup || !input) return;

    // Cmd+F (mac) / Ctrl+F (win/linux): open popup instead of browser find
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "f") {
        e.preventDefault();
        popup.classList.add("open");
        input.focus();
        input.select();
    }
    // Esc: close popup
    else if (e.key === "Escape" && popup.classList.contains("open")) {
        if (window.dash_clientside && dash_clientside.set_props) {
            dash_clientside.set_props("node-search", {value: ""});
        }

        popup.classList.remove("open");
        input.blur();
    }
});
