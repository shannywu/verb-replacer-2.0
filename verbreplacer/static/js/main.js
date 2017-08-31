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
            $('#search-result').html('<tr><td colspan="4"><img class="ui image centered" src="static/img/loading-b.gif"></td></tr>')
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
    if (data['recommend_list']) {
        console.log('yes');
        htmlFrag += '<tr>' +
                    '<td rowspan="3">' + 
                      '<span class="wrong-verb">' + data['wrong_verb'] + 
                      '</span><br><br>'+ data['object'] + 
                    '</td>'
        // data['sug_list'].forEach(function(element) {
        for(i = 0; i < data['recommend_list'].length; i++) {
          console.log(data['recommend_list'][i])
          console.log(i)
          element = data['recommend_list'][i]
          htmlFrag += '<td>' + (i+1) + '</td>' +
                      '<td>' + element[0] + '</td>' +
                      // '<td>' + element[1] + '</td>' +
                      '</tr>';
          // if(i < data['vobj_list'].length) {
          //   htmlFrag += '<td>' + data['vobj_list'][i][0] + '</td>' +
          //   '</tr>' ;
          // }
          // else {
          //   htmlFrag += '<td>N/A</td>' + '</tr>' ;
          // }
                      
        }
    } else {
        htmlFrag = '<tr><td colspan="4" class="no-replace">The sentence looks ok.</td></tr>';
    }
    console.log(htmlFrag)
    // $('#search-bar').removeClass("loading");
    $('#search-result > .ui.inverted.dimmer').removeClass("active");
    $('#search-result').html(htmlFrag);
};
