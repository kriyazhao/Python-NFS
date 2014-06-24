function popup(msg,timer) {
	var 
	h = $(document).scrollTop() +$(window).height() ;
	w = $(window).width();
	lw = Math.floor(w/2-200/2);

	var ht = 
	'<div id="popup" style="display:none;position:absolute;top:100%;left:'+lw+
	'px;text-align:center;background:#f6f9cc;border:1px solid #999;width:200px;z-index:1200;box-shadow:0 0 5px rgba(0,0,0,.4)">' +
	'<div class="popup-content" style="padding:15px"></div>' +
	'<a href="javascript:;" class="close-popup" style="display:inline-block;line-height:20px;position:absolute;right:5px;top:5px;width:20px;text-decoration:none;height:20px;font-family:Arial;font-size:28px;font-weight:bold;text-align:center;color:#777;border-radius:50px;">&times;</a>' +
	'</div>';
	$('#popup').remove();
	$('body').append(ht);
	var t ;
	function popout() {
		$('#popup').animate({
			top:'100%'
		},500,function() {
			$('#popup').hide();
		});
	}
	
	$('#popup .close-popup').click(function() {
		clearTimeout(t);
		popout();
		
	}).hover(function() {
		$(this).css({
			color:'#000'
		})
	},function() {
		$(this).css({
			color:'#777'
		})
	});
	$('#popup .popup-content').html(msg);
	$('#popup').show().animate({
		top:h/2
	},500,function() {
		t = setTimeout(function() {
			popout();
		},timer? parseInt(timer):2000)
	});
	
}

function popup_viewlog(){
	var h = $(document).scrollTop() +$(window).height() ;
	$('#popup-viewlog').remove();
	$("<div/>").attr({
		id: "popup-viewlog",
	}).appendTo('body');
	$("<div/>").attr({
		class: "grayScreenClass",
	}).appendTo('body');
	$("<div/>").attr({
		class: "popup-content"
	}).appendTo("#popup-viewlog");
	$("<h1/>").html("Activity log").appendTo(".popup-content");
	$("<div/>").attr("class", "wholelog").appendTo(".popup-content");
	$("<input/>").attr({
		type:"button",
		class:"close",
		value:"Close"
	}).appendTo(".popup-content");
	$('#popup-viewlog').show();

	$(".close").click(function(){
		$("#popup-viewlog").remove();
		$(".grayScreenClass").remove();
	});
}


function popup_delete(fileName){
	var h = $(document).scrollTop() +$(window).height() ;
	$('#popup-delete').remove();
	$("<div/>").attr({
		id: "popup-delete",
	}).appendTo('body');
	$("<div/>").attr({
		class: "grayScreenClass",
	}).appendTo('body');
	$("<div/>").attr({
		class: "popup-content"
	}).appendTo("#popup-delete");
	$("<h1/>").html("Delete file").appendTo(".popup-content");
	$("<h4/>").html(fileName).appendTo(".popup-content");
	$("<input/>").attr({
		type:"button",
		class:"delete",
		value:"Delete"
	}).appendTo(".popup-content");
	$("<input/>").attr({
		type:"button",
		class:"cancel5",
		value:"Cancel"
	}).appendTo(".popup-content");

	$('#popup-delete').show();

	$(".cancel5").click(function(){
		$("#popup-delete").remove();
		$(".grayScreenClass").remove();
	});
}

