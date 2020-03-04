$(document).on('submit','#form',function(e){
    e.preventDefault();
    msg = ''
    var $myForm = $('#form')
    var $formData = $(this).serialize()
    var $thisURL = $myForm.attr('data-url') || window.location.href
    var $mailID = $('#email').val()
    var isValid=validateForm()
    if (isValid)
    {
    $.ajax({
        type:'POST',
        url:$thisURL,
        data: $formData,
        xhrFields: {
        withCredentials: true
        },
        success:handleFormSuccess,
    });
    }
     function handleFormSuccess(data){
        $('#myModal').modal('show');
        console.log($mailID)
        $myForm[0].reset();
            $.ajax({
            type:'POST',
            url:'/success',
            data: $formData,
            success:function(){
            $('#myModal').modal('hide');
            }
        });
        }
    })


    function validateForm(){
    var $mailID = $('#email').val()
    var mailReg = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/ ;
    var isValid = false
        if (mailReg.test($mailID))
        {
        $('#error_mail').html("<div class=\"error-text medium\"><strong></strong></div>")
            mailValid = true
        }
        else
        {
        msg = "* Enter Valid Email ID."
        $('#error_mail').html("<div class=\"error-text medium\"><strong>"+ msg +"</strong></div>")
            mailValid = false
        }

        if (mailValid){
        isValid = true
        }
        else{
        isValid=false
        }
            return isValid
    }


    function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });