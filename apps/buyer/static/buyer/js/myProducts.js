$(document).ready(function () {
    let csrf = $('#jbasket-container-js').attr('data-csrf'),
        spinner = $("#jorder-total-widget-js .jspinner-block-js"),
        toast_error = $("#jorder-total-widget-toast-error-js"),
        toast_error_body = $("#jorder-total-widget-toast-error-body-js"),
        is_send_api_request = false;

    $(".vegFrameMenu").click(function () {
        $(this).siblings(".vegFrameDropMenu").fadeIn(200);
    });

    $('#jproductcategory-filter-js').change(function () {
        window.location = $(this).val();
    });

    $('.jproduct-value-input-js').on('change', function () {
        let order_item_api_url = $(this).attr('data-product-api'),
            order_item_container = $(this).closest('.jorder-item-container-js'),
            input_value = $(this).val(),
            in_basket_button = $('.inBasket', order_item_container),
            is_order_item_exists_in_cart = in_basket_button.hasClass('active');

        if (input_value !== undefined && is_order_item_exists_in_cart === true && is_send_api_request === false) {
            let form_data = new FormData();

            is_send_api_request = true;

            form_data.append("value", input_value);
            $.ajax({
                url: order_item_api_url,
                type: "PUT",
                headers: {'X-CSRFToken': csrf},
                data: form_data,
                processData: false,
                contentType: false,
            })
                .done(function (result) {
                    $('.jmessage-update-js', order_item_container).finish().fadeIn(100).delay(2000).fadeOut(1000);
                    update_ui_total(toast_error, toast_error_body, spinner);
                    is_send_api_request = false;
                })
                .fail(function (result) {
                    window.alert('[Update] PUT request error! <Need toast message!>');
                    is_send_api_request = false;
                });
        }
    });

    $('.jorder-item-in-backet-js').on('click', function () {
        let order_item_api_url = $(this).attr('data-product-api'),
            order_item_container = $(this).closest('.jorder-item-container-js'),
            in_basket_button = $(this).closest('.inBasket'),
            is_order_item_exists_in_cart = in_basket_button.hasClass('active');

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
                    update_ui_total(toast_error, toast_error_body, spinner);
                    update_ui_count(toast_error, toast_error_body);
                    is_send_api_request = false;
                })
                .fail(function (result) {
                    window.alert('DELETE request error! <Need toast message!>');
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
                        update_ui_total(toast_error, toast_error_body, spinner);
                        update_ui_count(toast_error, toast_error_body);
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