function popup_forget(stage, username, email){
	var h = $(document).scrollTop() +$(window).height() ;
	$('.usersection').remove();
	$('#popup-forget').remove();
	$('.grayScreenClass').remove();
	$("<div/>").attr({
		id: "popup-forget",
	}).appendTo('body');
	$("<div/>").attr({
		class: "grayScreenClass",
	}).appendTo('body');
	$("<div/>").attr({
		class: "popup-content"
	}).appendTo("#popup-forget");

	if (stage == 1){
		$("<h1/>").html("Send code").appendTo(".popup-content");

		$("<input/>").attr({
			type:"text",
			class:"username-forget",
			placeholder:"Username"
		}).appendTo(".popup-content");
		$("<input/>").attr({
			type:"email",
			class:"email-forget",
			placeholder:"E-mail address"
		}).appendTo(".popup-content");
	} else if (stage ==2) {
		$("<h1/>").html("Validate code").appendTo(".popup-content");

		$("<input/>").attr({
			type:"text",
			class:"username-forget",
			value:username,
			readonly:true
		}).appendTo(".popup-content");
		$("<input/>").attr({
			type:"email",
			class:"email-forget",
			value:email,
			readonly:true
		}).appendTo(".popup-content");
		$("#popup-forget").css("height", "340px");
		$("<input/>").attr({
			type:"text",
			class:"validate-forget",
			placeholder:"Copy validation code here"
		}).appendTo(".popup-content");
	} else if (stage ==3) {
		$("<h1/>").html("Reset password").appendTo(".popup-content");
		$("<input/>").attr({
			type:"password",
			class:"password-forget",
			placeholder:"New password",
		}).appendTo(".popup-content");
		$("<input/>").attr({
			type:"password",
			class:"repw-forget",
			placeholder:"Re-enter password",
		}).appendTo(".popup-content");
	}

	$("<div/>").attr("class", "forgetinfo").appendTo(".popup-content");
	if (stage == 1){
		$("<input/>").attr({
			type:"button",
			class:"send",
			value:"Send"
		}).appendTo(".popup-content");
	} else if (stage ==2) {
		$("<input/>").attr({
			type:"button",
			class:"confirm",
			value:"Confirm"
		}).appendTo(".popup-content");
	} else if (stage ==3){
		$("<input/>").attr({
			type:"button",
			class:"reset",
			value:"Reset"
		}).appendTo(".popup-content");
	}

	$("<input/>").attr({
		type:"button",
		class:"cancel4",
		value:"Cancel"
	}).appendTo(".popup-content");

	$('#popup-forget').show();

	$(".cancel4").click(function(){
		$("#popup-forget").remove();
		$(".grayScreenClass").remove();
	});
}


