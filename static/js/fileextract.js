$(document).on('click','.extract', function(){
    // retrieve file from MD5 and SHA1 codes
    var md5code = $(".md5").val();
	var sha1code = $(".sha1").val();
	if (md5code.length > 0 && sha1code.length > 0){
        $.ajax({
		type: "POST",
		url: "/extractfile",
		data: JSON.stringify({"md5": md5code, "sha1":sha1code}),
		dataType: 'json',
		success:function(results){
			var json = eval(results);
			if (json[0] == ""){
			    popup("No file is found, please check MD5 and SHA1!")
			} else {
				popup("1 file found!");
				var contentstr = "<tr><td class=\"first_9999\" id=\""+json.filename+"\">"+ json.filename +"</td>";
				contentstr += "<td class=\"second_9999\" id=\""+json.createon+"\">"+ json.createon +"</td>";
				contentstr += "<td class=\"third_9999\" id=\""+json.updateon+"\">"+ json.updateon +"</td>";
				contentstr += "<td><div id=\"zone-bar\"><ul><li><a href=\"#\"><span><h1>Action &nbsp;</h1><em class=\"opener-world\">" +
				"<img src=\"static/img/downarrow.png\" alt=\"dropdown\" /></em></span></a><ul><li><a href=\"#\" class=\"9999\"" +
				"id=\"viewfile\">view</a></li></ul></li></ul></div></td></tr>";
				$(contentstr).appendTo("tbody");			
			}			
		}
		});
    } else {
	    popup("MD5 or SHA1 cannot be empty!")
    }
});
