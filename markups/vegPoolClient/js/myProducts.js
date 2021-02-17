$(document).ready(function () {
    

    $(".vegFrameMenu").click(function () {
        $(this).siblings(".vegFrameDropMenu").fadeIn(200)
    })
    
    $(".inBasket").click(function () {
        $(this).toggleClass("active");
        if ($(this).hasClass('active')) {
            $(this).siblings(".basketMessage").finish().fadeIn(100).delay(2000).fadeOut(1000);
        } else {
            $(this).siblings('.basketMessage2').finish().fadeIn(100).delay(2000).fadeOut(1000);
        }
    });
  

    // $(".tileDisplaying").click(function () {
    //     $(this).toggleClass("displayingBoxesActive")
    //     $(".listDisplaying").removeClass("displayingBoxesActive")  
    // })
    // $(".listDisplaying").click(function () {
    //     $(this).toggleClass("displayingBoxesActive")
    //     $(".tileDisplaying").removeClass("displayingBoxesActive")  
    // })

    // $(".listDisplaying").click(function () {
    //     $(".productContainer").css("display", "none")
    //     $(".table").fadeIn(300)
    //     $(this).toggleClass("displayingBoxesActive")
    //     $(".tileDisplaying").removeClass("displayingBoxesActive")

    // })
    // $(".tileDisplaying").click(function () {
    //     $(".table").css("display", "none")
    //     $(".productContainer").fadeIn(300)
    //     $(this).toggleClass("displayingBoxesActive")
    //     $(".listDisplaying").removeClass("displayingBoxesActive")

    // })
})
