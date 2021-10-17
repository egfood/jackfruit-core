$(document).ready(function () {
    let csrf = $('#jbasket-container-js').attr('data-csrf');

    $(".vegFrameMenu").click(function () {
        $(this).siblings(".vegFrameDropMenu").fadeIn(200);
    });

    $('#jproductcategory-filter-js').change(function () {
        window.location = $(this).val();
    });

    $('.jorder-item-in-backet-js').on('click', function () {
        let order_item_api_url = $(this).attr('data-product-api'),
            order_item_container = $(this).closest('.jorder-item-container-js'),
            in_basket_button = $(this).closest('.inBasket'),
            is_order_item_exists_in_cart = in_basket_button.hasClass('active'),
            is_send_api_request = false;

        if (is_order_item_exists_in_cart === true && is_send_api_request === false) {
            is_send_api_request = true;
            $.ajax({
                url: order_item_api_url,
                type: "DELETE",
                headers: {'X-CSRFToken': csrf},
                processData: false,
                contentType: false,
            })
                .done(function (result) {
                    in_basket_button.toggleClass('active');
                    $('.jmessage-removed-js', order_item_container).finish().fadeIn(100).delay(2000).fadeOut(1000);
                    is_send_api_request = false;
                })
                .fail(function (result) {
                    window.alert('DELTE request error! <Need toast message!>');
                    is_send_api_request = false;
                });
        } else if (is_order_item_exists_in_cart === false && is_send_api_request === false) {
            let form_data = new FormData(),
                input_value = $('.number input', order_item_container).val();

            if (input_value !== undefined) {
                form_data.append("value", input_value);
                is_send_api_request = true;
                $.ajax({
                    url: order_item_api_url,
                    type: "PUT",
                    headers: {'X-CSRFToken': csrf},
                    data: form_data,
                    processData: false,
                    contentType: false,
                })
                    .done(function (result) {
                        in_basket_button.toggleClass('active');
                        $('.jmessage-added-js', order_item_container).finish().fadeIn(100).delay(2000).fadeOut(1000);
                        is_send_api_request = false;
                    })
                    .fail(function (result) {
                        window.alert('PUT request error! <Need toast message!>');
                        is_send_api_request = false;
                    });
            } else {
                window.alert('Order item value of input is undefined! <Need toast message!>');
            }
        }
    });

});
