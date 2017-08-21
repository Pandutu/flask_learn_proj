$(function() {
    $('#btn_1').click(function() {
        alert('hello hell.');
    });
    $('#btn_2').mouseenter(function() {
        $('#btn_2').css("background-color", "#cccccc");
    });
    $('#btn_2').mouseleave(function() {
        $('#btn_2').css("background-color", "#d0d0d0");
    });

    $("ul.dragdroptest li").on('ondragstart', function(e) {
        e.dataTransfer.setData('text/plain', e.target.outerHTML);
        e.dataTransfer.setData('text/uri-list', document.location.href);
    });


    $('#drophere').on({
        'dragover': function(event) {
            event.preventDefault();
        },
        'drop': function(event) {
            event.preventDefault()
            alert('cnm')
        }
    })


    $("#jquery-animate-test-button").click(function() {
        var div = $("#colorBlock");
        div.animate({ height: '300px', opacity: '0.4' }, "slow");
        div.animate({ width: '300px', opacity: '0.8' }, "slow");
        div.animate({ height: '100px', opacity: '0.4' }, "slow");
        div.animate({ width: '100px', opacity: '0.8' }, "slow");
    });
})