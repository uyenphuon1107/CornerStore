var util = {
    mobileMenu() {
        $("#nav").toggleClass("nav-visible");
    },
    windowResize() {
        if ($(window).width() > 800) {
            $("#nav").removeClass("nav-visible");
        }
    },
    scrollEvent() {
        var scrollPosition = $(document).scrollTop();

        $.each(util.scrollMenuIds, function(i) {
            var link = util.scrollMenuIds[i],
                container = $(link).attr("href"),
                containerOffset = $(container).offset().top,
                containerHeight = $(container).outerHeight(),
                containerBottom = containerOffset + containerHeight;

            if (scrollPosition < containerBottom - 20 && scrollPosition >= containerOffset - 20) {
                $(link).addClass("active");
            } else {
                $(link).removeClass("active");
            }
        });
    }
};
$('#myModal').on('shown.bs.modal', function () {
  $('#myInput').trigger('focus')
})

$('#exampleModal').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  var recipient = button.data('whatever') // Extract info from data-* attributes
  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  var modal = $(this)
  modal.find('.modal-title').text('New message to ' + recipient)
  modal.find('.modal-body input').val(recipient)
})

$(document).ready(function() {

    util.scrollMenuIds = $("a.nav-link[href]");
    $("#menu").click(util.mobileMenu);
    $(window).resize(util.windowResize);
    $(document).scroll(util.scrollEvent);

});
