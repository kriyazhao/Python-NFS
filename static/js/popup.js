function popup(msg,timer) {
	var 
	h = $(document).scrollTop() +$(window).height() ;
	w = $(window).width();
	lw = Math.floor(w/2-200/2);
	var ht = 
	'<div id="popup" style="display:none;position:absolute;top:100%;left:'+
	lw+
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
		},timer? parseInt(timer):5500)
	});
	
}