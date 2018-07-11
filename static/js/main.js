//Scroll Reveal
    window.sr = ScrollReveal();
    sr.reveal('.navbar', {
      duration: 2000,
      origin:'bottom'
    });
    sr.reveal('.showcase-left', {
      duration: 2000,
      origin:'top',
      distance:'300px'
    });
    sr.reveal('.showcase-right', {
      duration: 2000,
      origin:'right',
      distance:'300px'
    });
    sr.reveal('.showcase-btn', {
      duration: 2000,
      delay: 2000,
      origin:'bottom'
    });
    sr.reveal('#testimonial div', {
      duration: 2000,
      origin:'bottom'
    });
    sr.reveal('.info-left', {
      duration: 2000,
      origin:'left',
      distance:'300px',
      viewFactor: 0.2
    });
    sr.reveal('.info-right', {
      duration: 2000,
      origin:'right',
      distance:'300px',
      viewFactor: 0.2
    });

//Smooth Scroll

    $(function() {
      // Smooth Scrolling
      $('a[href*="#"]:not([href="#"])').click(function() {
        if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
          var target = $(this.hash);
          target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
          if (target.length) {
            $('html, body').animate({
              scrollTop: target.offset().top
            }, 1000);
            return false;
          }
        }
      });
    });
    
    //Navbar Scrolling
    
   /* $(document).ready(function(){
      var scroll_start = 0;
      var start_change = $('#newsletter');
      var offset = start_change.offset();
      if(start_change.length){
        $(document).scroll(function(){
          scroll_start = $(this).scrollTop();
          if(scroll_start > offset.top)
          {
            $('.navbar').css('background', 'white');
            $('.navbar-brand').css('color', 'black');
          }

          else{
            $('.navbar').css('background', 'transparent');
            $('.navbar-brand').css('color', 'white');
          }
        });
      }
    });*/
setTimeout(function() {
  document.getElementById('hideMe').style.display='none'
}, 3*1000);