String.prototype.format = function(args) {
    var newStr = this;
    for (var key in args) {
        newStr = newStr.replace('{' + key + '}', args[key]);
    }
    return newStr;
};

(function (factory) {
    if (typeof define === 'function' && define.amd) {
        // AMD
        define(['jquery'], factory);
    } else if (typeof exports === 'object') {
        // CommonJS
        factory(require('jquery'));
    } else {
        // Browser globals
        factory(jQuery);
    }
}(function ($) {

    var pluses = /\+/g;

    function encode(s) {
        return config.raw ? s : encodeURIComponent(s);
    }

    function decode(s) {
        return config.raw ? s : decodeURIComponent(s);
    }

    function stringifyCookieValue(value) {
        return encode(config.json ? JSON.stringify(value) : String(value));
    }

    function parseCookieValue(s) {
        if (s.indexOf('"') === 0) {
            // This is a quoted cookie as according to RFC2068, unescape...
            s = s.slice(1, -1).replace(/\\"/g, '"').replace(/\\\\/g, '\\');
        }

        try {
            // Replace server-side written pluses with spaces.
            // If we can't decode the cookie, ignore it, it's unusable.
            // If we can't parse the cookie, ignore it, it's unusable.
            s = decodeURIComponent(s.replace(pluses, ' '));
            return config.json ? JSON.parse(s) : s;
        } catch(e) {}
    }

    function read(s, converter) {
        var value = config.raw ? s : parseCookieValue(s);
        return $.isFunction(converter) ? converter(value) : value;
    }

    var config = $.cookie = function (key, value, options) {

        // Write

        if (arguments.length > 1 && !$.isFunction(value)) {
            options = $.extend({}, config.defaults, options);

            if (typeof options.expires === 'number') {
                var days = options.expires, t = options.expires = new Date();
                t.setTime(+t + days * 864e+5);
            }

            return (document.cookie = [
                encode(key), '=', stringifyCookieValue(value),
                options.expires ? '; expires=' + options.expires.toUTCString() : '', // use expires attribute, max-age is not supported by IE
                options.path    ? '; path=' + options.path : '',
                options.domain  ? '; domain=' + options.domain : '',
                options.secure  ? '; secure' : ''
            ].join(''));
        }

        // Read

        var result = key ? undefined : {};

        // To prevent the for loop in the first place assign an empty array
        // in case there are no cookies at all. Also prevents odd result when
        // calling $.cookie().
        var cookies = document.cookie ? document.cookie.split('; ') : [];

        for (var i = 0, l = cookies.length; i < l; i++) {
            var parts = cookies[i].split('=');
            var name = decode(parts.shift());
            var cookie = parts.join('=');

            if (key && key === name) {
                // If second argument (value) is a function it's a converter...
                result = read(cookie, value);
                break;
            }

            // Prevent storing a cookie that we couldn't decode.
            if (!key && (cookie = read(cookie)) !== undefined) {
                result[name] = cookie;
            }
        }

        return result;
    };

    config.defaults = {};

    $.removeCookie = function (key, options) {
        if ($.cookie(key) === undefined) {
            return false;
        }

        // Must not alter options, thus extending a fresh object...
        $.cookie(key, '', $.extend({}, options, { expires: -1 }));
        return !$.cookie(key);
    };

}));

function serialize_element(el) {
    var serialized = $(el).serialize();
    if (!serialized) // not a form
        serialized = $(el).find('input[name],select[name],textarea[name]').serialize();
    return serialized;
}

function docSting(f) {
    return f.toString().replace(/^[^\/]+\/\*!?\s?/, '').replace(/\*\/[^\/]+$/, '');
}

function setSidebarHide() {
    $('.content_layout').addClass('remove_sidebar');
    var settings = $.cookie('HOMEGATECONFIG')
    if(settings){
        settings.sidebar = '0'; 
        $.cookie('HOMEGATECONFIG', settings, { path: '/', expires: 365});
    }else{
        $.cookie('HOMEGATECONFIG', {sidebar: '0'}, { path: '/', expires: 365});
    }
}

function setSidebarShow() {
    $('.content_layout').removeClass('remove_sidebar');
    var settings = $.cookie('HOMEGATECONFIG');
    if(settings){
        settings.sidebar = '1'; 
        $.cookie('HOMEGATECONFIG', settings, { path: '/', expires: 365});
    }else{
        $.cookie('HOMEGATECONFIG', {sidebar: '1'}, { path: '/', expires: 365});
    }
}

function checkCookies() {
    var cookie_settings = $.cookie('HOMEGATECONFIG');
    if(cookie_settings){
        if(cookie_settings.sidebar=='0'){
            $('.content_layout').addClass('remove_sidebar');
        }else{
            $('.content_layout').removeClass('remove_sidebar');
            $('.siteSidebar').sidebar('push page')
        }
    }else{
        $('.content_layout').removeClass('remove_sidebar');
    }
}

$(document).ready(function() {
    $.cookie.json = true;
    $('.dropdown')
        .dropdown({
            transition: 'drop'
        });
    $('.message .close').on('click', function() {
        $(this).closest('.message').addClass('hidden');
    });

    $('.siteSidebar')
        .sidebar('setting', 'dimPage', false)
        .sidebar('setting', 'closable', false)
        .sidebar('setting', 'closable', false)
        .sidebar('attach events', '.sidebar_ctrl')
        .sidebar('setting', 'onHide', setSidebarHide)
        .sidebar('setting', 'onVisible', setSidebarShow);

    checkCookies();
;
})

function previewPortrait(img, selection) {
    if (!selection.width || !selection.height)
        return;
    var scaleX = 100 / selection.width;
    var scaleY = 100 / selection.height;

    $('#preview img').css({
        width: Math.round(scaleX * img.width),
        height: Math.round(scaleY * img.height),
        marginLeft: -Math.round(scaleX * selection.x1),
        marginTop: -Math.round(scaleY * selection.y1)
    });
}

function setAvatarBox(img, selection) {
    $(img).data('x1', selection.x1);
    $(img).data('y1', selection.y1);
    $(img).data('x2', selection.x2);
    $(img).data('y2', selection.y2);
    $(img).data('width', selection.width);
    $(img).data('height', selection.height);
}

$(function() {
    if ($('#photo').data('x1')) {
        $('#photo').imgAreaSelect({
            x1: $('#photo').data('x1'),
            y1: $('#photo').data('y1'),
            x2: $('#photo').data('x2'),
            y2: $('#photo').data('y2'),
            aspectRatio: '1:1',
            handles: true,
            fadeSpeed: 200,
            onSelectChange: previewPortrait,
            onInit: previewPortrait,
            onSelectEnd: setAvatarBox,
            hide: true,
            autoHide: true
        });
    } else {
        $('#photo').imgAreaSelect({
            aspectRatio: '1:1',
            handles: true,
            fadeSpeed: 200,
            onSelectChange: previewPortrait,
            onInit: previewPortrait,
            onSelectEnd: setAvatarBox
        });
    }

});

