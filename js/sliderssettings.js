function initializeSliders() {
    $('.slider').slick({
        dots: false,
        slidesToShow: 5,
        slidesToScroll: 1,
        variableWidth: false,
        centerMode: true,
        arrows: true,
        autoplay: true,
    
        centerMode: false,
        swipeToSlide: true,
        autoplaySpeed: 3000,

        responsive: [
            {
            breakpoint: 768,
            settings: {
                arrows: true,
                centerMode: true,
                swipeToSlide: true,
                centerPadding: '40px',
                slidesToShow: 3
            }
            },
            {
            breakpoint: 480,
            settings: {
                arrows: false,
                centerMode: true,
                swipeToSlide: true,
                slidesToShow: 2
            }
            },
            {
            breakpoint: 360,
            settings: {
                arrows: false,
                centerMode: true,
                swipeToSlide: true,
                slidesToShow: 1
            }
            },

        ]
    });
};
