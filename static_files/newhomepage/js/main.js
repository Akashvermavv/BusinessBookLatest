// Fixed Nav Onscroll

$(window).on("scroll",function(){
	if($(window).scrollTop()) {
	  $('.navbar-xl').addClass('fixed-nav');
	}

	else{
	  $('.navbar-xl').removeClass('fixed-nav');
	}
});

// Toggle menu Icon
$(document).ready(function(){  
    $(".navbar-toggler").click(function(){  
        $("nav").toggleClass("nav-bg");  
    });  
}); 


