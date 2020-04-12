
(function ($) {
    "use strict";

    /*==================================================================
    [ Validate ]*/
    var input = $('.validate-input .input100');

    $('.validate-form').on('submit',function(){
        var check = true;

        for(var i=0; i<input.length; i++) {
            if(validate(input[i]) == false){
                showValidate(input[i]);
                check=false;
            }
        }

        return check;
    });
    $(".countdown")
            .countdown('2020/12/1', function(event) {
            $(this).html(
                event.strftime('<div class="flex-col-c-m size6 bor2 m-l-10 m-r-10 m-t-15"><span class="l2-txt1 p-b-9 days">%D</span><span class="s2-txt4">Days</span></div><div class="flex-col-c-m size6 bor2 m-l-10 m-r-10 m-t-15"><span class="l2-txt1 p-b-9 hours">%H</span><span class="s2-txt4">Hours</span></div><div class="flex-col-c-m size6 bor2 m-l-10 m-r-10 m-t-15"><span class="l2-txt1 p-b-9 minutes">%M</span><span class="s2-txt4">Minutes</span></div><div class="flex-col-c-m size6 bor2 m-l-10 m-r-10 m-t-15"><span class="l2-txt1 p-b-9 seconds">%S</span><span class="s2-txt4">Seconds</span></div>')
            );
        });

    $('.validate-form .input100').each(function(){
        $(this).focus(function(){
           hideValidate(this);
        });
    });

    function validate (input) {
        if($(input).attr('type') == 'email' || $(input).attr('name') == 'email') {
            if($(input).val().trim().match(/^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{1,5}|[0-9]{1,3})(\]?)$/) == null) {
                return false;
            }
        }
        else {
            if($(input).val().trim() == ''){
                return false;
            }
        }
    }

    function showValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).addClass('alert-validate');
    }

    function hideValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).removeClass('alert-validate');
    }

    
    

})(jQuery);