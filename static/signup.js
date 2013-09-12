/* ===============================
 * Touchpoint Copyright 2013.
 * @author: Ryan Wong
 * @file: signup.css
 * Contains jquery for home-public page.
 * =============================== */

// height of viewport (minus the headerBar) is used
// for absolute height/width centering
$(window).ready(function(){
	viewportHeight = $(window).innerHeight() - $('.headerBar').height();
	$('.viewport').css('height',viewportHeight);
});

$(window).resize(function(){
	viewportHeight = $(window).innerHeight() - $('.headerBar').height();
	$('.viewport').css('height',viewportHeight);
});