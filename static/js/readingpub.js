$(document).ready(function() {
    $("#errordata").hide();
    $("#errordataregister").hide();
    $("time.timeago").timeago();


    $(".please").each(function(index) {
        // random color for no-thumbs
        var color = Please.make_color({
	    base_color: 'rebeccapurple' //set your base color
        });
        $(this).css("background-color", color);
    });


    $(".edittag").click(function() {
        var id = $(this).data("id");
        var title = $(this).data("title");
        var url = $(this).data("url");
        $("#edittagModal").modal('toggle');
        $("#titleSpan").text(title);
        $("#idInput").val(id);
    });


    $('.thumb').hover( function() {
        $(this).find('.thumbnail-hover').fadeIn(300);
    }, function() {
        $(this).find('.thumbnail-hover').fadeOut(100);
    });

    $('.page-wrap').mouseup(function(e) {
        if(getSelectedText() != "") {
            // console.log(getSelectionCoords());
            var sel = window.getSelection();
            var range = sel.getRangeAt(0).cloneRange();
            var boundingRect = range.getBoundingClientRect();
            var yOffset = window.pageYOffset;

            // console.log(range.getClientRects());
            var rect = boundingRect;
            var left = rect.left;
            var right = rect.right;
            var top = rect.top + yOffset;
            var bottom = rect.bottom;
            var width = rect.width;
            var height = rect.height;
            $(".highlight-wrapper").css("width", width);
            $(".highlight-wrapper").css("height", height);
            $(".highlight-wrapper").css("left", left);
            $(".highlight-wrapper").css("top", top);
            $(".highlight-wrapper").show();
        } else {
            $(".highlight-wrapper").hide();
        }
    });

    $('.highlight-wrapper').click(function(e) {
        $(".highlight-wrapper").hide();
    });

    $('.highlighted').click(function() {
        var html = $(this).html()
        $(this).after(html);
        $(this).remove();
        syncData();
    });

});

function getSelectedText() {
    if (window.getSelection) {
        return window.getSelection().toString();
    } else if (document.selection) {
        return document.selection.createRange().text;
    }
    return '';
}

function highlightSelected() {
    var sel = window.getSelection();

    var div = document.createElement("div");
    div.className = "highlighted";

    if (sel.rangeCount) {
        var range = sel.getRangeAt(0).cloneRange();
        try {
            range.surroundContents(div);
        } catch(err) {
            alert("multiple paragraph highlighting not supported. (yet)");
        }

        sel.removeAllRanges();
        sel.addRange(range);
    }
    syncData();

    $('.highlighted').click(function() {
        var html = $(this).html()
        $(this).after(html);
        $(this).remove();
        syncData();
    });
}

function syncData() {
    // send content to server replace post-content
    var html = $(".content-data").html();
    var postid = $(".content-data").data("id");
    var currenturl = $(location).attr("href");

    var data = {
        content: html,
        postid: postid
    }

    $.ajax({
        type: "POST",
        url : "/post/sync",
        data: JSON.stringify(data, null, '\t'),
        contentType: 'application/json;charset=UTF-8',
        success: function(result) {
            var res = JSON.parse(result);
            if(res.status == "success") {
                // window.location.href = currenturl;
            }
        },
        error: function(result) {
            console.log(result);
        }
    });
}

// used on base
function login() {
    $("#errordata").hide();
    var currenturl = $(location).attr("href");
    var username = $("#usernamelogin").val();
    var password = $("#passwordlogin").val();
    var remember_me = $("#rememberme").is(":checked");

    var data = {
        username: username,
        password: password,
        remember_me: remember_me
    }

    console.log(data);
    $.ajax({
        type: "POST",
        url : "/login",
        data: JSON.stringify(data, null, '\t'),
        contentType: 'application/json;charset=UTF-8',
        success: function(result) {
            var res = JSON.parse(result);
            if(res.status == "error") {
                $("#errorlogin").text(res.result);
                $("#errordata").show();
            } else {
                window.location.replace(currenturl);
                console.log(res.result);
            }
        },
        error: function(result) {
            console.log(result);
        }
    });
}

function register() {
    $("#errordataregister").hide();
    var currenturl = $(location).attr("href");
    var error = $("#errorregister");
    var email = $("#emailregister").val();
    var username = $("#usernameregister").val();
    var password = $("#passwordregister").val();

    var data = {
        email: email,
        username: username,
        password: password
    }

    $.ajax({
        type: "POST",
        url : "/register",
        data: JSON.stringify(data, null, '\t'),
        contentType: 'application/json;charset=UTF-8',
        success: function(result) {
            var res = JSON.parse(result);
            if(res.status == "error") {
                $("#errorregister").text(res.result);
                $("#errordataregister").show();
            } else {
                window.location.replace(currenturl);
                console.log(res.result);
            }
        },
        error: function(result) {
            console.log(result);
        }
    });
}
