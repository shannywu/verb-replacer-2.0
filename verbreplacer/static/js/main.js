// var replaceSocket;
// $(document).ready(function() {
//     initReplaceSocket();
// });


// function initReplaceSocket() {
//       // init translation socket
//       replaceSocket = new WebSocket("ws://" + window.location.host + "/replace/");
//       replaceSocket.onmessage = function(message) {
//           data = JSON.parse(message.data);
//           if(data.type == 'status') {
//               console.log('status: ' + data.content);
//               $('#search-result div.ui.text.loader').text(data.content);
//           } else if(data.type == 'result') {
//               renderSearchResult(data.content);
//               // var option = $('#trans_menu .item.active').text().toLowerCase();
//               // $('#search-result').addClass('active').siblings('p.result').removeClass('active');
//           }
//       }
//       replaceSocket.onopen = function(message) {
//         $('#search-bar').keypress(function(e){
//             if (e.which == 13) { $('#search-btn').click() }
//         })
//         $('#search-btn').click(function() {
//             search();
//           // $('#search_input').on('input', function() {
//           //     clearTimeout(timeoutId);
//           //     timeoutId = setTimeout(search, 1000);
//           // });
//             });
//         }
//       replaceSocket.onclose = function(message) {
//           setTimeout(function(){initReplaceSocket();}, 5000);
//       }
// }


// function search() {
//     var query = $('#search-bar').val().trim();

//     if (query !== '') {
//         console.log(query);
//         // $('#search-bar').addClass("loading");
//         $('#search-result').removeClass("hide");
//         $('#search-result').html('<tr><td colspan="3">' +
//             '<div class="ui segment loading-bar">' +
//                 '<div class="ui inverted dimmer">' +
//                     '<div class="ui text loader">Loading</div>' +
//                         '</div>' +
//                     '</div>' +
//                 '</td></tr>')
//         $('#search-result tr td > .ui.segment > .ui.inverted.dimmer').addClass("active");
//         replaceSocket.send(JSON.stringify({'text': query}));
//     }
    // $('#search-bar').keypress(function(e){
    //     if (e.which == 13) { $('#search-btn').click() }
    // })
    // $('#search-btn').click(function() {
    //     var query = $('#search-bar').val();
    //     console.log(query);
    //     if (query !== '') {
    //         console.log(query)
            // $('#search-result').html('<tr><td colspan="3"><img class="ui image centered" src="static/img/loading-b.gif"></td></tr>')
            // $.ajax({
            //     url: '/query/',
            //     data: {'search': query},
            //     type: 'POST',
            //     dataType: 'json',
            // }).done(function(data) {
            //     console.log(data);
            //     renderSearchResult(data);
            // });
    //     }
    // });
// }

$(document).ready(function() {
    $('#search-bar').keypress(function(e){
        if (e.which == 13) { 
          $('#search-btn').click()
        }
    })
    $('#search-btn').click(function() {
        var query = $('#search-bar').val().trim();
        
        if (query !== '') {
            console.log(query)
            $('#search-result').removeClass("hide");
            $('#search-result').html('<tr><td colspan="5"><img class="ui image centered" src="static/img/loading-b.gif"></td></tr>')
            // resetAutoSaveTimer(3000);
            $.ajax({
                url: '/query/',
                data: {'search': query},
                type: 'POST',
                dataType: 'json',
            }).done(function(data) {
                console.log(data);
                renderSearchResult(data);
            });
        }
    });
});


function renderSearchResult(data) {
    var htmlFrag = '';
    console.log(data)
    if (data['sug_list']) {
        htmlFrag += '<tr>' +
                    '<td rowspan="5">' + 
                      '<span class="wrong-verb">' + data['wrong_verb'] + 
                      '</span><span>'+ data['object'] + 
                    '</span></td>'
        data['sug_list'].forEach(function(element) {
          console.log(element)
          htmlFrag += '<td class="right-align">' + element[0] + '</td>' +
                      '<td>' + element[1] + '</td>' +
                      '<td class="right-align">' + element[2] + '</td>' +
                      '<td class="right-align">' + element[3] + '</td>' +
                    '</tr>' ;
        })
    } else {
        htmlFrag = '<tr><td colspan="3" class="no-replace">The sentence looks ok.</td></tr>';
    }
    console.log(htmlFrag)
    // $('#search-bar').removeClass("loading");
    $('#search-result > .ui.inverted.dimmer').removeClass("active");
    
    $('#search-result').html(htmlFrag);
};
