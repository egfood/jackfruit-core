(function ($, window) {
    $.fn.replaceLocations = function (locations) {
        var self, $option;

        this.empty();
        self = this;

        $.each(locations, function (index, loc) {
            let item = "<p class='pb-2'><i class='fas fa-map-marked-alt text-success'></i> " + loc.full_address + "</p>";
            self.append(item);
        });
    };
})(jQuery, window);


function update_profile_locations(spinner, locations_block, toast_error, toast_error_body) {
    let is_send_request_to_update_location = false;

    if (is_send_request_to_update_location === false) {
        spinner.show();
        is_send_request_to_update_location = true;

        $.ajax({
            url: locations_block.attr("data-api-locations-list-url"),
            type: "GET"
        })
            .done(function (result) {
                is_send_request_to_update_location = false;
                locations_block.replaceLocations(result);
                spinner.hide();
            })
            .fail(function (result) {
                toast_error_body.text(result);
                let toast = new bootstrap.Toast(toast_error);
                is_send_request_to_update_location = false;
                spinner.hide();
                toast.show();
            });
    }
}

$(document).ready(function () {

    let overlay_with_spinner = $("#jmodal-spinner-block"),
        profile_form = $("#jbuyer-profile-form"),
        profile_tab_container = profile_form.closest(".jprofile-tab-content-js"),
        profile_form_inputs = $(":input", profile_form),
        profile_form_buttons = $('.formButtons button', profile_form),
        profile_form_submit_button = $('#jsubmit-js'),
        profile_form_submit_button_spinner = $('#jsubmit-spinner', profile_form_submit_button),
        profile_form_csrf = $("[name='csrfmiddlewaretoken']", profile_form).val(),
        toast_success = $('#jprofile-toast-updated'),
        toast_error = $('#jprofile-toast-error'),
        toast_error_body = $("#jprofile-toast-error-body", toast_error),
        profile_api_url = profile_form.attr('data-api-url'),
        profile_images = $('.jimg-updated-on-upload-new-js');

    profile_form_inputs.on('change', function () {
        profile_tab_container.addClass('jform-changed');
    });

    $("#jprofileHeader").on('click', function () {
        let wi = profile_tab_container;
        load_profile_form_data(
            overlay_with_spinner, profile_api_url, profile_form, toast_error_body, toast_error, wi, profile_images
        );
    });

    profile_form_submit_button.on('click', function (e) {
        e.preventDefault();
        let wi = profile_tab_container;
        save_profile_form(
            profile_form, profile_form_csrf, profile_form_buttons, profile_form_submit_button_spinner, profile_api_url,
            toast_success, toast_error, toast_error_body, wi, profile_images
        );
    });


});