function popup_share(results, response) {
	var h = $(document).scrollTop() +$(window).height() ;
	$('#popup-share').remove();
	$('.grayScreenClass').remove();

	$("<div/>").attr({
		id: "popup-share",
	}).appendTo('body');

	$("<div/>").attr({
		class: "grayScreenClass",
	}).appendTo('body');

	$("<div/>").attr({
		class: "popup-content"
	}).appendTo("#popup-share");

	$("<h1/>").html("Share file").appendTo(".popup-content");

	$("<div/>").attr({
		class: "radio-share"
	}).appendTo(".popup-content");

	$("<input/>").attr({
		id: "anyone",
		type: "radio",
		name: "share",
		value: "anyone",
	}).appendTo(".radio-share");

	$("<label/>").attr({
		for: "anyone",
		class:"anyone"
	}).html("Share with anyone").appendTo(".radio-share");

	$("<input/>").attr({
		id: "someone",
		type: "radio",
		name: "share",
		value: "someone",
		checked: "checked",
	}).appendTo(".radio-share");

	$("<label/>").attr({
		for: "someone",
		class:"someone"
	}).html("Share with someone").appendTo(".radio-share");

	$("<div/>").attr({
		class: "share-response"
	}).appendTo(".popup-content");

    if (response == "anyone"){
        $("<h4/>").html("MD5 and SHA1 to share").appendTo(".share-response");

        $("<div/>").attr({
            class: "share-code"
        }).html('<div>MD5: <input type="text" class="share-md5" value='+results.md5+'></div><div>SHA1:<input type="text" class="share-md5" value='+results.sha1+'></div>').appendTo(".share-response");

        $("<h4/>").html("Permission").appendTo(".share-response");

        $("<div/>").attr({
            class: "radio-permission"
        }).appendTo(".share-response");

        $("<input/>").attr({
            id: "canedit",
            type: "radio",
            name: "permission",
            value: "canedit",
        }).appendTo(".radio-permission");

        $("<label/>").attr({
            for: "canedit",
            class:"canedit"
        }).html("Can edit").appendTo(".radio-permission");

        $("<input/>").attr({
            id: "canview",
            type: "radio",
            name: "permission",
            value: "canview",
        }).appendTo(".radio-permission");

        $("<label/>").attr({
            for: "canview",
            class:"canview"
        }).html("Can view").appendTo(".radio-permission");
        
        // set up radio button
        if (results.privilege == "11") {
            $("#canview").attr("checked", "checked");
        } else if (results.privilege == "12") {
            $("#canedit").attr("checked", "checked");
        } else {}
        
        $("<div/>").attr({
            class: "share-button"
        }).appendTo(".share-response");

        $("<input/>").attr({
            type:"button",
            name:"share",
            class:"share",
            value:"Share"
        }).appendTo(".share-button");

        $("<input/>").attr({
            type:"button",
            name:"cancel3",
            class:"cancel3",
            value:"Cancel"
        }).appendTo(".share-button");

    } else if (response == "someone") {
        $("<h4/>").attr("class", "share-h4").html("Add member in the share list").appendTo(".share-response");
        $("<input/>").attr({
            class: "add-share",
            type: "button",
            value: "Add",
        }).appendTo(".share-response");

        $("<div/>").attr({
            class: "share-list"
        }).html('<table id ="share-table" class="reference3"><thead><tr><th>Username</th><th>Permission</th><th></th></tr></thead><tbody></tbody></table>').appendTo(".share-response");

        $("<tr>").attr("class", "row_0").appendTo(".reference3 tbody");
        $("<td>").attr("class", "first_0").html('<input type="text" class="user_0" value="'+results[0].owner+'" readonly>').appendTo(".row_0");
        $("<td>").attr("class", "second_0").html('<div class="radio-permission2"><input id="canedit_0" type="radio" name="permission_0" value="canedit_0" checked="checked"><label for="canedit_0" class="canedit_0">Owner</label></div>').appendTo(".row_0");
        $("<td>").attr("class", "third_0").html('<a id="delete-share" class="0"></a>').appendTo(".row_0");
        
        for (var i=1; i <= results.slice(1).length; i++) {            
            $("<tr>").attr("class", "row_"+i.toString()).appendTo(".reference3 tbody");
            $("<td>").attr("class", "first_"+i.toString()).html('<input type="text" class="user_'+i.toString()+'" value="'+results[i].sharedwithID+'">').appendTo(".row_"+i.toString());
            $("<td>").attr("class", "second_"+i.toString()).html('<div class="radio-permission2"><input id="canedit_'+i.toString()+'" type="radio" name="permission_'+i.toString()+'" value="canedit_'+i.toString()+'"><label for="canedit_'+i.toString()+'" class="canedit_'+i.toString()+'">Edit</label><input id="canview_'+i.toString()+'" type="radio" name="permission_'+i.toString()+'" value="canview_'+i.toString()+'"><label for="canview_'+i.toString()+'" class="canview_'+i.toString()+'">View</label></div>').appendTo(".row_"+i.toString());
            $("<td>").attr("class", "third_"+i.toString()).html('<a id="delete-share" class="'+i.toString()+'"></a>').appendTo(".row_"+i.toString());
            if (results[i].privilege == "21"){
                $("#canview_"+i.toString()).attr("checked", "checked");
            } else if (results[i].privilege == "22") {
                $("#canedit_"+i.toString()).attr("checked", "checked");
            }
        }
        
        $("<div/>").attr("class", "add-share-info").appendTo(".share-response");

        $("<div/>").attr({
            class: "share-button"
        }).appendTo(".share-response");

        $("<input/>").attr({
            type:"button",
            name:"share",
            class:"share",
            value:"Share"
        }).appendTo(".share-button");

        $("<input/>").attr({
            type:"button",
            name:"cancel3",
            class:"cancel3",
            value:"Cancel"
        }).appendTo(".share-button");

    }

	$('#popup-share').show();

	$(".cancel3").click(function(){
		$("#popup-share").remove();
		$(".grayScreenClass").remove();

	});

	$(".add-share").click(function(){
		var row_id = $('.reference3 tr').length - 1;
		$("<tr>").attr("class", "row_"+row_id.toString()).appendTo(".reference3 tbody");
		$("<td>").attr("class", "first_"+row_id.toString()).html('<input type="text" class="user_'+row_id.toString()+'" placeholder="i.e. kriyazhao">').appendTo(".reference3 .row_"+row_id.toString());
		$("<td>").attr("class", "second_"+row_id.toString()).html('<div class="radio-permission2"><input id="canedit_'+row_id.toString()+'" type="radio" name="permission_'+row_id.toString()+'" value="canedit_'+row_id.toString()+'" checked="checked"><label for="canedit_'+row_id.toString()+'" class="canedit_'+row_id.toString()+'">Edit</label><input id="canview_'+row_id.toString()+'" type="radio" name="permission_'+row_id.toString()+'" value="canview_'+row_id.toString()+'"><label for="canview_'+row_id.toString()+'" class="canview_'+row_id.toString()+'">View</label></div>').appendTo(".reference3 .row_"+row_id.toString());
		$("<td>").attr("class", "third_"+row_id.toString()).html('<a id="delete-share" class="'+row_id.toString()+'"></a>').appendTo(".reference3 .row_"+row_id.toString());

	});

	$(document).on("click", "#delete-share", function(){
		var class_id=this.className;
		if (class_id != "0") {
			$(".reference3 .third_"+class_id).parent('tr').remove();
		}
	});
}

