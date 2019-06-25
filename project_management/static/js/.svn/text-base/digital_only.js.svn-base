
$(document).ready(function(){           
                $('.efforts').bind('keypress',function(event){
    if (event.which > 31 && (event.which < 48 || event.which > 57)) return false;
  });
  $('.cost').bind('keypress',function(event){
    if (event.which > 31 && (event.which < 48 || event.which > 57)) return false;
  });
$('#tot_effort').bind('keypress',function(event){
    if((event.which < 46 || event.which > 59) && event.which > 31) {
        event.preventDefault();
    } // prevent if not number/dot

    if(event.which == 46  && $(this).val().indexOf('.') != -1 ) {
        event.preventDefault();
    } // prevent if already dot
});
		   
    });


