$(document).ready(function(){
	
	// setup csrf token
	function csrfSafeMethod(method) {
	    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}
	$.ajaxSetup({
	    crossDomain: false, // obviates need for sameOrigin test
		beforeSend: function(xhr, settings){
		    if (!csrfSafeMethod(settings.type)){
			    xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'))
			}
		}
	});

	$.ajax({
		url:"checklogin/",
		dataType: 'json',
		success: function(json){
			var results = eval(json);
			if (results['r'] == '1'){
				writeloggedin(results);
				listFile();
				ActivityLog(1);

			} else {
				popup_login();
			}
		}
	});
    
    	// table formatting
	$("#sublist").tabs();

	//text-bar formatting
	$(".filecontent").jqte();
	$(".jqte_editor").attr("contenteditable", false);

	$(document).on('keypress','.username', function(e){
		if(e.which == 13){//Enter key pressed
			$('.login').click();
		}
	});
	$(document).on('keypress','.password', function(e){
		if(e.which == 13){//Enter key pressed
			$('.login').click();
		}
	});

	$(document).on('keypress','.searchtext', function(e){
		if(e.which == 13){//Enter key pressed
			$('.search').click();
		}
	});

	$(document).on('keypress','.md5', function(e){
		if(e.which == 13){//Enter key pressed
			$('.extract').click();
		}
	});

	$(document).on('keypress','.sha1', function(e){
		if(e.which == 13){//Enter key pressed
			$('.extract').click();
		}
	});

	//register user
	$(document).on('click','.register', function(){
		var username = $(".username").val();
		var password = $(".password").val();
		popup_register(username, password);
		$(".usersection").remove();
		$(".imageScreenClass").remove();
		var firstnameV=false,lastnameV=false,usernameV=false,passwordV=false,repwV=false,emailV=false;

		$(".firstname-register").on("blur",function(){
			if ($(this).val() == ""){
				$(this).css("border", "2px solid #FF0000");
				$(".registerinfo").html("First name cannot be empty.");
			} else{
				firstnameV = inputValidation(this);
			}
		});
		$(".lastname-register").on("blur",function(){
			if ($(this).val() == ""){
				$(this).css("border", "2px solid #FF0000");
				$(".registerinfo").html("Last name cannot be empty.");
			} else{
				lastnameV = inputValidation(this);
			}
		});

		$(".username-register").on("blur",function(){
			if ($(this).val() == ""){
				$(this).css("border", "2px solid #FF0000");
				$(".registerinfo").html("Username cannot be empty.");
			} else{
				usernameV = inputValidation(this);
				if (usernameV) {
					$.ajax({
						type: "POST",
						url: "registerexist/",
						data: JSON.stringify({"un":$(this).val()}),
						success:function(results){
							if (results == "success"){$(this).css("border", "");$(".registerinfo").html("");}
							else if (results == "exist"){
								$(this).css("border", "2px solid #FF0000");
								$(".registerinfo").html("Username exists!");							
							} else if (results == "notvalid"){
								$(this).css("border", "2px solid #FF0000");
								$(".registerinfo").html("Username should only be 3-20 characters of numbers,letters and '-_.'.");
							} else if (results == "loggedin") {
								popup("You have logged in!");
							}
						}
					});
					t = setTimeout(function() {
						$("#popup").remove();
					},2000)
				}
			}
		});
		$(".password-register").on("blur",function(){
			if ($(this).val() == ""){
				$(this).css("border", "2px solid #FF0000");
				$(".registerinfo").html("Password cannot be empty.");
			} else{
				passwordV = inputValidation(this);
			}
		});
		$(".repw-register").on("blur",function(){
			if ($(this).val() == ""){
				$(this).css("border", "2px solid #FF0000");
				$(".registerinfo").html("Password cannot be empty.");
			} else{
				repwV = inputValidation(this);
			}
		});
		$(".email-register").on("blur",function(){
			if ($(this).val() == ""){
				$(this).css("border", "2px solid #FF0000");
				$(".registerinfo").html("Email cannot be empty.");
			} else{
				emailV = inputValidation(this);
			}
		});

		$(document).on('click','.register2', function(){
			if (firstnameV && lastnameV && usernameV && passwordV && repwV && emailV) {
				var firstname = $(".firstname-register").val();
				var lastname = $(".lastname-register").val();
				var username= $(".username-register").val();
				var password= $(".password-register").val();
				var email= $(".email-register").val();

				$.ajax({
					type: "POST",
					url: "register/",
					data: JSON.stringify({"un":username,"pw":password,"fn":firstname,"ln":lastname,"em":email}),
					dataType: 'json',
					success:function(json){
						var results = eval(json);
						if(results['r'] == "exist"){//username has been registered
							popup("username already exists.");
						} else if (results['r'] == "notvalid"){
							popup("username/password is not valid.");
						} else {
							if(results['r'] == "loggedin"){
								$("#popup-register").remove();
								$(".grayScreenClass").remove();
								popup("login already!");
							} else if (results['r'] == "success"){
								$("#popup-register").remove();
								$(".grayScreenClass").remove();
								popup("Successfully registered!");
							}
							writeloggedin(results);
							listFile();
							ActivityLog(1);

						}
					}
				});
			} else {
				if (!firstnameV){$(".firstname-register").blur();}
				if (!lastnameV){$(".lastname-register").blur();}
				if (!usernameV){$(".username-register").blur();}
				if (!passwordV){$(".password-register").blur();}
				if (!repwV){$(".repw-register").blur();}
				if (!emailV){$(".email-register").blur();}
				if (firstnameV && lastnameV && usernameV && passwordV && repwV && emailV) {
					$(".register2").click();
				}			
			}

			t = setTimeout(function() {
				$("#popup").remove();
			},2000);
		});
	});	
	
	function inputValidation(current) {
		var nameRegex = /^[a-zA-Z]{1,20}$/i;
		var usernameRegex = /^[a-zA-Z][a-zA-Z0-9._-]{3,20}$/i;
		var passwordRegex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*])[0-9a-zA-Z!@#$%^&*]{6,}$/i;
		var emailRegex = /^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$/i;
		var content = $(current).val();
		if ($(current).attr("class").indexOf("forget") >= 0){infoClass = ".forgetinfo";pwClass = ".password-forget";}
		else {infoClass = ".registerinfo";pwClass = ".password-register";}
		if ($(current).attr("type") == "text" && ($(current).attr("class").indexOf("firstname") >= 0 || $(current).attr("class").indexOf("lastname") >= 0)) {
			if (!nameRegex.test(content)) {
				$(current).css("border", "2px solid #FF0000");
				$(infoClass).html("First or last name should only be letters.");
				return false;
			} else {$(current).css("border", "");$(infoClass).html("");return true;}

		} else if($(current).attr("type") == "text" && $(current).attr("class").indexOf("username") >= 0) {
			if (!usernameRegex.test(content)) {
				$(current).css("border", "2px solid #FF0000");
				$(infoClass).html("Username should only be 3-20 characters of numbers,letters and '-_.'.");
				return false;
			} else {$(current).css("border", "");$(infoClass).html("");return true;}
		} else if($(current).attr("class").indexOf("repw") >= 0 || $(current).attr("class").indexOf("renewpw") >= 0) {
			if (!passwordRegex.test(content)) {
				$(current).css("border", "2px solid #FF0000");
				$(infoClass).html("Password should be at least 6 characters of numbers,letters (both A and a) and '!@#$%^&*'.");
				return false;
			} else {
				if ($(current).attr("class").indexOf("renewpw") >= 0) {
					if (content == $(".newpass-edituser").val()) {
						$(current).css("border", "");
						$(infoClass).html("");
						return true;
					} else {
						$(current).css("border", "2px solid #FF0000");
						$(infoClass).html("password entries are not consistent.");
						return false;
					}

				} else {
					
					if (content == $(pwClass).val()) {
						$(current).css("border", "");
						$(infoClass).html("");
						return true;
					} else {
						$(current).css("border", "2px solid #FF0000");
						$(infoClass).html("password entries are not consistent.");
						return false;
					}
				}
			}
		} else if($(current).attr("type") == "password") {
			if (!passwordRegex.test(content)) {
				$(current).css("border", "2px solid #FF0000");
				$(".registerinfo").html("Password should be at least 6 characters of numbers,letters (both A and a) and '!@#$%^&*'.");
				return false;
			} else {$(current).css("border", "");$(".registerinfo").html("");return true;}
		} else if($(current).attr("type") == "email") {
			if (!emailRegex.test(content)) {
				$(current).css("border", "2px solid #FF0000");
				$(".registerinfo").html("E-mail address is not valid.");
				return false;
			} else {$(current).css("border", "");$(".registerinfo").html("");return true;}
		}
	}

	// forget password
	$(document).on('click', '.login-help a', function(){
		popup_forget(1);
		var usernameV=false,emailV=false, passwordV=false, repwV=false;

		$(".username-forget").on("blur", function(){
			if ($(this).val() == ""){
				$(this).css("border", "2px solid #FF0000");
				$(".forgetinfo").html("Username cannot be empty.");
			} else{
				usernameV = inputValidation(this);
				if (usernameV) {
					$.ajax({
						type: "POST",
						url: "registerexist/",
						data: JSON.stringify({"un":$(this).val()}),
						success:function(results){
							if (results == "success"){
								$(this).css("border", "2px solid #FF0000");
								$(".forgetinfo").html("Username does not exist!");
							} else if (results == "exist"){
								$(this).css("border", "");$(".forgetinfo").html("");
							} else if (results == "notvalid"){
								$(this).css("border", "2px solid #FF0000");
								$(".forgetinfo").html("Username should only be 3-20 characters of numbers,letters and '-_.'.");
							} else if (results == "loggedin") {
								popup("You have logged in!");
							}
						}
					});
					t = setTimeout(function() {
						$("#popup").remove();
					},2000)
				}
			}

		});
		$(".email-forget").on("blur",function(){
			if ($(this).val() == ""){
				$(this).css("border", "2px solid #FF0000");
				$(".forgetinfo").html("Email cannot be empty.");
			} else{
				emailV = inputValidation(this);
			}
		});
			
		$(document).on('click','.send', function(){
			if (usernameV && emailV) {
				var username= $(".username-forget").val();
				var email= $(".email-forget").val();
				$.ajax({
					type: "POST",
					url: "forgetpassword/",
					data: JSON.stringify({"un":username,"em":email}),
					success:function(results){
						if (results == "success"){
							popup_forget(2, username, email);
							$(".forgetinfo").html("An email is successfully sent");
							$(document).on('click','.confirm', function(){
								var validatecode = $(".validate-forget").val();
								$.ajax({
									type: "POST",
									url: "validatecode/",
									data: JSON.stringify({"un":username,"em":email, "code": validatecode}),
									success:function(results){
										if (results == "fail"){
											$(".forgetinfo").html("Validation code is not correct.");
										} else if (results == "success") {
											popup_forget(3);
											$(".password-forget").on("blur",function(){
												if ($(this).val() == ""){
													$(this).css("border", "2px solid #FF0000");
													$(".forgetinfo").html("Password cannot be empty.");
												} else{
													passwordV = inputValidation(this);
												}
											});
											$(".repw-forget").on("blur",function(){
												if ($(this).val() == ""){
													$(this).css("border", "2px solid #FF0000");
													$(".forgetinfo").html("Password cannot be empty.");
												} else{
													repwV = inputValidation(this);
												}
											});
											$(".forgetinfo").html("validate successfully.");
											$(document).on('click','.reset', function(){
												if (passwordV && repwV) {
													var newpass = $(".password-forget").val();
													$.ajax({
														type: "POST",
														url: "resetpassword/",
														data: JSON.stringify({"un":username,"pw":newpass}),
														success:function(results){
															if (results == "notvalid"){
																$(".forgetinfo").html("Password is not valid");
															} else if (results == "success"){
																popup("successfully reset password!");
															}
															t = setTimeout(function() {
																$("#popup").remove();
																window.location.reload();
															},2000);
														}
													});
												}
											});
										}
									}
								});
							});
						} else {
							if (results == "fail"){
								$(".forgetinfo").html("Email is failed to send.");
							} else if (results == "notvalid") {
								$(".username-forget").css("border", "2px solid #FF0000");
								$(".forgetinfo").html("Username is not valid.");
							} else if (results == "notfound"){
								$(".forgetinfo").html("Username or email is not correct");
							}
						}
					}
				});
			}
		});
	
	});

	// login user
	$(document).on('click','.login', function(){
		var username = $(".username").val();
		var password = $(".password").val();
		if (username.length > 0 && password.length > 0) {
			$.ajax({
				type: "POST",
				url: "login/",
				data: JSON.stringify({"un": username, "pw":password}),
				dataType: 'json',
				success:function(json){
					var results = eval(json);
					if(results['r'] == 0){//username has been registered
						popup("username or password is incorrect!");
					} else if (results['r'] == 3) {
						popup("username or password is not valid!")
					} else {
						if(results['r'] == 2){
							popup("login already!");
						} else if(results['r'] == 1){
						}
						writeloggedin(results);
						listFile();
						ActivityLog(1);

					}
				}
			});
		} else {
			popup("username or password cannot be empty!")
		}
		t = setTimeout(function() {
			$("#popup").remove();
		},2000)
	});
	
	$(document).on('click','.logout', function(){
		$.ajax({
			type: "GET",
			url: "logout/",
			dataType: 'json',
			success:function(json){
				results = eval(json)
				if(results['r'] == "1"){
					window.location.reload();
				}				
			}
		});
		
	});

	$(document).on('click','.edituser', function(){

		$.ajax({
			type: "GET",
			url: "edituser/",
			dataType: 'json',
			success:function(json){
				results = eval(json)
				if(results['r'] == "notlogin"){
					popup("You have not logged in.");
				} else if (results['r'] == "empty"){
					popup("The user is not found.");
				} else if (results['r'] == "success"){
					popup_edituser(results['fn'],results['ln'],results['un'],results['em']);
                    
                    var firstnameV=false,lastnameV=false,oldpassV=false,newpassV=false,repwV=false,emailV=false;
                    $(".firstname-edituser").on("blur",function(){
                        if ($(this).val() == ""){
                            $(this).css("border", "2px solid #FF0000");
                            $(".registerinfo").html("First name cannot be empty.");
                        } else{
                            firstnameV = inputValidation(this);
                        }
                    });

                    $(".lastname-edituser").on("blur",function(){
                        if ($(this).val() == ""){
                            $(this).css("border", "2px solid #FF0000");
                            $(".registerinfo").html("Last name cannot be empty.");
                        } else{
                            lastnameV = inputValidation(this);
                        }
                    });

                    $(".oldpass-edituser").on("blur",function(){
                        if ($(this).val() == ""){
                            $(this).css("border", "2px solid #FF0000");
                            $(".registerinfo").html("Old password cannot be empty.");
                        } else{
                            oldpassV = inputValidation(this);
                        }
                    });

                    $(".newpass-edituser").on("blur",function(){
                        if ($(this).val() == ""){
                            if ($(".renewpw-edituser").val() != "") {
                                $(this).css("border", "2px solid #FF0000");
                                $(".registerinfo").html("New password entries are not consistent.");
                            }
                        } else{
                            newpassV = inputValidation(this);
                        }
                    });

                    $(".renewpw-edituser").on("blur",function(){
                        if ($(this).val() == ""){
                            if ($(".newpass-edituser").val() != "") {
                                $(this).css("border", "2px solid #FF0000");
                                $(".registerinfo").html("New password entries are not consistent.");
                            }
                        } else{
                            repwV = inputValidation(this);
                        }
                    });
                    $(".email-edituser").on("blur",function(){
                        if ($(this).val() == ""){
                            $(this).css("border", "2px solid #FF0000");
                            $(".registerinfo").html("E-mail cannot be empty.");
                        } else{
                            emailV = inputValidation(this);
                        }
                    });

                    $(document).on('click','.saveedit', function(){
                        if ((firstnameV && lastnameV && oldpassV && emailV) && ((newpassV && repwV) || ($(".newpass-edituser").val()=="" && $(".renewpw-edituser").val()==""))) {
                            var firstname = $(".firstname-edituser").val();
                            var lastname = $(".lastname-edituser").val();
                            var oldpass= $(".oldpass-edituser").val();
                            var newpass= $(".newpass-edituser").val();
                            var email= $(".email-edituser").val();
                            $.ajax({
                                type: "POST",
                                url: "edituser/",
                                data: JSON.stringify({"oldpass":oldpass,"newpass":newpass,"fn":firstname,"ln":lastname,"em":email}),
                                success:function(results){
                                    if(results == "notcorrect"){
                                        popup("the old password is not correct.");
                                    } else if (results == "notvalid"){
                                        popup("the new password is not valid.");
                                    } else {
                                        if(results == "notlogin"){
                                            $("#popup-edituser").remove();
                                            $(".grayScreenClass").remove();
                                            popup_login();
                                        } else if (results == "success"){
                                            if (newpass != ""){
                                                popup("Successfully edit the profile, logout in 1 sec!");
                                                $(".logout").click();
                                            } else{
                                                $("#popup-edituser").remove();
                                                $(".grayScreenClass").remove();
                                                popup("Successfully edit the profile!");
                                            }
                                        }
                                    }
                                }
                            });
                        } else {
                            if (!firstnameV){$(".firstname-edituser").blur();}
                            if (!lastnameV){$(".lastname-edituser").blur();}
                            if (!oldpassV){$(".oldpass-edituser").blur();}
                            if (!emailV){$(".email-edituser").blur();}
                            if ((firstnameV && lastnameV && oldpassV && emailV) && ((newpassV && repwV) || ($(".newpass-edituser").val()=="" && $(".renewpw-edituser").val()==""))) {
                                $(".saveedit").click();
                            }
                        }
                        t = setTimeout(function() {
                            $("#popup").remove();
                        },2000);
                    });
				}				
			}
		});
	});
	//write logged-in div
	function writeloggedin(results){
		$(".imageScreenClass").remove();
		$(".usersection").remove();

		$("<div/>").attr("class","status").appendTo(".title");
		$("<div/>").html("<h4>Welcome &nbsp;"+results['un']+"</h4>").appendTo(".status");
		$("<div/>").attr("class", "statusbotton").appendTo(".status");
		$("<input/>").attr({
			type:"button",
			name:"edituser",
			class:"edituser",
			value:"Edit profile"
		}).appendTo(".statusbotton");
		$("<input/>").attr({
			type:"button",
			name:"logout",
			class:"logout",
			value:"Logout"
		}).appendTo(".statusbotton");
	}

	//write activity log
	function ActivityLog(type){
		$.ajax({
			url: "activitylog/",
			data: {"type":type},
			dataType: "json",
			success:function(json){
				results = eval(json);
				if (results[0] == "notlogin") {
					popup("You have not logged in!");
				} else {
					if (type == 1){
						className = ".activitylog";
						subName = "activity_log"
					}else if (type == 2){
						className = ".wholelog";
						subName = "whole_log"

					}
					if (results.length == 0) {
						$("<h4/>").html("No activity").appendTo(className);
					} else {
						var list1 = ["edit", "delete", "create", "upload", "copy"];
						var list2 = ["rename", "share", "de-share"];
						for (var i=0; i<results.length;i++) {
							$("<div/>").attr("class",subName+" log"+i.toString()).appendTo(className);

							if ("notself" in results[i]){ // others operate your file or share file with you
								if (list1.indexOf(results[i].action) >= 0) {
									if (list1.indexOf(results[i].action) == 0 || list1.indexOf(results[i].action) == 3) {$("<div/>").css("display","inline").html(results[i].notself+" "+results[i].action+"ed an item").appendTo(className+" .log"+i.toString());}
									else {$("<div/>").css("display","inline").html(results[i].notself+" "+results[i].action+"d an item").appendTo(className+" .log"+i.toString());}
									$("<div/>").css({display:"inline",float:"right"}).html(results[i].date).appendTo(className+" .log"+i.toString());
									if (list1.indexOf(results[i].action) == 1) {$("<div/>").html(results[i].curName).css("text-decoration", "line-through").appendTo(className+" .log"+i.toString());}
									else { $("<div/>").html(results[i].curName).appendTo(className+" .log"+i.toString());}
								} else {
									if (list2.indexOf(results[i].action) == 0) { // rename
										$("<div/>").css("display","inline").html(results[i].notself+" "+results[i].action+"d an item").appendTo(className+" .log"+i.toString());
										$("<div/>").css({display:"inline",float:"right"}).html(results[i].date).appendTo(className+" .log"+i.toString());
										var curName = results[i].curName.split("/")[0];
										var oldName = results[i].curName.split("/")[1];
										$("<div/>").html(curName).appendTo(className+" .log"+i.toString());
										$("<div/>").html(oldName).css("text-decoration", "line-through").appendTo(className+" .log"+i.toString());
									} else { //share/ de-share
										if (list2.indexOf(results[i].action) == 1){
											$("<div/>").css("display","inline").html(results[i].notself+" "+results[i].action+"d an item").appendTo(className+" .log"+i.toString());
											$("<div/>").css({display:"inline",float:"right"}).html(results[i].date).appendTo(className+" .log"+i.toString());
											$("<div/>").html(results[i].curName).appendTo(className+" .log"+i.toString());
											$("<div/>").html(results[i].sharedwithID+" "+results[i].privilege).appendTo(className+" .log"+i.toString());
										} else{
											$("<div/>").css("display","inline").html(results[i].notself+" "+results[i].action+"d an item").appendTo(className+" .log"+i.toString());
											$("<div/>").css({display:"inline",float:"right"}).html(results[i].date).appendTo(className+" .log"+i.toString());
											$("<div/>").html(results[i].curName).appendTo(className+" .log"+i.toString());
											$("<div/>").html(results[i].sharedwithID+" "+results[i].privilege).css("text-decoration", "line-through").appendTo(className+" .log"+i.toString());
										}
									}
								}
							}else{// youself operate file
								if (list1.indexOf(results[i].action) >= 0) {
									if (list1.indexOf(results[i].action) == 0 || list1.indexOf(results[i].action) == 3) {$("<div/>").css("display","inline").html("You "+results[i].action+"ed an item").appendTo(className+" .log"+i.toString());}
									else {$("<div/>").css("display","inline").html("You "+results[i].action+"d an item").appendTo(className+" .log"+i.toString());}
									$("<div/>").css({display:"inline",float:"right"}).html(results[i].date).appendTo(className+" .log"+i.toString());
									if (list1.indexOf(results[i].action) == 1) {$("<div/>").html(results[i].curName).css("text-decoration", "line-through").appendTo(className+" .log"+i.toString());}
									else { $("<div/>").html(results[i].curName).appendTo(className+" .log"+i.toString());}
								} else {
									if (list2.indexOf(results[i].action) == 0) { // rename
										$("<div/>").css("display","inline").html("You "+results[i].action+"d an item").appendTo(className+" .log"+i.toString());
										$("<div/>").css({display:"inline",float:"right"}).html(results[i].date).appendTo(className+" .log"+i.toString());
										var curName = results[i].curName.split("/")[0];
										var oldName = results[i].curName.split("/")[1];
										$("<div/>").html(curName).appendTo(className+" .log"+i.toString());
										$("<div/>").html(oldName).css("text-decoration", "line-through").appendTo(className+" .log"+i.toString());
									} else { //share / de-share

										if (list2.indexOf(results[i].action) == 1){
											$("<div/>").css("display","inline").html("You "+results[i].action+"d an item").appendTo(className+" .log"+i.toString());
											$("<div/>").css({display:"inline",float:"right"}).html(results[i].date).appendTo(className+" .log"+i.toString());
											$("<div/>").html(results[i].curName).appendTo(className+" .log"+i.toString());
											$("<div/>").html(results[i].sharedwithID+" "+results[i].privilege).appendTo(className+" .log"+i.toString());
										} else{
											if (results[i].sharedwithID == "You"){
											} else {
												$("<div/>").css("display","inline").html("You "+results[i].action+"d an item").appendTo(className+" .log"+i.toString());
												$("<div/>").css({display:"inline",float:"right"}).html(results[i].date).appendTo(className+" .log"+i.toString());
												$("<div/>").html(results[i].curName).appendTo(className+" .log"+i.toString());
												$("<div/>").html(results[i].sharedwithID+" "+results[i].privilege).css("text-decoration", "line-through").appendTo(className+" .log"+i.toString());
											}
										}
									}

								}
							}
						}
					}
				}
			}
		});
	}

	$(document).on("click", ".viewlog", function(){
		popup_viewlog();
		ActivityLog(2);
	});


	//write file list
	function listFile(){
		$.ajax({
			url: "listfile/",
			success:function(results){
				var json = eval(results);
				if (json[0] == "empty"){
                    		} else {
				$('tbody').find("tr:gt(0)").remove();

                        if (json[0] != null){
                            for(var i=0; i<json[0].length; i++){
                                $("<tr/>").attr("class", "list_"+i.toString()).appendTo(".reference tbody");
                                $("<td/>").attr({
                                    class: "first_"+i.toString()+" "+"viewfile",
                                    id: json[0][i].filename
                                }).html("<a class=\"first\" href=\"#\">"+json[0][i].filename+"</a>").appendTo(".reference .list_"+i.toString());			
                                $("<td/>").attr({
                                    class: "second_"+i.toString(),
                                    id: json[0][i].createon
                                }).html(json[0][i].createon).appendTo(".reference .list_"+i.toString());
                                $("<td/>").attr({
                                    class: "third_"+i.toString(),
                                    id: json[0][i].updateon
                                }).html(json[0][i].updateon).appendTo(".reference .list_"+i.toString());
                                var contentstr = "<div id=\"zone-bar\"><ul><li class=\"action-bar\"><a href=\"#\"><span><h1>Action &nbsp;</h1><em class=\"opener-world\">" +
                                "<img src=\"static/img/downarrow.png\" alt=\"dropdown\" /></em></span></a><ul><li><a href=\"#\" class=\""+i.toString()+
                                "\" id=\"editfile\">Edit</a></li><li><a href=\"#\" class=\""+i.toString()+"\" id=\"deletefile\">Delete</a></li>" +
                                "<li><a href=\"#\" class=\""+i.toString()+"\" id=\"sharefile\">Share</a></li><li><a href=\"#\" class=\""+i.toString()+
                                "\" id=\"renamefile\">Rename</a></li><li><a href=\"#\" class=\""+i.toString()+"\" id=\"appendfile\">Copy</a></li></ul></li></ul></div>";
                                $("<td/>").html(contentstr).appendTo(".reference .list_"+i.toString());
                            }
                        }
                        if (json[1] != null) {
                            for(var i=0; i<json[1].length; i++){
                                $("<tr/>").attr("class", "list_"+i.toString()).appendTo(".reference2 tbody");
                                $("<td/>").attr({
                                    class: "first_"+i.toString()+" "+"viewfile",
                                    id: json[1][i].filename
                                }).html("<a class=\"first\" href=\"#\">"+json[1][i].filename+"</a>").appendTo(".reference2 .list_"+i.toString());			
                                $("<td/>").attr({
                                    class: "second_"+i.toString(),
                                    id: json[1][i].owner
                                }).html(json[1][i].owner).appendTo(".reference2 .list_"+i.toString());
                                if (json[1][i].privilege == "12" || json[1][i].privilege == "22") {
                                    json[1][i].privilege = "Edit/View";
                                    var contentstr = "<div id=\"zone-bar\"><ul><li class=\"action-bar\"><a href=\"#\"><span><h1>Action &nbsp;</h1><em class=\"opener-world\">" +
                                    "<img src=\"static/img/downarrow.png\" alt=\"dropdown\" /></em></span></a><ul><li><a href=\"#\" class=\""+i.toString()+
                                    "\" id=\"editfile\">Edit</a></li><li><a href=\"#\" class=\""+i.toString()+"\" id=\"deletefile\">Delete</a></li>" +
                                    "<li><a href=\"#\" class=\""+i.toString()+"\" id=\"sharefile\">Share</a></li><li><a href=\"#\" class=\""+i.toString()+
                                    "\" id=\"renamefile\">Rename</a></li><li><a href=\"#\" class=\""+i.toString()+"\" id=\"appendfile\">Copy</a></li></ul></li></ul></div>";
                                } else {
                                    json[1][i].privilege = "View";
                                    var contentstr = "<div id=\"zone-bar\"><ul><li class=\"action-bar\"><a href=\"#\"><span><h1>Action &nbsp;</h1><em class=\"opener-world\">" +
                                    "<img src=\"static/img/downarrow.png\" alt=\"dropdown\" /></em></span></a><ul><li><a href=\"#\" class=\""+i.toString()+"\" id=\"deletefile\">Delete</a></li>" +
                                    "<li><a href=\"#\" class=\""+i.toString()+"\" id=\"renamefile\">Rename</a></li><li><a href=\"#\" class=\""+i.toString()+"\" id=\"appendfile\">Copy</a></li></ul></li></ul></div>";
                                }
                                $("<td/>").attr({
                                    class: "third_"+i.toString(),
                                    id: json[1][i].privilege
                                }).html(json[1][i].privilege).appendTo(".reference2 .list_"+i.toString());
                                
                                $("<td/>").html(contentstr).appendTo(".reference2 .list_"+i.toString());
                            }
                        }
                    
                }
				//mytable format
				$('#mytable').dataTable({
					"paging": true,
					"ordering": true,
					"order": [[2, "desc"]],
					"info": true,
					"pagingType": "full_numbers",
					"lengthMenu": [[6, 10, 15, -1], [6, 10, 15, "All"]],
					"bDestroy": true,
				});

				//mytable2 format
				$('#mytable2').dataTable({
					"paging": true,
					"ordering": true,
					"info": true,
					"pagingType": "full_numbers",
					"lengthMenu": [[6, 10, 15, -1], [6, 10, 15, "All"]],
					"bDestroy": true,
				});
                
                $(".dataTables_info").remove();
				$(".dataTables_length").remove();
				$("#mytable_first").remove();
				$("#mytable_previous").remove();
				$("#mytable_next").remove();
				$("#mytable_last").remove();
				$("#mytable2_first").remove();
				$("#mytable2_previous").remove();
				$("#mytable2_next").remove();
				$("#mytable2_last").remove();
			}
		});
	}

	$(document).on('click','.viewfile', function(){
		var class_name = $(this).attr("class").split(' ').slice(0,1);
        	if ($(this).closest('table').attr("id") == "mytable"){
            		var ownerName = "self";
			var fileName = $(".reference ."+class_name).attr("id");
        	} else if ($(this).closest('table').attr("id") == "mytable2"){
			var class_id = class_name.toString().substr(class_name.length - 1);
            		var ownerName = $(this).next().attr("id");
			var fileName = $(".reference2 ."+class_name).attr("id");
        	}
		$.ajax({
			type:"POST",
			url:"viewfile/",
			data:JSON.stringify({"filename":fileName, "owner":ownerName}),
			dataType:'text',
			success:function(results){
				if (results == "notlogin") {
					popup("You have not logged in!");
				} else if (results == "notfound") {
					popup("file is not found!");
				} else if (results == "internalerror") {
					popup("internall error!");
				} else {
					$(".editbar").html(fileName);
					if (ownerName == "self") {ownerName = "Yourself"};
					$(".editbar-owner").html(ownerName);
					$(".jqte_editor").html('loading');
					$(".jqte_editor").html(results);
					$(".jqte_editor").attr("contenteditable", false);
					$(".filestatus").html("View only");
				}
			}
		});
		t = setTimeout(function() {
			$("#popup").remove();
		},2000)
		return false;
	});

	// update file content
	$(document).on('click','#editfile', function(){
		var class_id = this.className;
        	if ($(this).closest('table').attr("id") == "mytable"){
            		var ownerName = "self"
			var fileName = $(".reference .first_"+class_id).attr("id");
        	} else if ($(this).closest('table').attr("id") == "mytable2"){
            		var ownerName = $(".reference2 .second_"+class_id).attr("id");
			var fileName = $(".reference2 .first_"+class_id).attr("id");
        	}

		$.ajax({
			type:"POST",
			url:"viewfile/",
			data:JSON.stringify({"filename":fileName, "owner":ownerName}),
			dataType:'text',
			success:function(results){
				if (results == "notlogin") {
					popup("You have not logged in!");
				} else if (results == "notfound") {
					popup("file is not found!");
				} else if (results == "internalerror") {
					popup("internall error!");
				} else {
					$(".editbar").html(fileName);
					if (ownerName == "self") {ownerName = "Yourself"};
					$(".editbar-owner").html(ownerName);
					$(".jqte_editor").html('loading');
					$(".jqte_editor").html(results);
					$(".jqte_editor").attr("contenteditable", true);
					$(".filestatus").html("File content will be automatically saved after done typing!");
					$(".jqte_tool").click(function(){
						if ($(".jqte_editor").attr("contenteditable") == "true"){
							saveContent(".jqte_editor");	
						}
					});
				}
			}
		});
		t = setTimeout(function() {
			$("#popup").remove();
		},2000)
		return false;
	});

	function saveContent(selector) {
			var content = $(selector).html();
			$(".filestatus").html("saving");
			$.ajax({
				type:"POST",
				url:"editfile/",
				data: JSON.stringify({"filename":$(".editbar").html(), "owner":$(".editbar-owner").html(), "content": content}),
				dataType: 'text',
				success:function(results){
					if(results == "success" || results == "exist"){
						$(".filestatus").html("saved");
					}
					else if(results == "internalerror"){
						$(".filestatus").html("internal error!");
					}
					else if(results == "notfound"){
						$(".filestatus").html("file is not found!");
					}
					else if(results == "notlogin"){
						popup("You have not logged in!");
					}
					t = setTimeout(function() {
						$("#popup").remove();
					},2000)
				}

			});
	}
	// save file content when done typing
	$(document).on('focus','.jqte_editor', function(){
		// sync after done typing text
		$(".jqte_editor").donetyping(function(){
			saveContent(this);	
		});
	});

	// delete file 
	$(document).on('click','#deletefile', function(){
		var class_id = this.className;
        	if ($(this).closest('table').attr("id") == "mytable"){
            		var ownerName = "self"
			var fileName = $(".reference .first_"+class_id).attr("id");
        	} else if ($(this).closest('table').attr("id") == "mytable2"){
            		var ownerName = $(".reference2 .second_"+class_id).attr("id");
			var fileName = $(".reference2 .first_"+class_id).attr("id");
        	}
		popup_delete(fileName);

		$(document).on('click','.delete', function(){
			$.ajax({
				type:"DELETE",
				url:"deletefile/",
				data:JSON.stringify({"filename":fileName, "owner": ownerName}),
				dataType: 'text',
				success:function(results){
					if(results == 'success'){
						if (ownerName == "self"){
							$(".reference .first_"+class_id).parent('tr').slideUp(1000);
							setTimeout(function(){
								$(".reference .first_"+class_id).parent('tr').remove();
							}, 1000); 
						} else {
							$(".reference2 .first_"+class_id).parent('tr').slideUp(1000);
							setTimeout(function(){
								$(".reference2 .first_"+class_id).parent('tr').remove();
							}, 1000); 
						}

					} else if (results == "notfound") {
						popup("File is not found.");
					}
					$("#popup-delete").remove();
					$(".grayScreenClass").remove();
				}
			});
			t = setTimeout(function() {
				$("#popup").remove();
			},2000)
			return false;
		});
		
	});

	//$(document).on('click','#file_upload', function(){
		$("#file-upload").uploadify({
			'swf': 'static//js//uploadify.swf',
			'cancelImg': 'static//js//uploadify-cancel.png',
			'uploader': '/uploadfile/',
			'auto': true,
			'folder': '\temp',
			'multi': false,
			'fileSizeLimit': 1024*5+'KB',
			'fileTypeDesc': 'Text Files',
			'fileTypeExts': '*.log; *.txt; *.py; *.ini; *.h; *.hpp; *.c; *.cpp; *.java; *.html; *.htm; *.php; *.js; *.jsp; *.asp; *.css; *.xml; *.sh; *.bsh; *.pl; *.pm; *.rb; *.rc; *.sql; *.nfo; *.mak; *.reg; *.cmd',
		});
		return false;
	//});
});