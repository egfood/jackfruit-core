$(document).ready(function () {
    let is_send_feedback = false,
        estimate_feedback_form = $("#jestimate-feedback-form-js"),
        btn_send_feedback = $("#jbtn-estimate-feedback-js"),
        toast_success = $("#jestimate-feedback-success-js"),
        toast_error = $("#jsend-feedback-toast-error-js"),
        toast_error_body = $("#jsend-feedback-toast-error-body-js"),
        estimate_feedback_popup = $("#jpopup-estimate-feedback-js");

    $(".jbtn-show-feedback-popup-js").on('click', function () {
        btn_send_feedback.attr('data-api-url', $(this).attr('data-api-url'));
        estimate_feedback_form[0].reset();
    });

    btn_send_feedback.on('click', function (e) {
        e.preventDefault();

        if (is_send_feedback === false) {
            is_send_feedback = true;

            $.ajax({
                //It's workaround and It must be fixed
                url: $(this).attr('data-api-url'),
                type: "POST",
                headers: {'X-CSRFToken': estimate_feedback_form.attr('data-csrf')},
                data: new FormData(estimate_feedback_form[0]),
                processData: false,
                contentType: false,
            })
                .done(function (result) {
                    is_send_feedback = false;
                    $(".mainWrap").css("filter", "none");
                    $(".vegFrameDropMenu, .mainWrapOpacity").css("display", "none");
                    estimate_feedback_popup.fadeOut(200);
                    let toast = new bootstrap.Toast(toast_success);
                    toast.show();
                    estimate_feedback_form[0].reset();
                })
                .fail(function (result) {
                    if (result.responseJSON.detail) {
                        toast_error_body.text(result.responseJSON.detail);
                    } else {
                        toast_error_body.text(result.responseText);
                    }

                    let toast = new bootstrap.Toast(toast_error);
                    is_send_feedback = false;
                    toast.show();
                });
        }
    });

});