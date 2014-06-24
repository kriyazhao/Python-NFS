$(document).ready(function(){
	;(function($){
	    $.fn.extend({
	        donetyping: function(callback,timeout){
	            timeout = timeout || 1e3; // 1 second default timeout
	            var timeoutReference,
	                doneTyping = function(el){
	                    if (!timeoutReference) return;
	                    timeoutReference = null;
	                    callback.call(el);
	                };
	                return this.each(function(i,el){
	                var $el = $(el);
	                $el.is('.jqte_editor') && $el.keypress(function(){
	                    if (timeoutReference) clearTimeout(timeoutReference);
	                    timeoutReference = setTimeout(function(){
	                        doneTyping(el);
	                    }, timeout);
	                }).blur(function(){
	                    doneTyping(el);
	                });
	            });
	        }
	    });
	})(jQuery);
});



