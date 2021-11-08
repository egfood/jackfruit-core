$(document).ready(function () {
    let order_modal_wrapper = $('#jorder-js'),
        order_form = $("#jform-send-order-js", order_modal_wrapper),
        contact_form_reset = $('#jlocation-btn-reset-js', order_modal_wrapper),
        contact_form = $("#jlocation-add-from-js", order_modal_wrapper),
        send_order_popup = $("#jpopup-send-order-js"),
        toast_error = $("#jorder-creation-toast-error-js"),
        toast_error_body = $("#jorder-creation-toast-error-body-js", toast_error),
        spinner_block = $("#jmodal-spinner-block"),
        is_send_request_to_update_order = false;


    contact_form_reset.on('click', function () {
        contact_form.fadeOut(200);
        send_order_popup.css("display", "flex");
    });

    $("#jbtn-send-order").on('click', function () {
        update_order_locations(spinner_block, order_form, toast_error, toast_error_body);
    });

    $("#jorder-form-submit-js").on('click', function (){
        if (is_send_request_to_update_order === false) {
            is_send_request_to_update_order = true;

            $.ajax({
                url: order_form.attr("data-api-order-update-url"),
                type: "PATCH",
                headers: {'X-CSRFToken': order_form.attr('data-csrf')},
                data: new FormData(order_form[0]),
                processData: false,
                contentType: false,
            })
                .done(function (result) {
                    is_send_request_to_update_order = false;
                    window.location.reload();
                })
                .fail(function (result) {
                    toast_error_body.text(result.responseText);
                    let toast = new bootstrap.Toast(toast_error);
                    is_send_request_to_update_order = false;
                    toast.show();
                });
        }
    });

});