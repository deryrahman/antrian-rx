$(document).ready(function(){
  $("#login").on('submit', function(e){
    e.preventDefault();
    data = {
      'email': this.email.value,
      'password': this.password.value
    }
    $.ajax({
      url: 'api/v1/login',
      type : "POST",
      dataType : 'json',
      contentType: "application/json; charset=utf-8",
      data : JSON.stringify(data),
      success : function(result) {
        console.log(result);
        window.location.replace('admin')
      },
      error: function(xhr, resp, text) {
          console.log(xhr, resp, text);
      }
    })
  });
});


function load_recipe(){
  $.getJSON( 'api/v1/recipes', function( data ) {
    items = "";
    $.each( data, function( key, val ) {
      if(key == 'payload'){
        $.each(val, function(id, recipe){
          if(recipe['status'] > 0){
              color = "bg-warning"
              if(recipe['status'] == 1){
                recipe['status'] = 'pending';
              } else if(recipe['status'] == 2){
                color = "bg-success"
                recipe['status'] = 'ready';
              }
              items += "<tr class='"+color+"'><th scope='row'>"+recipe['queue_number']+"</th><td>"+recipe['date_update']+"</td><td>"+recipe['status']+"</td></tr>"
          }
        })
      }
    });
    $('#recipe-table').empty()
    $('#recipe-table').append(items)
  });
}
