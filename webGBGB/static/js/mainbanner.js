$(document).ready(function(){
    //배너 슬라이드 script
    const bannerSwiper = new Swiper('.myBannerSwiper', {
        loop: true,                     // 무한 회전
        autoplay: {                     // 자동 재생 (원하면 지워도 됨)
        delay: 3000,
        disableOnInteraction: false,
        },
        pagination: {
        el: '.swiper-pagination',     // 우리가 HTML에 만든 div
        clickable: true,              // 불릿 클릭으로 이동
        },
    });
});//jquery