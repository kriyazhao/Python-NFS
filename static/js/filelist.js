function listFile(){
	$.ajax({
		url: "/listfile",
		success:function(results){
			var json = eval(results);
			if (json[0] == ""){
				strtype = 0;
				$(".filelist").html(headingstr + endingstr1);
			} else if (json[0] == "empty"){			 
				strtype = 1;
				$(".filelist").html(headingstr + endingstr1 + endingstr2);
			} else {
			    contentstr = "";
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
				$(".filelist").html(headingstr + contentstr + endingstr1 + endingstr2);
			}
		}
	});
}