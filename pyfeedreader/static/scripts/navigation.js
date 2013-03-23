$(function() {
    $(document).keypress(function(event) {
        var ch = String.fromCharCode(event.keyCode || event.charCode);
        switch (ch) {
            case 'j': case 'J':
            next();
            break;

            case 'k': case 'K':
            previous();
            break;

            case 'x': case 'X':
            open_link();
            break;
        }
    });
});


function next() {
    var active_number = $("#active").attr("entryNumber");
    var new_number = parseInt(active_number) + 1;

    var new_active = $("div[entryNumber='"+new_number+"']");
    if(new_active.length != 0) {
        $("#active").removeAttr("id");
        new_active.attr("id", "active");
        read(new_active);
    }
}

function previous() {
    var active_number = $("#active").attr("entryNumber");
    var new_number = parseInt(active_number) - 1;

    var new_active = $("div[entryNumber='"+new_number+"']");
    if(new_active.length != 0) {
        $("#active").removeAttr("id");
        new_active.attr("id", "active");
        read(new_active);
    }
}

function read(entry) {
    $.post("/read",
        {
            entry_id: entry.attr("entryId")
        },
        function(data, status) {

        }
    );
}

function open_link() {
    window.open($("#active").attr("link"), '_blank');
}