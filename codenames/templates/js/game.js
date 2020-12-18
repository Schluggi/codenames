var spymaster = false;
var msg_shown = false;
var assassin_field_id = -1;
var team = '';

var color_map = {
    'red': '#dd482a',
    'blue': '#3373b3',
    'assassin': '#191d1c',
    'neutral': '#b5b7a2'
}

function inking_field(id, color){
    $('#field-' + id).css('border', '10px solid '+ color_map[color]);
}

function update_playground(data){
    // Updating score
    $('#score-red').text(data['score']['red']);
    $('#score-blue').text(data['score']['blue']);
    $('#progress-red .progress-bar').css('width', 100 - data['score']['red'] / data['start_score']['red'] * 100  + '%');
    $('#progress-blue .progress-bar').css('width', 100 - data['score']['blue'] / data['start_score']['blue'] * 100  + '%');

    // Updating members
    $('#members-blue').empty();
    $('#members-red').empty();

    $.each(data['members']['blue'], function(i, username){
        $('#members-blue').append('<p>' + username + '</p>')
    });

    $.each(data['members']['red'], function(i, username){
        $('#members-red').append('<p>' + username + '</p>');
    });


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
                    $('#field-'+ field_id).prop('src', '{{ url_for("static", filename="img/cards/") }}' + key + '/' + data['img'][key][index]);
                }

                $('#field-'+ field_id).addClass('clickedField');
            }
        });
    });

}

$(function() {
    var origin = new URL(window.location.href).origin;
    var socket = io(origin, { "path": "{{ request.script_root }}/socket.io/" });

    $('#scoreboard-wrapper').popover({
        content: function(){
            return $('#scoreboard-wrapper-content').html();
        },
        trigger: 'hover',
    });


    Swal.fire({
        title: 'Choose a username and join a team!',
        showDenyButton: true,
        confirmButtonText: 'BLUE',
        denyButtonText: 'RED',
        input: 'text',
        inputValue: localStorage.getItem('username'),
        inputAttributes: {
            placeholder: 'Username',
            required: true
        },
        allowEscapeKey: false,
        allowOutsideClick: false,
        allowEnterKey: false,
        returnInputValueOnDeny: true
    }).then((result) => {
        if (result.isConfirmed) {
            team = "blue";
        } else if (result.isDenied) {
            team = "red";
        }
        localStorage.setItem('username', result.value);

        socket.emit('join game', {
            game_id: $('#playground').data('game-id'),
            team: team,
            username: localStorage.getItem('username')
        });
    })

    socket.on('page reload', function(data) {
        // reload the page
        // notice: can't use location.reload() because of browser-post-warning
        window.location.href = window.location.href;
        console.log('page reload');
    });

    socket.on('game won', function(data) {
        console.log(data);
        if (msg_shown == false){
            if (data == team){
                Swal.fire({
                    icon: 'success',
                    title: 'YOU WON!',
                    showConfirmButton: false,
                    timer: 4000
                });
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'YOU LOST!',
                    showConfirmButton: false,
                    timer: 4000
                });
            }
            msg_shown = true;
            console.log(data + 'won this game');
        }
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

    socket.on('msg', function(data){
            $.snack(data['type'], data['msg'], 5000)
    });

    $('.field-img').click(function(){
        if (spymaster == false && $(this).hasClass('clickedField') == false){
            socket.emit('field update', {
                field_id: $(this)[0].id
            });
            console.log('field update');
        }
    });

    $('.game-mode').click(function(){
        $('#game_mode').val($(this).data('mode'));
        $('#new_round').trigger('click');
    });

    $('#spymaster, #spymaster-mobile').click(function(){
        if (spymaster) {
            spymaster = false;
            $('#spymaster-mobile').empty().html('Spymaster is off');
            $('#spymaster').val('Spymaster is off');
            $('.field-img').removeClass('clickedField');

            socket.emit('get playground');
            console.log('playground update');
        } else {
            spymaster = true;
            $('#spymaster-mobile').empty().html('Spymaster is on');
            $('#spymaster').val('Spymaster is on');
            $('.field-img').addClass('clickedField');

            socket.emit('get playground', 'spymaster=True');
            console.log('playground update (for spymaster)');
        }
    });
});
