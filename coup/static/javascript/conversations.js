
$(document).ready(function(){
    var group_count = 5;
    var group_begin = 0;
    var conversation_count = 5;
    var conversation_begin = 0;
    var message_count = 100;
    var message_begin = 0;
    var scroll_height = 100000;
    //get cookie for csrf token
    function getCookie(name){
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    //adds is active class for groups
    $(document).on('click','button.group-name',function(){
        $('button.group-name').removeClass('active');
        $(this).addClass('active');
        $('.conversation-link').removeClass('active');
    });

    $(document).on('click', '.up-group',function(){
        conversation_begin = 0;
        message_begin = 0;
        var csrftoken = getCookie('csrftoken');
        var destination = $(this).attr('data-group-url');
        var begin = group_begin - 5;
        if( begin < 0) {
            begin = 0;
        }
        $.ajax({
            type:   'POST',
            url: destination,
            data:   
                {
                    'begin': begin,
                    'count': group_count,
                    'csrfmiddlewaretoken':csrftoken
                },
                failure: function(){
                    alert('Fail');
                },
                success: function(data) {
                    $('.groups-list').fadeOut(100, function(){
                        $(this).html(data);
                    }).fadeIn(400);
                    group_begin = group_begin - 5;
                    if( group_begin < 0) {
                        group_begin = 0;
                    }
                    $('.conversations-list').text('Click on a group to view conversations');
                }
        });
    });

    $(document).on('click', '.up-conv',function(){
        message_begin = 0;
        var csrftoken = getCookie('csrftoken');
        var destination = $(this).attr('data-conv-url');
        var group = $('button.group-name.active').attr('data-id');
        console.log(group);
        var begin = conversation_begin - 5;
        if( begin < 0) {
            begin = 0;
        }
        $.ajax({
            type:   'POST',
            url: destination,
            data:   
                {
                    'begin': begin,
                    'count': conversation_count,
                    'group': group,
                    'csrfmiddlewaretoken': csrftoken
                },
                failure: function(){
                    alert('Fail');
                },
                success: function(data) {
                    $('.conversations-list').fadeOut(100, function(){
                        $(this).html(data);
                    }).fadeIn(400);
                    conversation_begin = conversation_begin - 5;
                    if( conversation_begin < 0) {
                        conversation_begin = 0;
                    }
                    $('.conversations-list').text('Click on a group to view conversations');
                }
        });
    });

    $(document).on('click', '.down-group',function(){
        conversation_begin = 0;
        message_begin = 0;
        var csrftoken = getCookie('csrftoken');
        var destination = $(this).attr('data-group-url');
        var begin = group_begin + 5;
        $.ajax({
            type:   'POST',
            url: destination,
            data:   
                {
                    'begin': begin,
                    'count': group_count,
                    'csrfmiddlewaretoken':csrftoken
                },
                failure: function(){
                    alert('Fail');
                },
                success: function(data) {
                    if($(data).find('.stop').length>0){
                        return;
                    }
                    else {
                        $('.groups-list').fadeOut(100, function(){
                            $(this).html(data);
                        }).fadeIn(400);
                        group_begin = group_begin + 5;
                        $('.conversations-list').text('Click on a group to view conversations');
                    }
                }
        });
    });

    $(document).on('click', '.down-conv',function(){
        message_begin = 0;
        var csrftoken = getCookie('csrftoken');
        var destination = $(this).attr('data-conv-url');
        var group = $('button.group-name.active').attr('data-id');
        var begin = conversation_begin + 5;
        $.ajax({
            type:   'POST',
            url: destination,
            data:   
                {
                    'begin': begin,
                    'count': conversation_count,
                    'group': group,
                    'csrfmiddlewaretoken': csrftoken
                },
                failure: function(){
                    alert('Fail');
                },
                success: function(data) {
                    if($(data).find('.stop').length>0){
                        return;
                    }
                    else {
                        $('.conversations-list').fadeOut(100, function(){
                            $(this).html(data);
                        }).fadeIn(400);
                        conversation_begin = conversation_begin + 5;
                        //$('.conversations-list').replaceWith('Click on a group to view conversations');
                    }
                }
        });
    });

    //ajax query to display conversations list
    $(document).on('click','.group-link',function(){
        conversation_begin = 0;
        message_begin = 0;
        var group_name = $(this).text();
        var group = $(this).find('.group-name').attr('data-id');
        var csrftoken = getCookie('csrftoken');
        var destination = $(this).closest('ul').attr('data-url');
        
        $.ajax({
            type: 'POST',
            url:    destination,
            data:   {'begin': conversation_begin,
                    'count': conversation_count,
                    'group': group,
                    'csrfmiddlewaretoken': csrftoken
                    },
                failure: function(){
                    alert('No conversations available!');    
                },
                success: function(returnedData){
                    $('.conversations-list').fadeOut(100, function(){
                        $(this).html(returnedData);
                    }).fadeIn(400);

                    $('.messages-list').replaceWith('Click on a conversation to show messages');
            }
            });
    });
    //adds is active class (fire) for conversations
    $(document).on('click','button.conversation-name',function(){
        $('button.conversation-name').removeClass('fire');
        $(this).addClass('fire');
    });

    //ajax query to display messages list
    $(document).on("click",'.conversation-link',function(){
        message_begin = 0;
        var conversation_name = $(this).text();
        var conversation = $(this).find('.conversation-name').attr('data-id');
        var csrftoken = getCookie('csrftoken');
        var destination = $(this).closest('ul').attr('data-url');
        
        $.ajax({
            type: 'POST',
            url:    destination,
            data:   {'begin': message_begin,
                    'count': 100,
                    'conversation': conversation,
                    'csrfmiddlewaretoken': csrftoken
                    },
                failure: function(){
                    alert('No messages available!');    
                },
                success: function(msg){
                    //$('.messages-block').html(msg);
                    $('.messages-block').fadeOut(100, function(){
                        $(this).html(msg);
                    }).fadeIn(400);
                    $(this).first('.conversation-name').addClass('fire');
                    $(".messages-block").animate({ scrollTop: scroll_height}, 400);
                }
            });
    });
    //sends the message to the model using ajax
    $(document).on('click','.btn-send',function(){
        var text = $('textarea.msg-box').val();
        var conversation_id = $('.fire').attr('data-id');
        var destination = $('.msg-box').attr('data-msg');
        var csrftoken = getCookie('csrftoken');
        console.log(conversation_id);
        console.log(destination);
        $.ajax({
            type:   'POST',
            url:    destination,
            data:   {
                    'message':text,
                    'conversation': conversation_id,
                    'csrfmiddlewaretoken':csrftoken
                },
                failure: function(){
                    alert('Cannot send message!');
                },
                success: function(){
                    $('.msg-box').val('');
                    $('.fire').click();
                    $(".messages-block").animate({ scrollTop: scroll_height}, 400);

                }
        });
    });
    
});


   
