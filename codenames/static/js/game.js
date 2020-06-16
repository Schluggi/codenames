function update_playground(data){
    $('#fields-left-red').text(data['counter_red']);
    $('#fields-left-blue').text(data['counter_blue']);

    $.each([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], function(index, field_id){
        $('#field-'+ field_id).css('filter', 'none');
    });

    $.each(data, function(key, field_ids){
        switch(key) {
            case "blue":
                $.each(field_ids, function(index, field_id){
                    $('#field-'+ field_id).css('filter', 'hue-rotate(140deg)');
                });
                break;
            case "red":
                $.each(field_ids, function(index, field_id){
                    $('#field-'+ field_id).css('filter', 'hue-rotate(270deg)');
                });
                break;
            case "neutral":
                $.each(field_ids, function(index, field_id){
                    $('#field-'+ field_id).css('filter', 'hue-rotate(445deg)');
                });
                break;
            case "assassin":
                $.each(field_ids, function(index, field_id){
                    $('#field-'+ field_id).css('filter', 'brightness(40%)');
                });
                break;
        }
    });
}

$(function() {
    var url = new URL(window.location.href);
    var socket = io(url.origin);

    socket.on('connect', function() {
        socket.emit('join game', {
            game_id: $('#playground').data('game-id')
        });
        console.log('connected');
    });

    socket.on('refresh', function(data) {
        location.reload();
        console.log('refresh');
    });

    socket.on('playground update', function(data) {
        if ($('#spymaster').prop('checked') == false){
            update_playground(data);
            console.log('playground update');
        }
    });

    socket.on('spymaster', function(data) {
        if ($('#spymaster').prop('checked')){
            update_playground(data);
            console.log('playground update');
        }
    });

    $('img').click(function(){
        if ($('#spymaster').prop('checked') == false){
            socket.emit('field update', {
                game_id: $('#playground').data('game-id'),
                field_id: $(this)[0].id
            });
            console.log('field update');
        }
    });

    $('#spymaster').change(function(){
        if ($('#spymaster').prop('checked')){
            $('img').css('cursor', 'default');
            socket.emit('get spymaster', {
                game_id: $('#playground').data('game-id')
            });
            console.log('get spymaster');
        }
        else{
            $('img').css('cursor', 'pointer');
            socket.emit('get playground', {
                game_id: $('#playground').data('game-id')
            });
            console.log('playground update');
        }
    });


});
