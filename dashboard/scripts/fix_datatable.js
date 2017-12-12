$.initialize("div.react-grid-Toolbar .tools button.btn", function() {
	$(this).click();
});

$.initialize("div.react-grid-Toolbar", function() {
	$(this).hide();
});

$.initialize("div.react-grid-Cell .react-grid-Cell__value div span div", function() {
    if ($(this)[0].parentElement.parentElement.parentElement.parentElement.style.left == "0px") {
        $(this)[0].onclick = function () {
            window.history.pushState({}, '', "/queue/" + $(this)[0].title);
            window.dispatchEvent(new Event('onpushstate'));
            return false;
        };
    }
});
