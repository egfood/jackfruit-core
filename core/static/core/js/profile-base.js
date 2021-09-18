function load_profile_form_data(overlay_with_spinner, profile_api_url, profile_form, toast_error_body, toast_error,
                                wrapper_instance, profile_images) {
    'use strict';
    overlay_with_spinner.show();
    $.get({url: profile_api_url})
        .done(function (result) {
            $.each(result, function (key, value) {
                if (key === 'photo') {
                    profile_images.attr('src', value);
                } else {
                    $('[name="' + key + '"]', profile_form).val(value);
                }
            });
            overlay_with_spinner.hide();
            wrapper_instance.removeClass('jform-changed');
        })
        .fail(function (result) {
            overlay_with_spinner.hide();
            toast_error_body.text("Ошибка при попытке загрузки профиля!");
            let error_alert = new bootstrap.Toast(toast_error);
            error_alert.show();
        });
}

function save_profile_form(profile_form, profile_form_csrf, profile_form_buttons, profile_form_submit_button_spinner,
                           profile_api_url, toast_success, toast_error, toast_error_body, wrapper_instance,
                           profile_images) {
    'use strict';
    profile_form_buttons.attr('disabled', 'disabled');
    profile_form_submit_button_spinner.removeClass('d-none');

    $.ajax({
        url: profile_api_url,
        type: "PUT",
        data: new FormData(profile_form[0]),
        headers: {'X-CSRFToken': profile_form_csrf},
        processData: false,
        contentType: false,
    })
        .done(function (result) {
            reset_buttons_on_submit(profile_form_buttons, profile_form_submit_button_spinner);
            wrapper_instance.removeClass('jform-changed');
            if (result.photo) {
                profile_images.attr('src', result.photo);
            }
            let success_alert = new bootstrap.Toast(toast_success);
            success_alert.show();
        })
        .fail(function (result) {
            reset_buttons_on_submit(profile_form_buttons, profile_form_submit_button_spinner);
            toast_error_body.text("Ошибка при попытке обновления профиля!");
            let error_alert = new bootstrap.Toast(toast_error);
            error_alert.show();
        });
}

function reset_buttons_on_submit(buttons, submit_button_spinner) {
    'use strict';
    buttons.attr('disabled', 'disabled');
    submit_button_spinner.addClass('d-none');
}