$(document).ready(function () {
    let order_modal_wrapper = $('#jorder-js'),
        order_form = $("#jform-send-order-js", order_modal_wrapper),
        contact_form_reset = $('#jlocation-btn-reset-js', order_modal_wrapper),
        contact_form = $("#jlocation-add-from-js", order_modal_wrapper),
        send_order_popup = $("#jpopup-send-order-js"),
        toast_error = $("#jorder-creation-toast-error-js"),
        toast_error_body = $("#jorder-creation-toast-error-body-js", toast_error),
        toast_page_success = $("#jorder-page-toast-successfully-js"),
        toast_page_success_body = $("#jorder-page-toast-body-successfully-js", toast_page_success),
        toast_page_error = $("#jorder-page-toast-error-js"),
        toast_page_error_body = $("#jorder-page-toast-error-body-js", toast_page_error),
        toast_update_order_item_error = $("#jorder-item-update-toast-error-js"),
        toast_update_order_item_error_body = $("#jorder-item-update-toast-error-body-js", toast_update_order_item_error),
        toast_update_order_item_success = $("#jorder-item-update-toast-successfully-js"),
        order_total = $("#jorder-total-js"),
        order_total_spinner = $(".jspinner-block-js", order_total),
        spinner_block = $("#jmodal-spinner-block"),
        is_send_request_to_update_order = false,
        is_send_request_to_update_order_item = false,
        is_send_request_to_delete_order_item = false,
        order_total_text_items = $(".jorder-total-text-js"),
        order_item_table = $("#jorder-item-table-js"),
        spinner = $("#jorder-total-widget-js .jspinner-block-js"),
        delivery_cost_text = $("#jorder-delivery-cost-text-js", order_form),
        total_cost_text = $("#jorder-total-cost-text-js", order_form),
        order_item_table_csrf = order_item_table.attr("data-csrf");


    function order_table_updating_is_failed(result, spinners) {
        toast_update_order_item_error_body.text(result.responseText);
        let toast = new bootstrap.Toast(toast_update_order_item_error);
        is_send_request_to_update_order_item = false;
        toast.show();
        spinners.removeClass('visible').addClass('invisible');
    }

    function update_costs_by_location(){

    }

    contact_form_reset.on('click', function () {
        contact_form.fadeOut(200);
        send_order_popup.css("display", "flex");
        update_costs_by_location();
    });

    $("#jbtn-send-order").on('click', function () {
        update_order_locations(spinner_block, order_form, toast_error, toast_error_body);
    });

    $("#jorder-form-submit-js").on('click', function () {
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

    $(".jorder-item-js").on('change', function () {

        if (is_send_request_to_update_order_item === false) {
            let order_item_input = $(this),
                order_item_spinner = order_item_input.closest('tr').find('.jspinner-block-js'),
                spinners = order_item_spinner.add(order_total_spinner),
                form_data = new FormData();

            spinners.removeClass('invisible').addClass('visible');
            is_send_request_to_update_order_item = true;
            form_data.append("value", order_item_input.val());

            $.ajax({
                url: order_item_input.attr("data-order-item-api-url"),
                type: "PATCH",
                headers: {'X-CSRFToken': order_item_table_csrf},
                data: form_data,
                processData: false,
                contentType: false,
            })
                .done(function (result) {
                    is_send_request_to_update_order_item = false;
                    order_item_input.closest('tr').find('.jorder-item-total-js').text(result.item_total);
                    update_ui_total(toast_error, toast_error_body, spinner_block)

                    $.ajax({
                        url: order_item_table.attr("data-api-order-url"),
                        type: "GET"
                    })
                        .done(function (result) {
                            order_total_text_items.text(result.total_cost);
                            let toast = new bootstrap.Toast(toast_update_order_item_success);
                            toast.show();
                            spinners.removeClass('visible').addClass('invisible');
                        })
                        .fail(function (result) {
                            order_table_updating_is_failed(result, spinners);
                        });

                })
                .fail(function (result) {
                    order_table_updating_is_failed(result, spinners);
                });
        }

    });


    $(".jorder-item-del-js").on("click", function () {

        if (is_send_request_to_delete_order_item === false) {
            let order_item = $(this).closest("tr");
            is_send_request_to_delete_order_item = true;
            $.ajax({
                url: order_item.find(".jorder-item-js").attr("data-order-item-api-url"),
                type: "DELETE",
                headers: {'X-CSRFToken': order_item_table_csrf},
                processData: false,
                contentType: false,
            })
                .done(function (result) {
                    update_ui_total(toast_update_order_item_error, toast_update_order_item_error_body, spinner);
                    update_ui_count(toast_update_order_item_error, toast_update_order_item_error_body);
                    order_item.remove();

                    $.ajax({
                        url: order_item_table.attr("data-api-order-url"),
                        type: "GET"
                    })
                        .done(function (result) {
                            order_total_text_items.text(result.total_cost);
                            let toast = new bootstrap.Toast(toast_update_order_item_success);
                            toast.show();
                            spinners.removeClass('visible').addClass('invisible');
                        })
                        .fail(function (result) {
                            order_table_updating_is_failed(result, spinners);
                        });

                    toast_page_success_body.text("Товар из вашей корзины успешно удален.")
                    let toast = new bootstrap.Toast(toast_page_success);
                    toast.show();
                    is_send_request_to_delete_order_item = false;
                })
                .fail(function (result) {
                    toast_page_error_body.text(
                        "Упс! Что-то пошло не так. Мы не смогли удалить товар из вашей корзины. " +
                        "Перезагрузите страницу и попробуйте снова."
                    );
                    let toast = new bootstrap.Toast(toast_page_error);
                    toast.show();
                    is_send_request_to_delete_order_item = false;
                });
        }
    });

    $("#id_location", order_form).on("change", function() {
        let form = new FormData(order_form[0]);

        if (is_send_request_to_update_order === false && form.location !== "-1") {
            form.set("state", "created");
            is_send_request_to_update_order = true;

            $.ajax({
                url: order_form.attr("data-api-order-update-url"),
                type: "PATCH",
                headers: {'X-CSRFToken': order_form.attr('data-csrf')},
                data: form,
                processData: false,
                contentType: false,
            })
                .done(function (result) {
                    is_send_request_to_update_order = false;
                    delivery_cost_text.text(result.delivery_cost);
                    total_cost_text.text(result.total_cost);
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