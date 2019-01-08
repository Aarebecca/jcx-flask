
$(".header_nav").find("li").mouseenter(function(){
    let sub_menue = $(this).find(".sub_menue");
    if(sub_menue) {
        sub_menue.stop().slideDown(150)
    }
})
$(".header_nav").find("li").mouseleave(function(){
    let sub_menue = $(this).find(".sub_menue");
    if(sub_menue) {
        sub_menue.stop().slideUp(150)
    }
})