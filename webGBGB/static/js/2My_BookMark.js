
// // 모든 북마크된 버튼에 클릭 이벤트 연결
// document.querySelectorAll('.bookmarkBtn').forEach(button => {
// button.addEventListener('click', function () {
// const bookbox = this.closest('.bookbox');

// // 북마크된 책에서 클릭하면 삭제
// if (bookbox) {
//     const shouldDelete = confirm("북마크를 삭제하시겠습니까?");
//     if (shouldDelete) {
//     bookbox.remove();
//     }
// }
// });
// });




$(document).on('click', '.bookmarkBtn', function() {
  const $bookBox = $(this).closest('.bookbox');
  const bookmarkId = $bookBox.data('id'); // HTML에서 data-id로 지정된 값
  const cToken = $('meta[name="csrf-token"]').attr('content');

  if (!confirm('정말 삭제하시겠습니까?')) return;

  $.ajax({
    url: '/mypage/bookmark_delete/',  // 백엔드 URL에 맞게 수정
    type: 'post',
    headers: { 'X-CSRFToken': cToken },
    data: { 'bookmark_id': bookmarkId },
    success: function(data) {
      if (data.result === 'success') {
        $bookBox.remove(); // DOM에서 제거
      } else {
        alert('삭제 실패: ' + data.message);
      }
    },
    error: function() {
      alert('서버 오류');
    }
  });
});