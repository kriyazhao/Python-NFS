$(document).on('click','.logout', function(){
	$.ajax({
		type: "GET",
		url: "/logout",
		dataType: 'json',
		success:function(json){
			results = eval(json)
			if(results['r'] == "logout"){
				popup("log out successfully!");
			}
		}
	});
	setTimeout(function(){
		window.location.reload();
	}, 3000);
});
