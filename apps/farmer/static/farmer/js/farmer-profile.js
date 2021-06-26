$(document).ready(function () {

    let overlay_with_spinner = $("#jmodal-spinner-block"),
        profile_form = $("#jfarmer-profile-form"),
        profile_form_inputs = $(":input", profile_form),
        profile_form_submit_button = $('.jsubmit', profile_form),
        profile_form_csrf = $("[name='csrfmiddlewaretoken']", profile_form).val(),
        profile_api_url = profile_form.attr('data-api-url');

    function load_profile_form_data() {
        overlay_with_spinner.show();
        $.get({url: profile_api_url})
            .done(function (result) {
                $.each(result, function (key, value) {
                    $(['name="' + key + '"'], profile_form).val(value);
                    // alert(key + ": " + value);
                });
                overlay_with_spinner.hide();
                profile_form.removeClass('jform-changed');
            });
    }

    function save_profile_form() {
        overlay_with_spinner.show();
        $.ajax({
            url: profile_api_url,
            type:"PUT",
            data: profile_form.serialize(),
            headers: {'X-CSRFToken': profile_form_csrf}
        })
            .done(function (result) {
                overlay_with_spinner.hide();
                profile_form.removeClass('jform-changed');
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