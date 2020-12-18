$(function() {
    $.toastDefaults = {
        position: 'bottom-right',
        dismissible: true,
        stackable: true,
        pauseDelayOnHover: true,
        style: {
            toast: '',
            info: '',
            success: '',
            warning: '',
            error: ''
        }
    };

     $.each($('#messages').children(), function(i, obj){
        $.snack($(obj).data('category'), $(obj).text(), 5000);
    });

});
