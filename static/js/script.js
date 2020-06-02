/*
$(document).ready(function(){
  $("#owl-slider1").owlCarousel({
      slideSpeed: 300,
      paginationSpeed: 300,
      singleItem: true,
      navigation: true
  });
});

*/


$('body').scrollspy({ target:'#main-nav'});

$('#main-nav a').on('click',function(e){
    if(this.hash !== ''){
      e.preventDefault();
  
      const hash= this.hash;
  
      $('html, body').animate({
        scrollTop: $(hash).offset().top
      },700, function() {
        window.location.hash= hash;
      });
    }
  });


$(document).ready(function() {

    $('#preloader').css('display', 'none');


    $('#owl-slider1').owlCarousel({
        loop:true,
        autoplay: true,
        responsive:{
            0:{
                items:1
            },
            600:{
                items:1
            },
            1000:{
                items:1
            }
        }
    });
 
    $("#owl-slider2").owlCarousel({
   
        autoplay:true,
        autoPlay: 2000, //Set AutoPlay to 2 seconds
   
        responsive:{
            0:{
                items:1,
                
            },
            600:{
                items:2,
                
            },
            900:{
                items:3,
               
            },
            1000:{
                items:4,
            }
        }
   
    });


    new WOW().init();

    $('.testimonialSlider').slick({
        arrows: true,
      });  
   
});