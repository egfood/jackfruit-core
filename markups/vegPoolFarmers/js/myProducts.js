$(document).ready(function () {
    

    $(".vegFrameMenu").click(function () {
        $(this).siblings(".vegFrameDropMenu").fadeIn(200)
    })

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
