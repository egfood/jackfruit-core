(function ($, window) {
    $.fn.replaceOptions = function (options) {
        var self, $option;

        this.empty();
        self = this;

        $.each(options, function (index, option) {
            $option = $("<option></option>")
                .attr("value", option.id)
                .text(option.short_address);
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
            url: order_form.attr("data-api-locations-list-url"),
            type: "GET"
        })
            .done(function (result) {
                is_send_request_to_update_location = false;
                $("#id_location", order_form).replaceOptions(result);
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