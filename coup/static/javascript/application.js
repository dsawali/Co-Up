// displays tab on page load based on previous request
show_tab = function () {
    var positions_btn = $('button#positions');
    var users_btn = $('button#users');

    if (location.href.includes('company')) {
        if (!positions_btn.prop('class').includes('active')) {
            positions_btn.change(switch_tab());
            users_btn.toggleClass('active');
            positions_btn.toggleClass('active');
        }
    }
    else if (location.href.includes('username')) {
        if (!users_btn.prop('class').includes('active')) {
            users_btn.change(switch_tab());
            positions_btn.toggleClass('active');
            users_btn.toggleClass('active');
        }
    }
}

// displays selected search tab on search page
switch_tab = function () {
    var sel_btn = $(this).attr('id');
    var positions_btn = $('button#positions');
    var positions_tab = $('div#positions');
    var users_tab = $('div#users');
    var users_btn = $('button#users');

    if (sel_btn == 'positions') {
        if (users_tab.css('display') != 'none') {
            users_tab.toggle();
        }
        if (positions_tab.css('display') == 'none') {
            positions_tab.toggle();
        }
    }
    else {
        positions_tab.toggle();
        users_tab.toggle();
    }
}

// sets the "active" class to selected tab
highlight_active_tab = function() {
    var element = $(this).prop('tagName');
    $(element + '.active').toggleClass('active');
    $(this).toggleClass('active');
}

// sets the "active" class to link of current page 
highlight_active_page = function() {
    var path = location.pathname;
    var page =  $('.navbar-nav li').filter(function(){
        return $(this).find('a').attr('href') === path;
    })
    
    $('.navbar-nav li.active').toggleClass('active');
    if (! page.attr('class').includes('active')) {
        page.toggleClass('active');
    }
}

// sets the "active" class to current paginator link
highlight_active_paginator = function() {
    var path = location.search
    if (path.includes('page')) {
        $('.pagination li.active').toggleClass('active');
        var link = $('.pagination li').filter(function() {
            return $(this).find('a').attr('href') == path;
        });
        link.toggleClass('active');
    }
}

setup = function() {
    highlight_active_page();
    highlight_active_paginator();
    $('.tab').on('click', 'button', switch_tab);
    $('.tab').on('click', 'button', highlight_active_tab);
    show_tab();

    // autocompletion of position titles
    $('input#id_company').autocomplete({
        source: 'api/get_companies/',
        minLength: 2
    });
    $('input#id_title').autocomplete({
        source: 'api/get_titles/',
        minLength: 2
    });
    $('input#id_username').autocomplete({
        source: 'api/get_usernames/',
        minLength: 2
    });
    $('input#id_fullname').autocomplete({
        source: 'api/get_fullnames/',
        minLength: 2
    });
}

$(document).ready(setup);


