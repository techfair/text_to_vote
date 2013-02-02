function updateValues() {
  $.ajax({
    url: '/get_json',
    success: function(data) {
        var json = JSON.parse(data);
        for (var vote_id in json){
            console.log(json[vote_id]['votes'].toString());
            $('#votes_'+vote_id.toString()).html(json[vote_id]['votes'].toString());

        } 
        setTimeout(updateValues, 2000); 
    }
  });
}

$(document).ready(function() {
  setTimeout(updateValues, 2000);
});