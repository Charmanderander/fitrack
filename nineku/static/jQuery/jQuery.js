function changeHeart(id){
  id = id.replace('likebutton','');
  var currentLikes = document.getElementById('likecount'+id).innerHTML;

  console.log(currentLikes)

  if (document.getElementById(id+'heart').className=="fa fa-heart-o"){
    document.getElementById(id+'heart').className="fa fa-heart";
    document.getElementById('likecount'+id).innerHTML = +currentLikes + 1;
  } else {
    document.getElementById(id+'heart').className="fa fa-heart-o";
    document.getElementById('likecount'+id).innerHTML = +currentLikes - 1;
  }
}

function likePost(id){
  id = id.replace('likeform','');
  $.ajax({
    url : "likeProcess/", // the endpoint
    type : "POST", // http method
    data : { id : $('#id'+id).val(), username : $('#username'+id).val() }, // data sent with the post request

    // handle a successful response
    success : function(json) {
    },

    // handle a non-successful response
    error : function(xhr,errmsg,err) {
      $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
      " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
      console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
  });
};


function getCookie(name) {
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

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});

$('.forms').on('submit', function(event){
  event.preventDefault();
});
