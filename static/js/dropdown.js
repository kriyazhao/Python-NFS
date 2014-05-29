$(document).on('click', '#zone-bar li em', function(){
    var hidden = $(this).parents("li").children("ul").is(":hidden");
    $("#zone-bar>ul>li>ul").hide();        
    $("#zone-bar>ul>li>a").removeClass();
    if (hidden) {
        $(this)
        .parents("li").children("ul").toggle()
        .parents("li").children("a").addClass("zoneCur");
    } 
    return false;
});

$(document).on('click', '#zone-bar li ul a', function(){
    $("#zone-bar>ul>li>ul").hide();        
    $("#zone-bar>ul>li>a").removeClass(); 
    return false;
});
