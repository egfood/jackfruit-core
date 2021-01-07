$(document).ready(function () {
    $(".addProduct, .addPruductsButtonPlus").click(function () {
        $(".mainWrap").css("filter", "blur(5px)");
        $(".popupWindow").fadeIn(200);
        $(".mainWrapOpacity").css("display", "block");
    });

    $("#popupForm").submit(function (event) {
        event.preventDefault();
    })

    $("#popupForm").submit(function (event) {
        event.preventDefault();
        $(".popupWindow").fadeOut(200);
        $(".recievedWindow").fadeIn(200);
        $(".close2").click(function () {
            $(".recievedWindow").fadeOut(200);
            $(".generalWrap").css("filter", "none");
            $(".mainWrapOpacity").css("display", "none");
        })   
    })

    $(document).mouseup(function (e){ 
        var block = $(".vegFrameDropMenu, .profileSettings, .popupWindow, .popupMessengers, .editForm, .icalendar");
        if (!block.is(e.target)
            && block.has(e.target).length === 0) {
            block.hide();
            $(".mainWrap").css("filter", "none");
            $(".mainWrapOpacity").css("display", "none");
            $(".popup").css("opacity", "1");
            $(".popupBg").css("display", "none");
        }
    });


    $(".profileHeader").click(function () {
        $(".mainWrap").css("filter", "blur(5px)");
        $(".mainWrapOpacity").css("display", "block");
        $(".profileSettings").fadeIn(200);
        $(".profileSettings").css("display", "flex");
    });

    $(".calendar").click(function () {
        $(".mainWrap").css("filter", "blur(5px)");
        $(".mainWrapOpacity").css("display", "block");
        $(".popup").css("opacity", ".3");
        $(".popupBg").fadeIn(200)
        $(".icalendar").fadeIn(300);
    });
    
    $(document).mouseup(function (e){ 
        var block = $(".icalendar");
        if (!block.is(e.target)
            && block.has(e.target).length === 0) {
            block.hide();
        }
        $(".popupBg").css("display", "none");
        $(".popup").css("opacity", "1");
    });

    $(".icalendar__days > div").click(function () {
        $(".icalendar").css("display", "none");
        $(".popupBg").css("display", "none");
        $(".popup").css("opacity", "1");
    })

    $(".close1").click(function () {
        $(".mainWrap").css("filter", "none");
        $(".vegFrameDropMenu").css("display", "none");
        $(".profileSettings").fadeOut(200);
        $(".popupWindow").fadeOut(200);
        $(".mainWrapOpacity").css("display", "none");
        $(".popupMessengers").fadeOut(200);
        $(".editForm").fadeOut(200);
        
    })   


    $(".hideMenu").click(function () {
        $(this).css("display", "none");
        $(".showMenu").css("display", "inline");
        $(".mainContentWrap").toggleClass("maincontentWrapPadding")
        $(".mainMenu").toggleClass("openCloseMenu");
        $(".header").toggleClass("headerPaddingClose");
        $(".burgerAndBasket").toggleClass("burgerAndBasketPadding");
        $(".countOrderedProduct").css("display", "none");
        $(".countOrderedProduct").show(500);
   });
    $(".showMenu").click(function () {
        $(this).css("display", "none");
        $(".hideMenu").css("display", "inline");
        $(".mainContentWrap").toggleClass("maincontentWrapPadding")
        $(".mainMenu").toggleClass("openCloseMenu");
        $(".header").toggleClass("headerPaddingClose");
        $(".burgerAndBasket").removeClass("burgerAndBasketPadding");
    });


    $(".tileDisplaying").click(function () {
        $(this).toggleClass("displayingBoxesActive");
        $(".listDisplaying").removeClass("displayingBoxesActive");  
    })
    $(".listDisplaying").click(function () {
        $(this).toggleClass("displayingBoxesActive");
        $(".tileDisplaying").removeClass("displayingBoxesActive"); 
    })


    $(".burger").click(function (params) {
        $(this).toggleClass("burger_active");
        $(".mainMenu").toggleClass("active");
   });
   
   $(".menuList a").click(function (params) {
        $(".mainMenu").removeClass("active");    
        $(".burger").removeClass("burger_active");
   })

    $(".mainContent").click(function (params) {
        $(".mainMenu").removeClass("active");
        $(".burger").removeClass("burger_active");
    });

    $("#checkAll").click(function() {
        $("input[type=checkbox]").prop("checked", $(this).prop("checked"));
    });
    

    $(".edit").click(function () {
        $(".mainWrap").css("filter", "blur(5px)");
        $(".mainWrapOpacity").css("display", "block");
        $(".editForm").fadeIn(200);
    });


    $(".selfSend").click(function(){
		$(".mainWrap").css("filter", "blur(5px)");
		$(".mainWrapOpacity").css("display", "block");
		$(".popupMessengers").fadeIn(200);
	});


    $("input[type=checkbox]").click(function() {
        if (!$(this).prop("checked")) {
        $("#selectAll").prop("checked", false);
        }
    });


    $(".pageNumber").click(function () {
        $(".pageNumber").removeClass("active");
        $(this).addClass("active");
    });


    $('.minus').click(function () {
        var $input = $(this).parent().find('input');
        var count = parseInt($input.val()) - 1;
        count = count < 1 ? 1 : count;
        $input.val(count);
        $input.change();
        return false;
    });
    $('.plus').click(function () {
        var $input = $(this).parent().find('input');
        $input.val(parseInt($input.val()) + 1);
        $input.change();
        return false;
    });

    $('.vegFrameOptions .fa-shopping-basket').click(function () {
        $(this).toggleClass("active");
    })
})
