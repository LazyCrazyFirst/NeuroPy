$(function () {
    $(".send_mail_button").on("click", validate);

    // Validate email
    function validateEmail(email) {
        var re = /[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?/;
        return re.test(String(email).toLowerCase());
    }

    // validate email and send form after success validation
    function validate() {
        var email = $(".email").val();
        var $mail_error = $(".mail_error");
        $mail_error.text("");

        var name_value = document.querySelector('.name_value').value;
        var mail_value = document.querySelector('.mail_value').value;
        var subject_value = document.querySelector('.subject_value').value;
        var message_value = document.querySelector('.message_value').value;

        var name_error;
        var mail_error;
        var subject_error;
        var message_error;


        if (name_value !== "") {
            $(".name_error").text("Form sending").fadeIn();
            name_error = 1;
        } else {
            $(".name_error").text("Is not valid").fadeIn();
            name_error = 0;
        }

        if (validateEmail(email)) {
            $(".mail_error").text("Form sending").fadeIn();
            mail_error = 1;
        } else {
            $mail_error.fadeIn();
            $mail_error.text(email + " is not valid");
            mail_error = 0;
        }

        if (subject_value !== "") {
            $(".subject_error").text("Form sending").fadeIn();
            subject_error = 1;
        } else {
            $(".subject_error").text("Is not valid").fadeIn();
            subject_error = 0;
        }

        if (message_value !== "") {
            $(".message_error").text("Form sending").fadeIn();
            message_error = 1;
        } else {
            $(".message_error").text("Is not valid").fadeIn();
            message_error = 0;
        }

        if ((name_error === 1) && (mail_error === 1) && (subject_error === 1) && (message_error === 1)) {
            selection = {
                'name_value': name_value,
                'mail_value': mail_value,
                'subject_value': subject_value,
                'message_value': message_value
            }
            //передаём конечное значение на сервер в python, для дальнейшей обработки
            socket.emit('send email', {'selection': selection});
            document.querySelector('.name_value').value = "";
            $(".name_error").text("").fadeIn();
            document.querySelector('.mail_value').value = "";
            $(".mail_error").text("").fadeIn();
            document.querySelector('.subject_value').value = "";
            $(".subject_error").text("").fadeIn();
            document.querySelector('.message_value').value = "";
            $(".message_error").text("").fadeIn();
        }


        return false;
    }
});