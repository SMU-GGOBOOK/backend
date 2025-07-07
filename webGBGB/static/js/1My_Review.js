


/*
// 모든 삭제 버튼에 클릭 이벤트 연결
document.querySelectorAll('.deleteBtn').forEach(button => {
  button.addEventListener('click', function () {
    const comment_item = this.closest('.comment_item');

    // 리뷰박스에서 삭제버튼 클릭하면 삭제
    if (comment_item) {
      const shouldDelete = confirm("리뷰를 삭제하시겠습니까?");
      if (shouldDelete) {
        comment_item.remove();
      }
    }
  });
});*/


//리뷰박스 삭제 요청 및 삭제 스크립트
// $(document).on('click', '.deleteBtn', function() {
//   const $commentItem = $(this).closest('.comment_item');
//   const reviewId = $commentItem.data('id'); // HTML에서 data-id로 지정된 값
//   const cToken = $('meta[name="csrf-token"]').attr('content');

//   if (!confirm('정말 삭제하시겠습니까?')) return;

//   $.ajax({
//     url: '/ajaxData/review_delete/',  // 백엔드 URL에 맞게 수정
//     type: 'post',
//     headers: { 'X-CSRFToken': cToken },
//     data: { 'review_id': reviewId },
//     success: function(data) {
//       if (data.result === 'success') {
//         $commentItem.remove(); // DOM에서 제거
//       } else {
//         alert('삭제 실패: ' + data.message);
//       }
//     },
//     error: function() {
//       alert('서버 오류');
//     }
//   });
// });


// 리뷰박스 클릭시 상세페이지 

// document.addEventListener('DOMContentLoaded', function () {
//   document.querySelectorAll('.comment_item').forEach(function (element) {
//     element.addEventListener("click", function (e) {
//       // 버튼 클릭이면 무시
//       if (e.target.closest("button")) return; // 삭제 버튼 같은 건 제외
      
//       // 페이지 이동
//       const reviewId = this.dataset.reviewId;
//       if (reviewId) {
//         window.location.href = `/books/${reviewId}/`; // ← 여길 실제 경로에 맞게
//       }
//     });
//   });
// });



document.addEventListener('DOMContentLoaded', () => {

  /* 펼치기 */
  document.querySelectorAll('.comment_item').forEach(item => {
    const moreBtn = item.querySelector('.btn_more_body');
    if (!moreBtn) return;

    if (item.classList.contains('overflow')) {
      moreBtn.style.display = 'block';
    } else {
      moreBtn.style.display = 'none';
    }

    moreBtn.addEventListener('click', () => {
      const isActive = item.classList.toggle('active');
      moreBtn.classList.toggle('active', isActive);
      moreBtn.querySelector('.text').textContent = isActive ? '접기' : '펼치기';

      const icon = moreBtn.querySelector('i');
      if (icon) {
        icon.classList.toggle('fa-circle-arrow-up', isActive);
        icon.classList.toggle('fa-circle-arrow-down', !isActive);
      }

      const thumb = item.querySelector('.comment_thumb_box');
      const swiper = item.querySelector('.comment_swiper_wrap');
      if (thumb && swiper) {
        thumb.style.display = isActive ? 'none' : 'block';
        swiper.style.display = isActive ? 'block' : 'none';
      }
    });
  });

  // /* 별점 */
  // const stars = document.querySelectorAll(".rating-stars-review .star");
  // const input = document.getElementById("rating-value-review");
  // const valSpan = document.querySelector(".caption-review .val"); // 오타 반영
  // const textSpan = document.querySelector(".caption-review-badge span > span:first-child");
  // const visibleRatingInput = document.querySelector(".form_rating.rating-input"); // 🔹 추가된 라인

  // let currentValue = parseInt(input.value || "0");

  // function updateStars(value) {
  //   stars.forEach((s, idx) => {
  //     s.classList.toggle("active", idx < value);
  //   });

  //   if (input) input.value = value;
  //   if (visibleRatingInput) visibleRatingInput.value = value; // 🔹 여기에 추가!
  //   if (valSpan) valSpan.textContent = value;
  //   if (textSpan) textSpan.textContent = `5점 중 ${value}점`;

  //   currentValue = value; // 현재 점수 저장
  // }

  // stars.forEach((star, idx) => {
  //   const hoverValue = idx + 1;

  //   star.addEventListener("mouseenter", function () {
  //     stars.forEach((s, i) => {
  //       s.classList.toggle("active", i < hoverValue);
  //     });

  //     if (input) input.value = hoverValue;
  //     if (valSpan) valSpan.textContent = hoverValue;
  //     if (textSpan) textSpan.textContent = `5점 중 ${hoverValue}점`;
  //   });

  //   star.addEventListener("mouseleave", function () {
  //     updateStars(currentValue); // 마우스 빠질 때 기존 값으로 복원
  //   });

  //   star.addEventListener("click", function () {
  //   const newValue = idx + 1;

  //   stars.forEach((s, i) => {
  //     const shouldFade = (i < currentValue && i >= newValue) || (i >= currentValue && i < newValue);
  //     if (shouldFade) s.classList.add("fading-out");
  //   });

  //   setTimeout(() => {
  //     updateStars(newValue);
  //     stars.forEach(s => s.classList.remove("fading-out"));
  //   }, 120);
  // });
  // ;
  // });

  // 초기 세팅
  // updateStars(currentValue);

  /* 이미지 썸네일 클릭 시 Swiper 보기 */
  document.querySelectorAll('.comment_thumb_box').forEach(box => {
    box.addEventListener('click', () => {
      const item = box.closest('.comment_item');
      if (item) {
        item.classList.add('overflow', 'active');
        const thumb = item.querySelector('.comment_thumb_box');
        const swiper = item.querySelector('.comment_swiper_wrap');
        if (thumb) thumb.style.display = 'none';
        if (swiper) swiper.style.display = 'block';
      }
    });
  });
    //   // 모든 swiper-container 초기화
    // document.querySelectorAll('.swiper-container').forEach((container, idx) => {
    //   new Swiper(container, {
    //     loop: true,
    //     navigation: {
    //       nextEl: container.closest('.comment_swiper_wrap').querySelector('.swiper-button-next'),
    //       prevEl: container.closest('.comment_swiper_wrap').querySelector('.swiper-button-prev'),
    //     },
    //     pagination: {
    //       el: container.closest('.comment_swiper_wrap').querySelector('.swiper-pagination'),
    //       clickable: true,
    //     },
    //   });
    // });







});







