$(window).on('resize', function() {
    var win = $(this);
    if (win.width() < 600) {
  
      document.getElementById("homemenu").classList.remove("nav-pills");
      document.getElementById("homemenu").classList.add("flex-column");
      document.getElementById("topics").classList.remove("col-8");
      document.getElementById("topics").classList.add("col-12");
      var els = document.getElementsByClassName('metadata');
      for (var i = 0; i < els.length; i++) {
        els[i].classList.remove('mt-4')
      }
      $("#login-carousel").remove();
      $("#statistics").remove();
      $('.author-separator').remove();
      $('#responsive-login').removeAttr('hidden');
      
    } else {
      document.getElementById("homemenu").classList.add("nav-pills");
      document.getElementById("homemenu").classList.remove("flex-column");
      
      
    }
  });


function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#img-prof')
                .attr('src', e.target.result)
        };

        reader.readAsDataURL(input.files[0]);
    }
}


    
