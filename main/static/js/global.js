$(document).ready(function () {
  // Only one checkbox can be selected at time
  $('table').bind('click', 'input[type="checkbox"]', function(event){
    // If the checkbox is already checked
    var object = $(event.target);
    if(object.is(":checked") != true){
      object.attr('checked', false);
    } else {
      object.attr('checked', true);
    }
    activateToolbar();
  });
});

function activateToolbar(){
  // Activate or deactivate Toolbar
  if($('input[type="checkbox"]:checked').length > 0) {
    $('.can-be-deactivated').show();
  } else {
    $('.can-be-deactivated').hide();
  }
}
function uncheckAllCheckbox() {
  // uncheck all chechbox items in the page
  $('input[type="checkbox"]').each(function(){
    $(this).attr('checked', false);
  });
}


$(document).ready(function () {
  // Activate or deactivate Toolbar

  /*
  $("#delete-user-btn").click(function(){
     var row_id = $('input[type="checkbox"]:checked').attr('data-id');
        $.ajax({
          type: "POST",
          url: "/publisher/sites/delete/",
          data: 'id=' + row_id,
          success: function(result)
            {
               alert("site eliminado");         

            } 
        });

       return false;

     
});
*/

//$('#myModal').modal();




 $("#delete-user-btn").click(function(){
     var row_id = $('input[type="checkbox"]:checked').attr('data-id');
       ('#myModal').modal();


       return false;

     
});




















});
