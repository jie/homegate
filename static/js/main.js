function serialize_element(el) {
    var serialized = $(el).serialize();
    if (!serialized) // not a form
        serialized = $(el).find('input[name],select[name],textarea[name]').serialize();
    return serialized;
}

function docSting(f) {
    return f.toString().replace(/^[^\/]+\/\*!?\s?/, '').replace(/\*\/[^\/]+$/, '');
}

$(document).ready(function() {
    $('.dropdown')
        .dropdown({
            // you can use any ui transition
            transition: 'drop'
        });
    $('.message .close').on('click', function() {
        $(this).closest('.message').addClass('hidden');
    });

    // $('.sidebar').sidebar('show');
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
    console.log(selection);
    $(img).data('x1', selection.x1);
    $(img).data('y1', selection.y1);
    $(img).data('x2', selection.x2);
    $(img).data('y2', selection.y2);
    $(img).data('width', selection.width);
    $(img).data('height', selection.height);
}

$(function() {
    console.log($('#photo').data('x1'));
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
