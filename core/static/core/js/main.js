$(document).ready(function () {
    $(".addProduct, .addPruductsButtonPlus").click(function () {
        $("body").css("overflow", "hidden");
        $(".mainWrap").css("filter", "blur(5px)");
        $(".popupWindow").fadeIn(200);
        $(".mainWrapOpacity").css("display", "block");
    });

    $("#jform-send-order-js").submit(function (event) {
        event.preventDefault();
    });

    $("#jform-send-order-js").submit(function (event) {
        event.preventDefault();
        $(".popupWindow").fadeOut(200);
        $(".recievedWindow").fadeIn(200);
        $(".close2").click(function () {
            $(".recievedWindow").fadeOut(200);
            $(".generalWrap").css("filter", "none");
            $(".mainWrapOpacity").css("display", "none");
        });
    });

    $(document).mouseup(function (e){ 
        var block = $(".vegFrameDropMenu, .profileSettings, .popupWindow, .popupMessengers, .editForm, .icalendar, .contactData, .feedbackPopup, .orderSuccess");
        if (!block.is(e.target)
            && block.has(e.target).length === 0) {
            block.hide();
            $("body").css("overflow", "auto");
            $(".mainWrap").css("filter", "none");
            $(".mainWrapOpacity").css("display", "none");
            $(".popup, .profileSettings").css("opacity", "1");
            $(".popupBg").css("display", "none");
        }
    });


    $(".profileSettingsMenu nav a").click(function () {
        $(".profileSettingsMenu nav a").removeClass("profileSettingsMenuActive");
        $(this).addClass("profileSettingsMenuActive");
    })

    $(".profileHeader").click(function () {
        $("body").css("overflow", "hidden");
        $(".mainWrap").css("filter", "blur(5px)");
        $(".mainWrapOpacity").css("display", "block");
        $(".profileSettings").fadeIn(200);
        $(".profileSettings").css("display", "flex");
    });

    $(".calendar").click(function () {
        $("body").css("overflow", "hidden");
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
        $(".vegFrameDropMenu, .mainWrapOpacity").css("display", "none");
        $(".profileSettings, .popupWindow, .popupMessengers, .editForm, .contactData, .feedbackPopup, .orderSuccess").fadeOut(200); 
    });


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
        $("body").css("overflow", "hidden");
        $(".mainWrap").css("filter", "blur(5px)");
        $(".mainWrapOpacity").css("display", "block");
        $(".editForm").fadeIn(200);
    });


    $(".selfSend").click(function(){
        $("body").css("overflow", "hidden");
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
    
    $("#adressSet").click(function () {
        $(".profileInfo").hide();
        $(".adressSettings").fadeIn(400);
        $(".profileSettings h2").html("Мои адреса");

    })
    
    $("#profileInfoSet").click(function () {
        $(".adressSettings").hide();
        $(".profileInfo").fadeIn(400);
        $(".profileSettings h2").html("Мой профиль");
        
    })

    $("#profilePhone, #phoneNumber").inputmask({"mask": "+375(99) 999-99-99"});
    // $(".contactData button[type='reset']").click(function () {
    //     $(".contactData").fadeOut(200);
    //     $(".profileSettings").css("display", "flex");
    //
    // })

    $(".leaveFeedback").click(function () {
        $("body").css("overflow", "hidden");
        $(".mainWrap").css("filter", "blur(5px)");
        $(".mainWrapOpacity").css("display", "block");
        $(".feedbackPopup").fadeIn(200);
    })
    $("#jorder-submit-js").click(function () {
        $(".orderSuccess").css("display", "block");    
    })
})