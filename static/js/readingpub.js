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

});



// used on base
function login() {
    $("#errordata").hide();
    var currenturl = $(location).attr("pathname");
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
    var currenturl = $(location).attr("pathname");
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
