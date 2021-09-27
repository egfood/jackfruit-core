$(document).ready(function () {
    $(".vegFrameMenu").click(function () {
        $(this).siblings(".vegFrameDropMenu").fadeIn(200);
    });

    $(".inBasket").click(function () {
        $(this).toggleClass("active");
        if ($(this).hasClass('active')) {
            $(this).siblings(".basketMessage").finish().fadeIn(100).delay(2000).fadeOut(1000);
        } else {
            $(this).siblings('.basketMessage2').finish().fadeIn(100).delay(2000).fadeOut(1000);
        }
    });

    $('#jproductcategory-filter-js').change(function () {
        window.location = $(this).val();
    });

});
