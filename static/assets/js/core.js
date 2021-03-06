"use strict";
$(document).ready(function() {
    /* -- Menu js -- */
    $.sidebarMenu($('.vertical-menu'));
    $(function() {
        for (var a = window.location, abc = $(".vertical-menu a").filter(function() {
            return this.href == a;
        }).addClass("active").parent().addClass("active"); ;) {
            if (!abc.is("li")) break;
            $(".vertical-menu-detail .tab-pane").removeClass("show active");
            abc = abc.parent().addClass("in").parent().addClass("show active");
            if ($(".vertical-menu-detail #v-pills-crm").hasClass("show active")) {
                $(".vertical-menu-icon .nav-link").removeClass("active");
                $(".vertical-menu-icon #v-pills-crm-tab").addClass("active");
            }
            if ($(".vertical-menu-detail #v-pills-ecommerce").hasClass("show active")) {
                $(".vertical-menu-icon .nav-link").removeClass("active");
                $(".vertical-menu-icon #v-pills-ecommerce-tab").addClass("active");
            }
            if ($(".vertical-menu-detail #v-pills-hospital").hasClass("show active")) {
                $(".vertical-menu-icon .nav-link").removeClass("active");
                $(".vertical-menu-icon #v-pills-hospital-tab").addClass("active");
            }
            if ($(".vertical-menu-detail #v-pills-uikits").hasClass("show active")) {
                $(".vertical-menu-icon .nav-link").removeClass("active");
                $(".vertical-menu-icon #v-pills-uikits-tab").addClass("active");
            }
            if ($(".vertical-menu-detail #v-pills-pages").hasClass("show active")) {
                $(".vertical-menu-icon .nav-link").removeClass("active");
                $(".vertical-menu-icon #v-pills-pages-tab").addClass("active");
            }
        }
    });
    /* -- Infobar Setting Sidebar -- */
    $("#infobar-settings-open").on("click", function(e) {
        e.preventDefault();
        $(".infobar-settings-sidebar-overlay").css({"background": "rgba(0,0,0,0.4)", "position": "fixed"});
        $("#infobar-settings-sidebar").addClass("sidebarshow");
    });
    $("#infobar-settings-close").on("click", function(e) {
        e.preventDefault();
        $(".infobar-settings-sidebar-overlay").css({"background": "transparent", "position": "initial"});
        $("#infobar-settings-sidebar").removeClass("sidebarshow");
    });
    /* -- Menu Hamburger -- */
    $(".menu-hamburger").on("click", function(e) {
        e.preventDefault();
        $("body").toggleClass("toggle-menu");
        $(".menu-hamburger img").toggle();
    });
    /* -- Menu Topbar Hamburger -- */
    $(".topbar-toggle-hamburger").on("click", function(e) {
        e.preventDefault();
        $("body").toggleClass("topbar-toggle-menu");
        $(".topbar-toggle-hamburger img").toggle();
    });
    /* -- Media Size -- */
    function mediaSize() {
        if (window.matchMedia('(max-width: 767px)').matches) {
            $("body").removeClass("toggle-menu");
            $(".menu-hamburger img.menu-hamburger-close").hide();
            $(".menu-hamburger img.menu-hamburger-collapse").show();
        }
    };
    mediaSize();
    window.addEventListener('resize', mediaSize, false);
    /* -- Switchery -- */
    // var setting_first = document.querySelector('.js-switch-setting-first');
    // var switchery = new Switchery(setting_first, { color: '#3E8B69', size: 'small' });
    // var setting_second = document.querySelector('.js-switch-setting-second');
    // var switchery = new Switchery(setting_second, { color: '#3E8B69', size: 'small' });
    // var setting_third = document.querySelector('.js-switch-setting-third');
    // var switchery = new Switchery(setting_third, { color: '#3E8B69', size: 'small' });
    // var setting_fourth = document.querySelector('.js-switch-setting-fourth');
    // var switchery = new Switchery(setting_fourth, { color: '#3E8B69', size: 'small' });
    // var setting_fifth = document.querySelector('.js-switch-setting-fifth');
    // var switchery = new Switchery(setting_fifth, { color: '#3E8B69', size: 'small' });
    // var setting_sixth = document.querySelector('.js-switch-setting-sixth');
    // var switchery = new Switchery(setting_sixth, { color: '#3E8B69', size: 'small' });
    // var setting_seventh = document.querySelector('.js-switch-setting-seventh');
    // var switchery = new Switchery(setting_seventh, { color: '#3E8B69', size: 'small' });
    // var setting_eightth = document.querySelector('.js-switch-setting-eightth');
    // var switchery = new Switchery(setting_eightth, { color: '#3E8B69', size: 'small' });
    /* -- Bootstrap Popover -- */
    $('[data-toggle="popover"]').popover();
    /* -- Bootstrap Tooltip -- */
    $('[data-toggle="tooltip"]').tooltip();
});
