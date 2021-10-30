$(document).ready(function () {
    let is_send_request_to_create_location = false,
        location_form = $("#jlocation-form");

    $('#jlocation-btn-send-js').on('click', function () {
        if (is_send_request_to_create_location === false) {
            is_send_request_to_create_location = true;

            $.ajax({
                url: location_api_url,
                type: "PUT",
                headers: {'X-CSRFToken': location_form.attr('csrf-data')},
                data: new FormData(location_form[0]),
                processData: false,
                contentType: false,
            })
                .done(function (result) {
                    $('.jmessage-update-js', order_item_container).finish().fadeIn(100).delay(2000).fadeOut(1000);
                    is_send_api_request = false;
                })
                .fail(function (result) {
                    window.alert('[Update] PUT request error! <Need toast message!>');
                    is_send_api_request = false;
                });
        }
    });
});