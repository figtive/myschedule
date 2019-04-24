var $ = require("jquery");

$(document).ready(function() {
    const tabMenu = $('.tabs ul li');
    const tabSelections = $(".tabs-content .tab-selection");

    resetTabs()
    showTab(0)

    tabMenu.click(function() {
        if ($(this).hasClass("is-active")) {
            return
        }
        resetTabs()
        var tabMenuIndexClicked = tabMenu.index($(this));
        showTab(tabMenuIndexClicked)
    })

    function resetTabs() {
        tabSelections.css("display", "none")
        tabMenu.removeClass('is-active')
    }

    function showTab(index) {
        tabMenu.eq(index).addClass("is-active")
        tabSelections.eq(index).css("display", "block");
    }
})