function popup_rename(filename, class_id, tableName) {
	var h = $(document).scrollTop() +$(window).height() ;
	
	$('#popup-rename').remove();
	
	$("<div/>").attr({
		id: "popup-rename",
	}).appendTo('body');
	
	$("<div/>").attr({
		class: "grayScreenClass",
	}).appendTo('body');

	$("<div/>").attr({
		class: "popup-content"
	}).appendTo("#popup-rename");

	$("<div/>").attr({
		class: "codeentry-rename"
	}).appendTo(".popup-content");
	
	$("<h1/>").html("Rename file").appendTo(".codeentry-rename");
	
	$("<form/>").attr({
		class: "popup-form"
	}).appendTo(".codeentry-rename");
	
	$("<input/>").attr({
		type:"text",
		name:filename,
		Tname:tableName,
		class:"newname",
		id:class_id,
		value:filename,
	}).appendTo(".popup-form");

	$("<div/>").attr({
		class:"renameinfo",
	}).appendTo(".popup-form");	

	$("<input/>").attr({
		type:"button",
		name:"rename",
		class:"rename",
		value:"Rename"
	}).appendTo(".popup-form");

	$("<input/>").attr({
		type:"button",
		name:"cancel2",
		class:"cancel2",
		value:"Cancel"
	}).appendTo(".popup-form");

	$(".cancel2").click(function(){
		$("#popup-rename").remove();
		$(".grayScreenClass").remove();

	});
	
	$('#popup-rename').show();
	
}


function popup_create() {
	var h = $(document).scrollTop() +$(window).height() ;
	
	$('#popup-create').remove();
	
	$("<div/>").attr({
		id: "popup-create",
	}).appendTo('body');
	
	$("<div/>").attr({
		class: "grayScreenClass",
	}).appendTo('body');

	$("<div/>").attr({
		class: "popup-content"
	}).appendTo("#popup-create");

	$("<div/>").attr({
		class: "codeentry-create"
	}).appendTo(".popup-content");
	
	$("<h1/>").html("Create file").appendTo(".codeentry-create");
	
	$("<form/>").attr({
		class: "popup-form"
	}).appendTo(".codeentry-create");
	
	$("<input/>").attr({
		type:"text",
		class:"createname"
	}).appendTo(".popup-form");
	
	$("<div/>").attr({
		class:"createinfo"
	}).appendTo(".popup-form");

	$("<input/>").attr({
		type:"button",
		class:"create2",
		value:"Create"
	}).appendTo(".popup-form");

	$("<input/>").attr({
		type:"button",
		class:"cancel2",
		value:"Cancel"
	}).appendTo(".popup-form");

	$(".cancel2").click(function(){
		$("#popup-create").remove();
		$(".grayScreenClass").remove();
	});

	$('#popup-create').show();
}

function popup_register(username, password) {
	var h = $(document).scrollTop() +$(window).height() ;

	$('#popup-register').remove();
	
	$("<div/>").attr({
		id: "popup-register",
	}).appendTo('body');
	
	$("<div/>").attr({
		class: "grayScreenClass",
	}).appendTo('body');

	$("<div/>").attr({
		class: "popup-content"
	}).appendTo("#popup-register");

	$("<div/>").attr({
		class: "codeentry-register"
	}).appendTo(".popup-content");
	
	$("<h1/>").html("Register").appendTo(".codeentry-register");
	
	$("<form/>").attr({
		class: "register-form"
	}).appendTo(".codeentry-register");

	$("<input/>").attr({
		type:"text",
		class:"firstname-register",
		placeholder:"First name"
	}).appendTo(".register-form");

	$("<input/>").attr({
		type:"text",
		class:"lastname-register",
		placeholder:"Last name"
	}).appendTo(".register-form");
	
	$("<input/>").attr({
		type:"text",
		class:"username-register",
		placeholder: "Username (8-16 characters)",
		value:username
	}).appendTo(".register-form");

	$("<input/>").attr({
		type:"password",
		class:"password-register",
		placeholder: "Password (8-16 characters)",
	}).appendTo(".register-form");

	$("<input/>").attr({
		type:"password",
		class:"repw-register",
		placeholder: "Re-enter password"
	}).appendTo(".register-form");

	$("<input/>").attr({
		type:"email",
		class:"email-register",
		placeholder:"E-mail Address"
	}).appendTo(".register-form");
	$("<div/>").attr({
		class:"registerinfo",
	}).appendTo(".register-form");

	$("<input/>").attr({
		type:"button",
		class:"register2",
		value:"Register"
	}).appendTo(".register-form");

	$("<input/>").attr({
		type:"button",
		class:"cancel2",
		value:"Cancel"
	}).appendTo(".register-form");

	$(".cancel2").click(function(){
		$("#popup-register").remove();
		$(".grayScreenClass").remove();
		popup_login();
	});
	
	$('#popup-register').show();
	
}

