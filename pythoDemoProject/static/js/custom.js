// sticky-header
$(window).scroll(function () {
    var sc = $(window).scrollTop();
    if (sc > 0) {
      $("header").addClass("sticky-header");
    } else {
      $("header").removeClass("sticky-header");
    }
  });

  $(document).ready(function(){
    $("#user_nav").click(function(){
    $(".user-menu").toggleClass("active");
    });
  });





