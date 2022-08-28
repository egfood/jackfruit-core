$(document).ready(function () {
    let is_send_request_to_create_location = false,
        location_form = $("#jlocation-form-js"),
        location_popup = $("#jpopup-location-add-js"),
        btn_create_location = $("#jlocation-btn-send-js"),
        toast_error = $("#jlocation-creation-toast-error-js"),
        toast_error_body = $("#jlocation-creation-toast-error-body-js"),
        order_form = $("#jform-send-order-js"),
        order_toast_error = $("#jorder-creation-toast-error-js"),
        order_toast_error_body = $("#jorder-creation-toast-error-body-js", toast_error),
        spinner_block = $("#jmodal-spinner-block"),
        profile_toast_error = $('#jprofile-toast-error'),
        profile_toast_error_body = $("#jprofile-toast-error-body", toast_error),
        locations_block = $("#jprofile-locations-js");

    $(".jshow-add-location-js").click(function () {
        let parent_popup = $(this).closest('.jinitiator-of-add-location-js');
        $("#jpopup-location-add-js").fadeIn(400);
        parent_popup.css("display", "none");
        btn_create_location.attr('data-parent-popup', parent_popup.attr("class"));
    });

    btn_create_location.on('click', function () {
        // I don't know why $(this).attr("id") is undefined?!?! The workaround was needed
        let parent_popup = $("." + $(this).attr('data-parent-popup').split(" ").join("."));

        if (is_send_request_to_create_location === false) {
            is_send_request_to_create_location = true;

            $.ajax({
                url: location_form.attr("data-location-api-url"),
                type: "POST",
                headers: {'X-CSRFToken': location_form.attr('data-csrf')},
                data: new FormData(location_form[0]),
                processData: false,
                contentType: false,
                success: function (result) {
                    update_order_locations(spinner_block, order_form, order_toast_error, order_toast_error_body);
                    update_profile_locations(
                        spinner_block, locations_block, profile_toast_error, profile_toast_error_body
                    );
                    is_send_request_to_create_location = false;
                    parent_popup.fadeIn(400);
                    location_popup.css("display", "none");
                },
                error: function (result) {
                    toast_error_body.text(result.responseText);
                    let toast = new bootstrap.Toast(toast_error);
                    is_send_request_to_create_location = false;
                    toast.show();
                }
            })

        }
    });

});