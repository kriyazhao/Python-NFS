$(document).ready(function(){
	$('.usersection').html("<div class=\"checklogin\">Checking Status...</div>");
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
	
	$(document).on('click','.register', function(){
		
		//register user
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
						} else if(results['r'] == 2){
							popup("login already! logout first before register!");
							writeloggedin(results);
							//listFile();
						} else if(results['r'] == 1){
							popup("register successfully!");
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
	
	$(document).on('click','.login', function(){
		//login user
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
					}
					else if(results['r'] == 2){
						popup("login already!");
						writeloggedin(results);
						setTimeout(function(){
							listFile();
						}, 1000);
					}
					else if(results['r'] == 1){
						popup("login successfully!");
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
});