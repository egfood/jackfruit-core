$(document).ready(function () {
    let order_modal_wrapper = $('#jorder-js'),
        contact_form_reset = $('#jlocation-btn-reset-js', order_modal_wrapper),
        contact_form = $("#jlocation-add-from-js", order_modal_wrapper),
        send_order_popup = $("#jpopup-send-order-js");


    contact_form_reset.on('click', function () {
        contact_form.fadeOut(200);
        send_order_popup.css("display", "flex");
    });

});