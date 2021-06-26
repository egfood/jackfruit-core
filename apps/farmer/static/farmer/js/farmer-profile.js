$(document).ready(function () {

    let overlay_with_spinner = $("#jmodal-spinner-block"),
        profile_form = $("#jfarmer-profile-form"),
        profile_api_url = profile_form.attr('data-api-url');

    $(":input", profile_form).change(function() {
      $(this).closest('form').data('changed', true);
    });

    function load_profile_data() {
        overlay_with_spinner.show();

        $.get({url: profile_api_url})
            .done(function (result) {
                window.alert(result);
            });

        setTimeout(function () {
            overlay_with_spinner.hide();
        }, (3 * 1000));
    }

    load_profile_data();

});