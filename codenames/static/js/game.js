var spymaster = false;
var msg_shown = false;
var assassin_field_id = -1;

var color_map = {
    'red': '#dd482a',
    'blue': '#3373b3',
    'assassin': '#191d1c',
    'neutral': '#b5b7a2'
}

function winning(team) {
    Swal.fire({
      icon: 'success',
      title: 'Team ' + team + ' wins!',
      showConfirmButton: false,
      timer: 2500
    });

    msg_shown = true;
    $('#spymaster').prop('checked', true);
    $('#spymaster').trigger('change');
}

function losing() {
    Swal.fire({
      icon: 'error',
      title: 'Game over!',
      showConfirmButton: false,
      timer: 2500
    });

    msg_shown = true;
    $('#spymaster').prop('checked', true);
    $('#spymaster').trigger('change');
}

function inking_field(id, color){
    $('#field-' + id).css('border', '10px solid '+ color_map[color]);
}

function update_playground(data){
    // Updating score
    $('#score-red').text(data['score']['red']);
    $('#score-blue').text(data['score']['blue']);

    if (spymaster == false){
        // Reset borders
        $('.field-img').each( function(){
            $(this).css('border', '')
        });
    }

    $.each(data['fields'], function(key, field_ids){
        $.each(field_ids, function(index, field_id){
            if (data['spymaster']){
                inking_field(field_id, key);
            }else{
                // swap images
                var img = document.getElementById('field-'+ field_id);

                img.onload = function(){
                    inking_field(field_id, key);
                };

                if ($('#field-'+ field_id).prop('src').includes('cards') == false){
                    $('#field-'+ field_id).prop('src', '/static/img/cards/' + key + '/' + data['img'][key][index]);
                }

                $('#field-'+ field_id).addClass('clickedField');

                if (key == 'assassin' && msg_shown == false){
                    losing();
                }
            }



        });
    });


    if (msg_shown == false){
        if (data['score']['red'] == 0){
            winning('red');
        } else if (data['score']['blue'] == 0){
            winning('blue');
        }

   }

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

    socket.on('page reload', function(data) {
        // reload the page
        // notice: can't use location.reload() because of browser-post-warning
        window.location.href = window.location.href;
        console.log('page reload');
    });

    socket.on('playground update', function(data) {
            update_playground(data);
            console.log('playground update');
    });

    socket.on('post spymaster', function(data) {
        if (spymaster){
            update_playground(data);
            console.log('playground update');
        }
    });

    $('.field-img').click(function(){
        if (spymaster == false && $(this).hasClass('clickedField') == false){
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
            $('.field-img').addClass('clickedField');

            socket.emit('get spymaster', {
                game_id: $('#playground').data('game-id')
            });
            console.log('get spymaster');
        }
        else{
            spymaster = false;
            $('.field-img').removeClass('clickedField');

            socket.emit('get playground', {
                game_id: $('#playground').data('game-id')
            });
            console.log('playground update');
        }
    });


});
