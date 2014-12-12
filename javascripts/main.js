console.log('This would be the main JS file.');

// Scrolling function
$( document ).ready(function() {
    $.localScroll({
    	axis: 'y',
    	duration: 400
    });
});

$(window).scroll(function(e){ 
  $el = $('#nav1'); 
  if ($(this).scrollTop() > 200 && $el.css('position') != 'fixed'){ 
    $('#nav1').css({'position': 'fixed', 'top': '0px'}); 
  }
  if ($(this).scrollTop() < 200 && $el.css('position') == 'fixed')
  {
    $('#nav1').css({'position': 'static', 'top': '0px'}); 
  } 
});