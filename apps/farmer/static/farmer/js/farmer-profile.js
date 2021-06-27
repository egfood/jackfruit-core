$(document).ready(function () {

    let overlay_with_spinner = $("#jmodal-spinner-block"),
        profile_form = $("#jfarmer-profile-form"),
        profile_form_inputs = $(":input", profile_form),
        profile_form_buttons = $('.formButtons .button', profile_form),
        profile_form_submit_button = $('#jsubmit-js', profile_form),
        profile_form_submit_button_spinner = $('#jsubmit-spinner', profile_form_submit_button),
        profile_form_csrf = $("[name='csrfmiddlewaretoken']", profile_form).val(),
        toast_success = $('#jprofile-toast-updated'),
        toast_error = $('#jprofile-toast-error'),
        toast_error_body = $("#jprofile-toast-error-body", toast_error),
        profile_api_url = profile_form.attr('data-api-url');


    function load_profile_form_data() {
        overlay_with_spinner.show();
        $.get({url: profile_api_url})
            .done(function (result) {
                $.each(result, function (key, value) {
                    $(['name="' + key + '"'], profile_form).val(value);
                });
                overlay_with_spinner.hide();
                profile_form.removeClass('jform-changed');
            })
            .fail(function (result) {
                overlay_with_spinner.hide();
                toast_error_body.text("Ошибка при попытке загрузки профиля!");
                let error_alert = new bootstrap.Toast(toast_error);
                error_alert.show();
            });
    }

    function reset_profile_buttons_on_submit() {
        profile_form_buttons.attr('disabled', 'disabled');
        profile_form_submit_button_spinner.addClass('d-none');
    }

    function save_profile_form() {
        profile_form_buttons.attr('disabled', 'disabled');
        profile_form_submit_button_spinner.removeClass('d-none');

        $.ajax({
            url: profile_api_url,
            type: "PUT",
            data: profile_form.serialize(),
            headers: {'X-CSRFToken': profile_form_csrf}
        })
            .done(function (result) {
                reset_profile_buttons_on_submit();
                profile_form.removeClass('jform-changed');
                let success_alert = new bootstrap.Toast(toast_success);
                success_alert.show();
            })
            .fail(function (result) {
                reset_profile_buttons_on_submit();
                toast_error_body.text("Ошибка при попытке обновления профиля!");
                let error_alert = new bootstrap.Toast(toast_error);
                error_alert.show();
            });
    }

    profile_form_inputs.on('change', function () {
        profile_form.addClass('jform-changed');
    });

    $("#jprofileHeader").on('click', function () {
        load_profile_form_data();
    });

    profile_form_submit_button.on('click', function (e) {
        e.preventDefault();
        save_profile_form();
    });

});