function popup_login() {
	var h = $(document).scrollTop() +$(window).height() ;

	$('.usersection').remove();
	
	$("<div/>").attr({
		class: "usersection",
	}).appendTo('body');
	
	$("<div/>").attr({
		class: "imageScreenClass",
	}).appendTo('body');

	$("<h1/>").html("Log-in").appendTo(".usersection");
	
	$("<form/>").attr({
		class: "form1"
	}).appendTo(".usersection");

	$("<input/>").attr({
		type:"text",
		name:"user",
		class:"username",
		value:"test.account"
	}).appendTo(".form1");

	$("<input/>").attr({
		type:"password",
		name:"pass",
		class:"password",
		value: "#EDC3edc",
	}).appendTo(".form1");

	$("<input/>").attr({
		type:"button",
		name:"register",
		class:"register",
		value:"Register"
	}).appendTo(".form1");
	
	$("<input/>").attr({
		type:"button",
		name:"login",
		class:"login",
		value:"Login"
	}).appendTo(".form1");

	$("<div/>").attr({
		class: "login-help"
	}).html("<a href=\"#\">Forgot Password</a>").appendTo(".usersection");

	$('.usersection').show();
}

function popup_edituser(firstname, lastname, username, email) {
	var h = $(document).scrollTop() +$(window).height() ;

	$('#popup-edituser').remove();
	
	$("<div/>").attr({
		id: "popup-edituser",
	}).appendTo('body');
	
	$("<div/>").attr({
		class: "grayScreenClass",
	}).appendTo('body');

	$("<div/>").attr({
		class: "popup-content"
	}).appendTo("#popup-edituser");

	$("<div/>").attr({
		class: "codeentry-edituser"
	}).appendTo(".popup-content");
	
	$("<h1/>").html("Edit Profile").appendTo(".codeentry-edituser");
	
	$("<form/>").attr({
		class: "edituser-form"
	}).appendTo(".codeentry-edituser");

	$("<input/>").attr({
		type:"text",
		class:"firstname-edituser",
		placeholder:"First name",

		value:firstname
	}).appendTo(".edituser-form");

	$("<input/>").attr({
		type:"text",
		class:"lastname-edituser",
		placeholder:"Last name",
		value:lastname
	}).appendTo(".edituser-form");
	
	$("<input/>").attr({
		type:"text",
		class:"username-edituser",
		value:username,
		readonly:true
	}).appendTo(".edituser-form");

	$("<input/>").attr({
		type:"password",
		class:"oldpass-edituser",
		placeholder: "Old password",
	}).appendTo(".edituser-form");

	$("<input/>").attr({
		type:"password",
		class:"newpass-edituser",
		placeholder: "New password",
	}).appendTo(".edituser-form");

	$("<input/>").attr({
		type:"password",
		class:"renewpw-edituser",
		placeholder: "Re-enter new password"
	}).appendTo(".edituser-form");

	$("<input/>").attr({
		type:"email",
		class:"email-edituser",
		placeholder:"E-mail Address",
		value:email
	}).appendTo(".edituser-form");

	$("<div/>").attr({
		class:"registerinfo",
	}).appendTo(".edituser-form");

	$("<input/>").attr({
		type:"button",
		class:"saveedit",
		value:"Save"
	}).appendTo(".edituser-form");

	$("<input/>").attr({
		type:"button",
		class:"cancel2",
		value:"Cancel"
	}).appendTo(".edituser-form");

	$(".cancel2").click(function(){
		$("#popup-edituser").remove();
		$(".grayScreenClass").remove();
	});
	
	$(".save").click(function(){
		$("#popup-edituser").remove();
		$(".grayScreenClass").remove();
	});
	
	$('#popup-edituser').show();
	
}