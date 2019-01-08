let h0 = $(document.body).height(),
    h1 = $(".logo_wrapper").outerHeight(true),
    h2 = $(".header_nav").outerHeight(true),
    h3 = $(".banner_wrapper").outerHeight(true),
    h4 = $(".footer_wrapper").outerHeight(true),
    h5 = $(".location").outerHeight(true),
    h6 = $(".out_wrapper").css("marginTop").replace('px', ''),
    h7 = $(".content_details").css("marginTop").replace('px', ''),
    height = h0 - h1 - h2 - h3 - h4 - h5 - h6 - h7;
if($(".content_details").innerHeight() <= height) {
    $(".content_details").innerHeight(height);
}
$(window).on("resize", ()=> {
    h0 = $(document.body).height();
    height = h0 - h1 - h2 - h3 - h4 - h5 - h6 - h7;
    if($(".content_details").innerHeight() <= height) {
        $(".content_details").innerHeight(height);
    }
})