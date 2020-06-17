var spymaster = false;
var color_map = {
    'red': '#dd482a',
    'blue': '#3373b3',
    'assassin': '#191d1c',
    'neutral': '#b5b7a2'
}

function update_playground(data){
    // Updating score
    $('#fields-left-red').text(data['score']['red']);
    $('#fields-left-blue').text(data['score']['blue']);

    // Reset borders
    $('.field-img').each( function(){
        $(this).css('border', '')
    });

    console.log(data);

    $.each(data['fields'], function(key, field_ids){
        $.each(field_ids, function(index, field_id){
            // change border color
            $('#field-'+ field_id).css('border', '10px solid '+ color_map[key]);

            if (spymaster == false){
                // swap images
                $('#field-'+ field_id).prop('src', '/static/img/cards/' + key + '/' + data['img'][key][index]);
            }
        });
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
        if (spymaster == false){
            update_playground(data);
            console.log('playground update');
        }
    });

    socket.on('spymaster', function(data) {
        if (spymaster){
            update_playground(data);
            console.log('playground update');
        }
    });

    $('.field-img').click(function(){
        if (spymaster == false){
            socket.emit('field update', {
                game_id: $('#playground').data('game-id'),
                field_id: $(this)[0].id
            });
            console.log('field update');
        }
    });

    $('#spymaster').change(function(){
        if ($('#spymaster').prop('checked')){
            spymaster = true;
            $('.field-img').css('cursor', 'default');

            socket.emit('get spymaster', {
                game_id: $('#playground').data('game-id')
            });
            console.log('get spymaster');
        }
        else{
            spymaster = false;
            $('.field-img').css('cursor', 'pointer');

            socket.emit('get playground', {
                game_id: $('#playground').data('game-id')
            });
            console.log('playground update');
        }
    });


});
