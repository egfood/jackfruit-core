(function ($, window) {
    $.fn.replaceOptions = function (options, selected_id) {
        var self, $option;

        this.empty();
        self = this;

        options.unshift({id: -1, short_address: "<Выберите адрес>"})
        if (selected_id === ""){
            selected_id = "-1";
        }

        $.each(options, function (index, option) {
            $option = $("<option></option>")
                .attr("value", option.id)
                .text(option.short_address);
            if (parseInt(selected_id) ===  option.id){
                $option.attr("selected", "");
            }
            self.append($option);
        });
    };
})(jQuery, window);

function update_order_locations(spinner_block, order_form, toast_error, toast_error_body) {
    let is_send_request_to_update_location = false;

    if (is_send_request_to_update_location === false) {
        spinner_block.show();
        is_send_request_to_update_location = true;

        $.ajax({
            url: order_form.attr("data-api-locations-list-url"), type: "GET"
        })
            .done(function (result) {
                is_send_request_to_update_location = false;
                $("#id_location", order_form).replaceOptions(result, order_form.attr("data-selected-location-id"));
                spinner_block.hide();
            })
            .fail(function (result) {
                toast_error_body.text(result);
                let toast = new bootstrap.Toast(toast_error);
                is_send_request_to_update_location = false;
                spinner_block.hide();
                toast.show();
            });
    }
}

function update_ui_total(toast_error, toast_error_body, spinner_block) {
    let is_send_request_to_update_total = false,
        widget = $("#jorder-total-widget-js");
    if (is_send_request_to_update_total === false) {
        spinner_block.show();
        is_send_request_to_update_total = true;

        $.ajax({
            url: widget.attr("data-api-order-total-url"), type: "GET"
        })
            .done(function (result) {
                is_send_request_to_update_total = false;
                $(".jorder-total-widget-value-js", widget).text(result);
                spinner_block.hide();
            })
            .fail(function (result) {
                toast_error_body.text(
                    "Упс! Что-то пошло не так. Мы не смогли обновить сумму вашей корзины в виджете. " +
                    "Попробуйте перезагрузить страницу."
                );
                let toast = new bootstrap.Toast(toast_error);
                is_send_request_to_update_total = false;
                spinner_block.hide();
                toast.show();
            });
    }
}

function update_ui_count(toast_error, toast_error_body) {
    let is_send_request_to_update_total_count = false,
        widget = $("#jorder-total-count-widget-js");
    if (is_send_request_to_update_total_count === false) {
        is_send_request_to_update_total_count = true;

        $.ajax({
            url: widget.attr("data-api-order-total-count-url"), type: "GET"
        })
            .done(function (result) {
                is_send_request_to_update_total_count = false;
                widget.text(result);
            })
            .fail(function (result) {
                toast_error_body.text(
                    "Упс! Что-то пошло не так. Мы не смогли обновить количество товаров корзины в виджете меню. " +
                    "Попробуйте перезагрузить страницу."
                );
                let toast = new bootstrap.Toast(toast_error);
                is_send_request_to_update_total_count = false;
                toast.show();
            });
    }
}