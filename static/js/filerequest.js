// view file content
$(document).on('click','#viewfile', function(){
	var class_id = this.className;
	var fileName = $(".first_"+class_id).attr("id");
	$.ajax({
		type:"GET",
		url:"/manipulatefile",
		data:{"filename":fileName},
		dataType:'text',
		success:function(results){
			$(".editbar").html(fileName);
			$(".filecontent").html('loading');
			$(".filecontent").html(results);
			$(".filecontent").attr("readonly", true);
			$(".filestatus").html("View only");
		}
	});
});

// update file content
$(document).on('click','#editfile', function(){
	var class_id = this.className;
	var fileName = $(".first_"+class_id).attr("id");

	$.ajax({
		type:"GET",
		url:"/manipulatefile",
		data:{"filename":fileName},
		dataType:'text',
		success:function(results){
			$(".editbar").html(fileName);
			$(".filecontent").html('loading');
			$(".filecontent").html(results);
			$(".filecontent").attr("readonly", false);
			$(".filestatus").html("file content will be automatically saved after done typing!");
		}
	});

});

// save file content when done typing
$(document).on('click','.filecontent', function(){
	// sync after done typing text
	$(".filecontent").donetyping(function(){
		var content = $(this).val();
		$(".filestatus").html("saving");
		$.ajax({
			type:"POST",
			url:"/manipulatefile",
			data: JSON.stringify({"filename":$(".editbar").html(), "content": content}),
			dataType: 'text',
			success:function(results){
				if(results == "success"){
					$(".filestatus").html("saved");
				}
				else if(results == "exist"){
					$(".filestatus").html("nothing new happended");
				}
			}
		});
	});
});

// delete file 
$(document).on('click','#deletefile', function(){
	//delete file
	var class_id = this.className;
	var fileName = $(".first_"+class_id).attr("id");
	$.ajax({
		type:"DELETE",
		url:"/manipulatefile",
		data:JSON.stringify({"filename":fileName}),
		dataType: 'text',
		success:function(results){
			if(results == 'success'){
				$(".first_"+class_id).parent('tr').slideUp(1000);
				setTimeout(function(){
					$(".first_"+class_id).parent('tr').remove();
				}, 1000); 
				popup("delete successfully!")
			}
		}
	});
});

$(document).on('click','#file_upload', function(){
	$(this).uploadify({
		'swf': 'static//js//uploadify.swf',
		'cancelImg': 'static//js//uploadify-cancel.png',
		'uploader': '/uploadfile',
		'auto': true,
		'folder': '\temp',
		'multi': false,
		'fileSizeLimit': 1024*5+'KB',
		'fileTypeDesc': 'Upload Files (.TXT)',
		'fileTypeExts': '*.txt'
	});
});

//delete file 
$(document).on('click','#sharefile', function(){
	//delete file
	var class_id = this.className;
	var fileName = $(".first_"+class_id).attr("id");
	$.ajax({
		type:"POST",
		url:"/sharefile",
		data:JSON.stringify({"filename":fileName}),
		dataType: 'json',
		success:function(json){
			var results = eval(json)
			popup('MD5:'+results.md5+'  SHA1:'+results.sha1)
		}
	});
});
