$(document).ready(function () {
  $('.comment_item').each(function () {
    const $commentItem = $(this);
    const $moreButton = $commentItem.find('.btn_more_body');

    // 내용이 긴 경우만 버튼 보여줌
    if ($commentItem.hasClass('overflow')) {
      $moreButton.show();
    } else {
      $moreButton.hide();
    }
  });

  $('.btn_more_body').on('click', function () {
    const $button = $(this);
    const $commentItem = $button.closest('.comment_item');
    const isActive = $commentItem.hasClass('active');

    if (!isActive) {
      // 펼치기
      $commentItem.addClass('active');
      $button.addClass('active');
      $button.find('.text').text('접기');
      $button.find('i').removeClass('fa-circle-arrow-down').addClass('fa-circle-arrow-up');

      // 썸네일 숨기고 swiper 보이게
      $commentItem.find('.comment_thumb_box').hide();
      $commentItem.find('.comment_swiper_wrap').show();

    } else {
      // 접기
      $commentItem.removeClass('active');
      $button.removeClass('active');
      $button.find('.text').text('펼치기');
      $button.find('i').removeClass('fa-circle-arrow-up').addClass('fa-circle-arrow-down');

      // swiper 숨기고 썸네일 보이게
      $commentItem.find('.comment_swiper_wrap').hide();
      $commentItem.find('.comment_thumb_box').show();
    }
  });
});



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
$(document).on('click', '.deleteBtn', function() {
  const $commentItem = $(this).closest('.comment_item');
  const reviewId = $commentItem.data('id'); // HTML에서 data-id로 지정된 값
  const cToken = $('meta[name="csrf-token"]').attr('content');

  if (!confirm('정말 삭제하시겠습니까?')) return;

  $.ajax({
    url: '/ajaxData/review_delete/',  // 백엔드 URL에 맞게 수정
    type: 'post',
    headers: { 'X-CSRFToken': cToken },
    data: { 'review_id': reviewId },
    success: function(data) {
      if (data.result === 'success') {
        $commentItem.remove(); // DOM에서 제거
      } else {
        alert('삭제 실패: ' + data.message);
      }
    },
    error: function() {
      alert('서버 오류');
    }
  });
});










