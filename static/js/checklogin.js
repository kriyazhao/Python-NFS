$(document).ready(function(){
	$("<div/>").html("Checking Status...").appendTo(".usersection");
	$.ajax({
		url:"/checklogin",
		dataType: 'json',
		success: function(json){
			var results = eval(json);
			if (results['r'] == '1'){
				writeloggedin(results);
			} else {
				writelogin();
			}
			listFile();
		}
	});
	
	//register user
	$(document).on('click','.register', function(){
		var username = $(".username").val();
		var pwraw = $(".password").val();
		if (username.length > 0 && pwraw.length > 0) {
			password = CryptoJS.MD5(pwraw).toString();
			$.ajax({
				type: "POST",
				url: "/register",
				data: JSON.stringify({"un":username,"pw":password}),
				dataType: 'json',
				success:function(json){
					var results = eval(json);
					if(results['r'] == 0){//username has been registered
						popup("username has been used, please change another name!");
					} else {
						if(results['r'] == 2){
							popup("login already! logout first before register!");
						} else if (results['r'] == 1){
							popup("register successfully!");
						}
						writeloggedin(results);
						setTimeout(function(){
								listFile();
							}, 1000);
					}
				}
			});
		} else {
			popup("username or password cannot be empty!")
		}
	});	
	
	// login user
	$(document).on('click','.login', function(){
		var username = $(".username").val();
		var pwraw = $(".password").val();
		if (username.length > 0 && pwraw.length > 0) {
			password = CryptoJS.MD5(pwraw).toString();
			$.ajax({
				type: "POST",
				url: "/login",
				data: JSON.stringify({"un": username, "pw":password}),
				dataType: 'json',
				success:function(json){
					var results = eval(json);
					if(results['r'] == 0){//username has been registered
						popup("username or password is incorrect!");
					} else {
						if(results['r'] == 2){
							popup("login already!");
						} else if(results['r'] == 1){
							popup("login successfully!");
						}
						writeloggedin(results);
						setTimeout(function(){
							listFile();
						}, 1000);
					}
				}
			});
		} else {
			popup("username or password cannot be empty!")
		}
	});
	
	var msg;
	//write logged-in div
	function writeloggedin(results){
		
		msg = "<div class=\"welcomeuser\">welcome  &nbsp;";
		msg += results['un'] + "</div>";
		msg += '<form class="form2"><input type="button" name="edituser" class="edituser" value="edit profile">';
		msg += '<input type="button" name="logout" class="logout" value="logout"></form>';
		$(".usersection").html(msg);
	}

	//write login div
	function writelogin(){
		msg = "<h1>Log-in</h1>";
		msg +="<form><input type=\"text\" name=\"user\" class=\"username\" placeholder=\"Username\">" +
				"<input type=\"password\" name=\"pass\" class=\"password\" placeholder=\"Password\">" +
				"<input type=\"button\" name=\"register\" class=\"register\" value=\"register\">" +
				"<input type=\"button\" name=\"login\" class=\"login\" value=\"login\"></form>" +
				"<div class=\"login-help\"><a href=\"#\">Forgot Password</a></div>";
		$(".usersection").html(msg);
	}

	//write file list
	function listFile(){
		$.ajax({
			url: "/listfile",
			success:function(results){
				var json = eval(results);
				if (json[0] == ""){
					strtype = 0;
				} else {
					endingstr = "<div id=\"addfile\"><input type=\"button\" name=\"file_upload\" id=\"file_upload\" value=\"add file\"></div>"
					contentstr = "";
					if (json[0] == "empty"){			 
						strtype = 1;
						$(endingstr).appendTo(".filelist");
						//$(".filelist").html(headingstr + endingstr1 + endingstr2);
					} else {
						for(var i=0; i<json.length; i++){
							contentstr += "<tr><td class=\"first_"+i.toString()+"\" id=\""+json[i].filename+"\">"+ json[i].filename +"</td>";
							contentstr += "<td class=\"second_"+i.toString()+"\" id=\""+json[i].createon+"\">"+ json[i].createon +"</td>";
							contentstr += "<td class=\"third_"+i.toString()+"\" id=\""+json[i].updateon+"\">"+ json[i].updateon +"</td>";
							contentstr += "<td><div id=\"zone-bar\"><ul><li><a href=\"#\"><span><h1>Action &nbsp;</h1><em class=\"opener-world\">" +
							"<img src=\"static/img/downarrow.png\" alt=\"dropdown\" /></em></span></a><ul><li><a href=\"#\" class=\""+i.toString()+
							"\" id=\"viewfile\">view</a></li><li><a href=\"#\" class=\""+i.toString()+"\" id=\"editfile\">Edit</a></li>" +
							"<li><a href=\"#\" class=\""+i.toString()+"\" id=\"deletefile\">Delete</a></li><li><a href=\"#\" class=\""+i.toString()+
							"\" id=\"sharefile\">Share</a></li></ul></li></ul></div></td></tr>";				
						}
						strtype = 2;
						$(contentstr).appendTo("tbody");
						$(endingstr).appendTo(".filelist");

						//$(".filelist").html(headingstr + contentstr + endingstr1 + endingstr2);
					}
				}
				
				
			}
		});
}
});