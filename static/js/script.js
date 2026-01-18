$(document).ready(function () {
    console.log("Hello World")

    $('.menu-btn').click(function(event){
        event.preventDefault()
        event.stopPropagation(); // Sabse zaroori: click ko bahar failne se rokta hai
        // $('.slidemenu').addClass('active');
        $('.slidemenu').toggleClass('active');

    })

    $('.slidemenu ul li a').click((function (event){
        $('.slidemenu').removeClass('active');
    }))
})