$(document).ready(function(){
  $("#login").on('submit', function(e){
    e.preventDefault();
    data = {
      'email': this.email.value,
      'password': this.password.value
    }
    $('#error-message').hide()
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
        response = JSON.parse(xhr.responseText)
        $('#error-message').append(response['msg'])
        $('#error-message').show()
      }
    })
  });

  $("#logout").on('click', function(e){
    e.preventDefault();
    $.ajax({
      url: 'api/v1/logout',
      type : "GET",
      dataType : 'json',
      contentType: "application/json; charset=utf-8",
      success : function(result) {
        console.log(result);
        window.location.replace('/')
      },
      error: function(xhr, resp, text) {
          console.log(xhr, resp, text);
      }
    })
  });

  $("#add-antrian-form").on('submit', function(e){
    e.preventDefault();
    data = {
      'queue_number': this.queue_number.value
    }
    $.ajax({
      url: 'api/v1/recipes',
      type : "POST",
      dataType : 'json',
      contentType: "application/json; charset=utf-8",
      data : JSON.stringify(data),
      success : function(result) {
        console.log(result);
        $('#add-antrian').modal('toggle');
        load_recipe_admin()
      },
      error: function(xhr, resp, text) {
          console.log(xhr, resp, text);
      }
    })
  });

  $("#add-user-form").on('submit', function(e){
    e.preventDefault();
    if(this.role.value == 'admin'){
      data['role'] = 'admin'
    }
    data = {
    	'name': this.name.value,
    	'email': this.email.value,
    	'password': this.password.value,
    	'role': this.role.value
    }
    $.ajax({
      url: 'api/v1/users',
      type : "POST",
      dataType : 'json',
      contentType: "application/json; charset=utf-8",
      data : JSON.stringify(data),
      success : function(result) {
        console.log(result);
        $('#add-user').modal('toggle');
        alert('success add ' + this.email.value);
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
              color = "warning"
              if(recipe['status'] == 1){
                recipe['status'] = 'proses';
              } else if(recipe['status'] == 2){
                color = "success"
                recipe['status'] = 'siap';
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

function update(queue_number, status){
  data = {
    'status': parseInt(status)
  }
  $.ajax({
    url: 'api/v1/recipes/' + queue_number,
    type : "PUT",
    dataType : 'json',
    contentType: "application/json; charset=utf-8",
    data : JSON.stringify(data),
    success : function(result) {
      console.log(result);
      load_recipe_admin()
    },
    error: function(xhr, resp, text) {
        console.log(xhr, resp, text);
    }
  })
}

function load_recipe_admin(){
  $.getJSON( 'api/v1/recipes', function( data ) {
    items = "";
    $.each( data, function( key, val ) {
      if(key == 'payload'){
        $.each(val, function(id, recipe){
            color = "danger"
            queue_number = recipe['queue_number']
            tag_pending = 'onclick="update(\''+String(queue_number)+'\',\''+1+'\')"'
            tag_ready = 'onclick="update(\''+String(queue_number)+'\',\''+2+'\')"'
            tag_finish = 'onclick="update(\''+String(queue_number)+'\',\''+0+'\')"'
            if(recipe['status'] == 1){
              color = "warning"
              tag_pending = "disabled"
              recipe['status'] = 'proses';
            } else if(recipe['status'] == 2){
              color = "success"
              tag_ready = "disabled"
              recipe['status'] = 'siap';
            } else {
              tag_finish = "disabled"
              recipe['status'] = 'selesai';
            }
            items += "<tr class='"+color+"'><th scope='row'>"+recipe['queue_number']+"</th><td>"+recipe['date_update']+"</td>"
            pending = "<button "+tag_pending+" class='btn btn-primary'><span class='glyphicon glyphicon-refresh'></span>  Proses</button>"
            ready = "<button "+tag_ready+" class='btn btn-primary'><span class='glyphicon glyphicon-ok'></span>  Siap</a>"
            finish = "<button "+tag_finish+" class='btn btn-primary'><span class='glyphicon glyphicon-flag'></span>  Selesai</button>"
            button = "<div class='btn-group' style='margin:0px 20px;'>"+pending+ready+finish+"</div>"
            items += "<td>"+button+"</td></tr>"
        })
      }
    });
    $('#recipe-table').empty()
    $('#recipe-table').append(items)
  });
}
