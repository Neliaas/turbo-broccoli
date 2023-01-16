$(".accept").click(function(){
    $(".cookie").hide();
});
$('a[href="#cookie"]').click(function() {
    $(window).scrollTo('#cookie', {
     onAfter: function() {
      setTimeout(function () {
         alert('test');
       }, 100)
     }
    })
  });