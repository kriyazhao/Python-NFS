$(document).ready(function(){

	function checksharelist(selector, callback){
		var classname = "."+selector.attr("class");
		var validate = false;
		if ($(classname).val() == "") {
			$(classname).css("border", "2px solid #FF0000");
			$(".add-share-info").html("Username cannot be empty");
			return validate;
		} else {
			$.ajax({
				type: "POST",
				url: "shareexist/",
				data: JSON.stringify({"un":$(classname).val()}),
				success:function(results){
					if (results == "success"){
						validate = true;
						var rowCount = $('.reference3 tbody tr').length;
						for (var i=0; i < rowCount; i++) {	
							if (classname != ".user_"+i.toString()){
								if ($(".user_"+i.toString()).val() == $(classname).val()){
									validate = false;
									$(classname).css("border", "2px solid #FF0000");
									$(".add-share-info").html("Username duplicated");
								}
							} 
						}
						if (validate == true){
							$(classname).css("border", "");
							$(".add-share-info").html("");
						}

					} else {
						if (results == "notfound"){
							$(classname).css("border", "2px solid #FF0000");
							$(".add-share-info").html("Username does not exist.");
						} else if (results == "notvalid"){
							$(classname).css("border", "2px solid #FF0000");
							$(".add-share-info").html("Username is not valid.");
						} else if (results == "notlogin") {
							popup("You have not logged in!");
						}
					}
					if (callback) {callback(validate);}
				}
			});
		}
	}

	//share file 
	$(document).on('click','#sharefile', function(){
		//delete file
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
			url:"sharefile/",
			data:JSON.stringify({"filename":fileName, "owner":ownerName}),
			dataType: 'json',
			success:function(json){
				var results = eval(json); // [{'md5':rows[1],'sha1':rows[2], 'owner':owner, 'privilege': rows[4]}]
				popup_share(results, "someone");

				$(document).on('click','.anyone', function(){
					popup_share(results[0], "anyone");
				});

				$(document).on('click','.someone', function(){
					popup_share(results, "someone");
				});

				$(document).on("blur", ".reference3 input", function(){
					checksharelist($(this));
				});	

				// anyone can edit: 12, anyone can view: 11, someone can edit: 22, someone can view: 21
				$(document).on("click", ".share", function(){
					if ($("#anyone").is(':checked')) {
						if ($("#canedit").is(':checked')) {
							$.ajax({
								type:"POST",
								url:"shareoption/",
								data:JSON.stringify({"privilege":12, "filename": fileName, "owner": ownerName}),
								success:function(results){
									if (results == "success") {
                                        					$("#popup-share").remove();
                                        					$(".grayScreenClass").remove();
                                        					popup("Successfully share the file!");
                                    				} else if (results == "notfound") {
                                        					popup("File is not found!");
                                    				} else if (results == "notlogin") {
                                        					popup("You have not logged in!");
                                    				}
								}
							});
						} else if ($("#canview").is(':checked')) {
							$.ajax({
								type:"POST",
								url:"shareoption/",
								data:JSON.stringify({"privilege":11, "filename": fileName, "owner": ownerName}),
								success:function(results){
									if (results == "success") {
                                        					$("#popup-share").remove();
                                        					$(".grayScreenClass").remove();
                                        					popup("Successfully share the file!");
                                    				} else if (results == "notfound") {
                                        					popup("File is not found!");
                                    				} else if (results == "notlogin") {
                                        					popup("You have not logged in!");
                                    				}
								}
							});
						}
					} else if ( $("#someone").is(':checked')) {
						var rowCount = $('.reference3 tbody tr').length;
						var sharelist = [fileName]
						var checkmember = true;
						for (var i=0; i < rowCount; i++) {
						    	checksharelist($(".user_"+i.toString()), function(validate){
								if (validate == false){
									checkmember = false;
								} 		
							});							
						}
						if (checkmember == true) {
							for (var i=0; i < rowCount; i++) {
								var member = {}
								member.un = $(".user_"+i.toString()).val();
								if ($("#canedit_"+i.toString()).is(':checked')){
									member.privilege = 22
								} else if ($("#canview_"+i.toString()).is(':checked')) {
									member.privilege = 21
								}
								sharelist.push(member);
							}
							$.ajax({
								type:"POST",
								url:"shareoption/",
								data:JSON.stringify(sharelist),
								success:function(results){
									if (results == "success") {
										$("#popup-share").remove();
                                        					$(".grayScreenClass").remove();
                                        					popup("Successfully share the file!");
                                    				} else if (results == "notfound") {
                                        					popup("File is not found!");
                                    				} else if (results == "notlogin") {
                                        					popup("You have not logged in!");
                                    				}
								}
                                
							});
						}
					}
        			t = setTimeout(function() {
					$("#popup").remove();
					window.location.reload();
				},2000)
				});

			}
		});
        	t = setTimeout(function() {
			$("#popup").remove();
		},2000)
		return false;
	});

	$(document).on('click','.extract', function(){
		// retrieve file from MD5 and SHA1 codes
    		var md5code = $(".md5").val();
		var sha1code = $(".sha1").val();
		if (md5code.length > 0 && sha1code.length > 0){
        		$.ajax({
				type: "POST",
				url: "extractfile/",
				data: JSON.stringify({"md5": md5code, "sha1":sha1code}),
				dataType: 'json',
				success:function(results){
					var json = eval(results);
					if (json[0] == "notfound"){
			    			popup("No file is found, please check MD5 and SHA1!");
					} else if (json[0] == "notvalid"){
			    			popup("MD5 or SHA1 is not valid!");
					} else if (json[0] == "exist") {
			    			popup("File already in Shared Files!");
					} else if (json[0] == "owner") {
			    			popup("File already in My Files!");
					} else if (json[0] == "notlogin") {
			    			popup("You have not logged in!")
					} else if (json[0] == "restricted") {
			    			popup("Sorry, you cannot get access to the file!");
					} else {
						popup("1 file found!");
						var i = $('.reference2 tr').length;

						$("<tr/>").attr("class", "list_"+i.toString()).appendTo(".reference2 tbody");
                                		$("<td/>").attr({
                                    		class: "first_"+i.toString()+" "+"viewfile",
                                    		id: json[0].fileAlias
                                		}).html("<a class=\"first\" href=\"#\">"+json[0].fileAlias+"</a>").appendTo(".reference2 .list_"+i.toString());			
                                		$("<td/>").attr({
                                    		class: "second_"+i.toString(),
                                    		id: json[0].owner
                                		}).html(json[0].owner).appendTo(".reference2 .list_"+i.toString());

						if (json[0].privilege == "12" || json[0].privilege == "22") {
                                    		json[0].privilege = "Edit/View";
                                    		var contentstr = "<div id=\"zone-bar\"><ul><li class=\"action-bar\"><a href=\"#\"><span><h1>Action &nbsp;</h1><em class=\"opener-world\">" +
                                    		"<img src=\"static/img/downarrow.png\" alt=\"dropdown\" /></em></span></a><ul><li><a href=\"#\" class=\""+i.toString()+
                                    		"\" id=\"editfile\">Edit</a></li><li><a href=\"#\" class=\""+i.toString()+"\" id=\"deletefile\">Delete</a></li>" +
                                    		"<li><a href=\"#\" class=\""+i.toString()+"\" id=\"sharefile\">Share</a></li><li><a href=\"#\" class=\""+i.toString()+
                                    		"\" id=\"renamefile\">Rename</a></li><li><a href=\"#\" class=\""+i.toString()+"\" id=\"appendfile\">Copy</a></li></ul></li></ul></div>";
                                		} else {
                                    		json[0].privilege = "View";
                                    		var contentstr = "<div id=\"zone-bar\"><ul><li class=\"action-bar\"><a href=\"#\"><span><h1>Action &nbsp;</h1><em class=\"opener-world\">" +
                                    		"<img src=\"static/img/downarrow.png\" alt=\"dropdown\" /></em></span></a><ul><li><a href=\"#\" class=\""+i.toString()+"\" id=\"deletefile\">Delete</a></li>" +
                                    		"<li><a href=\"#\" class=\""+i.toString()+"\" id=\"renamefile\">Rename</a></li><li><a href=\"#\" class=\""+i.toString()+"\" id=\"appendfile\">Copy</a></li></ul></li></ul></div>";
                                		}

                                		$("<td/>").attr({
                                    		class: "third_"+i.toString(),
                                    		id: json[0].privilege
                                		}).html(json[0].privilege).appendTo(".reference2 .list_"+i.toString());
                                
                                		$("<td/>").html(contentstr).appendTo(".reference2 .list_"+i.toString());
					}			
				}
			});
		} else {
	    		popup("MD5 or SHA1 cannot be empty!")
		}
		t = setTimeout(function() {
			$("#popup").remove();
		},2000)
		return false;
	});

	$(document).on('click','.create', function(){
		popup_create();
		$(".create2").click(function(){

			var newname = $(".createname").val();
			if (newname == ""){
				$(".createname").css("border", "2px solid #FF0000");
				$(".createinfo").html("File name cannot be empty.");							
			} else {
				$.ajax({
					type: "POST",
					url: "createexist/",
					data: JSON.stringify({"fn":newname}),
					dataType: 'json',
					success:function(json){
						results = eval(json);
						if (results[0] == "success"){
							$(".createname").css("border", "");
							$(".createinfo").html("");
							$.ajax({
								type: "POST",
								url: "createfile/",
								data: JSON.stringify({"fn":newname}),
								dataType: 'json',
								success:function(json){
									results = eval(json);
									if (results == "exist"){
										$(".createname").css("border", "2px solid #FF0000");
										$(".createinfo").html("File name already exists.");
									} else if (results == "notvalid"){
										$(".createname").css("border", "2px solid #FF0000");
										$(".createinfo").html("File name is not valid.");
									} else if (results == "notlogin") {
										popup("You have not logged in!");	
									} else {
                                        $("#popup-create").remove();
                                        $(".grayScreenClass").remove();
						window.location.reload();
/*										var i = $('.reference tr').length;

                                        $("<tr/>").attr("class", "list_"+i.toString()).appendTo(".reference tbody");
                                        $("<td/>").attr({
                                            class: "first_"+i.toString()+" "+"viewfile",
                                            id: results.filename
                                        }).html("<a class=\"first\" href=\"#\">"+results.filename+"</a>").appendTo(".reference .list_"+i.toString());			
                                        $("<td/>").attr({
                                            class: "second_"+i.toString(),
                                            id: results.createon
                                        }).html(results.createon).appendTo(".reference .list_"+i.toString());
                                        $("<td/>").attr({
                                            class: "third_"+i.toString(),
                                            id: results.updateon
                                        }).html(results.updateon).appendTo(".reference .list_"+i.toString());
                                        var contentstr = "<div id=\"zone-bar\"><ul><li class=\"action-bar\"><a href=\"#\"><span><h1>Action &nbsp;</h1><em class=\"opener-world\">" +
                                        "<img src=\"static/img/downarrow.png\" alt=\"dropdown\" /></em></span></a><ul><li><a href=\"#\" class=\""+i.toString()+
                                        "\" id=\"editfile\">Edit</a></li><li><a href=\"#\" class=\""+i.toString()+"\" id=\"deletefile\">Delete</a></li>" +
                                        "<li><a href=\"#\" class=\""+i.toString()+"\" id=\"sharefile\">Share</a></li><li><a href=\"#\" class=\""+i.toString()+
                                        "\" id=\"renamefile\">Rename</a></li><li><a href=\"#\" class=\""+i.toString()+"\" id=\"appendfile\">Copy</a></li></ul></li></ul></div>";
                                        $("<td/>").html(contentstr).appendTo(".reference .list_"+i.toString());
*/
                                    }
                                }
							});
							
						} else {
							if (results[0] == "exist"){
								$(".createname").css("border", "2px solid #FF0000");
								$(".createinfo").html("File name already exists.");
							} else if (results[0] == "notvalid"){
								$(".createname").css("border", "2px solid #FF0000");
								$(".createinfo").html("File name is not valid.");
							} else if (results[0] == "notlogin") {
								popup("You have not logged in!");	
							}
						}	
					}
				});
			}
		});
		return false;
	});

	// rename file
	$(document).on('click','#renamefile', function(){
		var class_id = this.className;
        	if ($(this).closest('table').attr("id") == "mytable"){
			var fileName = $(".reference .first_"+class_id).attr("id");
        	} else if ($(this).closest('table').attr("id") == "mytable2"){
			var fileName = $(".reference2 .first_"+class_id).attr("id");
        	}
		var tableName = $(this).closest('table').attr("id");
		popup_rename(fileName, class_id, tableName);
		return false;
	
	});
	$(document).on('click', '.rename', function(){

		var class_id = $(".popup-form .newname").attr("id");
        	if ($(".popup-form .newname").attr("Tname") == "mytable"){
            		var ownerName = "self"
        	} else if ($(".popup-form .newname").attr("Tname") == "mytable2"){
            		var ownerName = $(".reference2 .second_"+class_id).attr("id");
        	}
		var oldName = $(".popup-form .newname").attr("name");
		var newName = $(" .popup-form .newname").val();

		var newname = $(".newname").val();
		if (newname == ""){
			$(".newname").css("border", "2px solid #FF0000");
			$(".renameinfo").html("File name cannot be empty.");							
		} else {
			$.ajax({
				type: "POST",
				url: "renameexist/",
				data: JSON.stringify({"fn":newname, "owner":ownerName}),
				dataType: 'json',
				success:function(json){
					results = eval(json);
					if (results[0] == "success"){
						$(".newname").css("border", "");
						$(".renameinfo").html("");
						$.ajax({
							type: "POST",
							url: "renamefile/",
							data:JSON.stringify({"oldname":oldName, "newname":newName, "owner": ownerName}),
							dataType:'json',
							success:function(json){

								results2 = eval(json);
								if( results2[0] == "success"){

									if (ownerName == "self"){

										$(".reference .first_"+class_id).attr("id", newName);
										$(".reference .first_"+class_id + " .first").html(newName);
									} else {
										$(".reference2 .first_"+class_id).attr("id", newName);
										$(".reference2 .first_"+class_id + " .first").html(newName);
									}
									t = setTimeout(function() {
										$("#popup-rename").remove();
										$(".grayScreenClass").remove();
									},1000)
								} else if (results2[0] == "exist") {
									$(".newname").css("border", "2px solid #FF0000");
									$(".renameinfo").html("File name already exists.");
								} else if (results2[0] == "notvalid") {
									$(".newname").css("border", "2px solid #FF0000");
									$(".renameinfo").html("File name is not valid.");								
								}

							}
						});
					} else {
						if (results[0] == "exist"){
							$(".newname").css("border", "2px solid #FF0000");
							$(".renameinfo").html("File name already exists.");
						} else if (results[0] == "notvalid"){
							$(".newname").css("border", "2px solid #FF0000");
							$(".renameinfo").html("File name is not valid.");
						} else if (results[0] == "notlogin") {
							popup("You have not logged in!");	
						}
					}	
				}
			});
		}
		t = setTimeout(function() {
			$("#popup").remove();
		},1000)
	});
	

	$(document).on('click','#appendfile', function(){
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
			url:"appendfile/",
			data: JSON.stringify({"filename":fileName, "owner":ownerName}),
			dataType: 'json',
			success:function(json){
				var results = eval(json);
				if (results[0] == 'success'){
					window.location.reload();
				} else if (results[0] == 'exist'){
					popup("This shouldn't be happening, but the file exists already.");
				} else if (results[0] == 'notlogin'){
					popup("You have not logged in!");
				}
			}
		});
		t = setTimeout(function() {
			$("#popup").remove();
		},2000)
		return false;
	});
});