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
	
	//write logged-in div
	function writeloggedin(results){
		$(".usersection").html($("<div/>").html("welcome  &nbsp;"+results['un']).attr("class", "welcomeuser"));
		$("<form/>").attr("class", "form2").appendTo(".usersection");
		$("<input/>").attr({
			type:"button",
			name:"edituser",
			class:"edituser",
			value:"edit profile"
		}).appendTo(".form2");
		$("<input/>").attr({
			type:"button",
			name:"logout",
			class:"logout",
			value:"logout"
		}).appendTo(".form2");
	}

	//write login div
	function writelogin(){
		$(".usersection").html($("<h1/>").html("Log-in"));
		$("<form/>").attr("class", "form1").appendTo(".usersection");
		$("<input/>").attr({
			type:"text",
			name:"user",
			class:"username",
			placeholder:"Username"
		}).appendTo(".form1");
		$("<input/>").attr({
			type:"password",
			name:"pass",
			class:"password",
			placeholder:"Password"
		}).appendTo(".form1");
		$("<input/>").attr({
			type:"button",
			name:"register",
			class:"register",
			value:"register"
		}).appendTo(".form1");
		$("<input/>").attr({
			type:"button",
			name:"login",
			class:"login",
			value:"login"
		}).appendTo(".form1");
	}

	//write file list
	function listFile(){
		$.ajax({
			url: "/listfile",
			success:function(results){
				var json = eval(results);
				if (json[0] == ""){
				} else {
					contentstr = "";
					if (json[0] == "empty"){			 
<<<<<<< HEAD
						$("<div/>").attr("id", "addfile").appendTo(".filelist");
						$("<input/>").attr({
							type:"button",
							name:"file_upload",
							id:"file_upload",
							value:"add file"
						}).appendTo("#addfile");
=======
						strtype = 1;
						$(endingstr).appendTo(".filelist");
>>>>>>> 1f115e13e028ed2b57cb328288e2db723fb6259b
					} else {
						for(var i=0; i<json.length; i++){
						    $("<tr/>").attr("class", "list_"+i.toString()).appendTo("tbody");
							$("<td/>").attr({
								class: "first"+i.toString(),
								id: json[i].filename
							}).html(json[i].filename).appendTo(".list_"+i.toString());			
							$("<td/>").attr({
								class: "second"+i.toString(),
								id: json[i].filename
							}).html(json[i].filename).appendTo(".list_"+i.toString());
							$("<td/>").attr({
								class: "third"+i.toString(),
								id: json[i].filename
							}).html(json[i].filename).appendTo(".list_"+i.toString());
							var contentstr = "<div id=\"zone-bar\"><ul><li><a href=\"#\"><span><h1>Action &nbsp;</h1><em class=\"opener-world\">" +
							"<img src=\"static/img/downarrow.png\" alt=\"dropdown\" /></em></span></a><ul><li><a href=\"#\" class=\""+i.toString()+
							"\" id=\"viewfile\">view</a></li><li><a href=\"#\" class=\""+i.toString()+"\" id=\"editfile\">Edit</a></li>" +
							"<li><a href=\"#\" class=\""+i.toString()+"\" id=\"deletefile\">Delete</a></li><li><a href=\"#\" class=\""+i.toString()+
							"\" id=\"sharefile\">Share</a></li></ul></li></ul></div>";
							$("<td/>").html(contentstr).appendTo(".list_"+i.toString());
							//contentstr += "<tr><td class=\"first_"+i.toString()+"\" id=\""+json[i].filename+"\">"+ json[i].filename +"</td>";
							//contentstr += "<td class=\"second_"+i.toString()+"\" id=\""+json[i].createon+"\">"+ json[i].createon +"</td>";
							//contentstr += "<td class=\"third_"+i.toString()+"\" id=\""+json[i].updateon+"\">"+ json[i].updateon +"</td>";
							//contentstr += "<td><div id=\"zone-bar\"><ul><li><a href=\"#\"><span><h1>Action &nbsp;</h1><em class=\"opener-world\">" +
							//"<img src=\"static/img/downarrow.png\" alt=\"dropdown\" /></em></span></a><ul><li><a href=\"#\" class=\""+i.toString()+
							//"\" id=\"viewfile\">view</a></li><li><a href=\"#\" class=\""+i.toString()+"\" id=\"editfile\">Edit</a></li>" +
							//"<li><a href=\"#\" class=\""+i.toString()+"\" id=\"deletefile\">Delete</a></li><li><a href=\"#\" class=\""+i.toString()+
							//"\" id=\"sharefile\">Share</a></li></ul></li></ul></div></td></tr>";				
						}
<<<<<<< HEAD
						//$(contentstr).appendTo("tbody");
						$("<div/>").attr("id", "addfile").appendTo(".filelist");
						$("<input/>").attr({
							type:"button",
							name:"file_upload",
							id:"file_upload",
							value:"add file"
						}).appendTo("#addfile");
=======
						strtype = 2;
						$(contentstr).appendTo("tbody");
						$(endingstr).appendTo(".filelist");
>>>>>>> 1f115e13e028ed2b57cb328288e2db723fb6259b
					}
				}
			}
		});
	}
});
