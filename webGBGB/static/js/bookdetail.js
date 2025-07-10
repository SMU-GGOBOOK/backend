// 북마크 버튼 js
function toggleBookmark(button) {
    const bookId = button.getAttribute('data-book-id');
    let cToken = $('meta[name="csrf-token"]').attr('content');
    const icon = button.querySelector('i');
    if (!icon) {
        console.warn('아이콘 없음');
        return;
    }

    $.ajax({
        url: '/bookmark/create/',
        type: 'post',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': cToken },
        data: JSON.stringify({ book_id: bookId }),
        success: function(data) {
            if (data.bookmarked !== undefined) {
                icon.classList.remove('fa-solid', 'fa-regular');
                icon.classList.add(data.bookmarked ? 'fa-solid' : 'fa-regular');
                button.classList.toggle('active', data.bookmarked);
            }
        },
        error: function() {
        }
    });

    // 애니메이션 효과는 성공 후에 처리하는 게 더 자연스러울 수 있습니다.
    icon.classList.add('fading-out');
    setTimeout(() => {
        icon.classList.remove('fading-out');
    }, 100);
}

document.addEventListener('DOMContentLoaded', () => {
  /* 글자수 체크 - 댓글 / 모달 통합 */
  document.querySelectorAll('.form_textarea').forEach(textarea => {
    textarea.addEventListener('input', () => {
      const count = textarea.closest('.reply_write_area, .modal')?.querySelector('.byte_check .count');
      if (count) count.textContent = textarea.value.length;
    });
  });

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

  /* 좋아요 */
  document.querySelectorAll('.btn_like').forEach(likeBtn => {
    likeBtn.addEventListener('click', function() {
      const reviewId = likeBtn.getAttribute('data-review-id');
      let cToken = $('meta[name="csrf-token"]').attr('content');
      const countEl = this.querySelector('.text');
      const icon = this.querySelector('i');
      let count = parseInt(countEl?.textContent || '0');
      const liked = this.classList.toggle('liked');
      icon?.classList.toggle('fa-solid', liked);
      icon?.classList.toggle('fa-regular', !liked);

      if (countEl) countEl.textContent = liked ? count + 1 : count - 1;


      $.ajax({
        url: '/review/like/',
        type: 'post',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': cToken },
        data: JSON.stringify({ review_id: reviewId, delta: liked ? 1 : -1 }),
        success: function(data) {
          if (data.likes !== undefined) {
            countEl.textContent = data.likes; // 서버에서 최신값 받아서 반영!
          }          
        },
        error: function(){
        }
      });
    });
  });
});

// 답글달기 토글 JS
// 페이지 내 모든 답글 버튼에 이벤트 연결
$(document).on('click', '.btn_reply', function () {
  console.log('btn_reply 클릭됨!');
  const $commentItem = $(this).closest('.comment_item');
  $commentItem.find('.reply_wrap').first().toggle();
});


// 모달 팝업 내 사진 추가
document.addEventListener('DOMContentLoaded', function () {
  const fileList = document.querySelector('.file_list');
  const MAX_FILES = 3;

  let attachedFiles = [];

  function generateId() {
    return 'file_' + Math.random().toString(36).slice(2);
  }

  function updateAttachVal() {
    const valElem = document.querySelector('.file_attach_val .total');
    if (valElem) {
      valElem.textContent = ` / ${MAX_FILES}`;
      const currentValElem = valElem.previousElementSibling;
      if (currentValElem && currentValElem.classList.contains('val')) {
        currentValElem.textContent = attachedFiles.length;
      }
    }
  }

  function createBtnBox(attached = false, imgSrc = '') {
    const id = generateId();

    const li = document.createElement('li');
    li.classList.add('list_item');
    li.innerHTML = `
      <span class="file_item ${attached ? 'attached' : ''}">
        <span class="btn_box">
          <input id="${id}" type="file" name="review_image" multiple/>
          <label for="${id}"><span class="hidden">첨부파일 추가</span></label>
          <span class="attach_img_box" style="display:${attached ? 'inline-block' : 'none'};">
            <span class="attach_img_view" style="background-image: url('${imgSrc}');"></span>
            <button class="btn_remove_img" type="button"><span class="hidden">첨부파일 삭제</span></button>
          </span>
        </span>
      </span>
    `;

    const input = li.querySelector('input[type="file"]');
    const removeBtn = li.querySelector('.btn_remove_img');
    const preview = li.querySelector('.attach_img_view');
    const attachBox = li.querySelector('.attach_img_box');
    const fileItem = li.querySelector('.file_item');

    input.addEventListener('change', () => {
      const file = input.files[0];
      if (!file) return;

      const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];

      if (!allowedTypes.includes(file.type)) {
        alert('이미지 파일(JPG, PNG, GIF)만 업로드 가능합니다.');
        input.value = '';
        return;
      }

      const reader = new FileReader();
      reader.onload = (e) => {
        const imgUrl = e.target.result;
        attachedFiles.push(imgUrl);

        // 1. 현재 btn_box를 attached로 변경
        fileItem.classList.add('attached');
        attachBox.style.display = 'inline-block';
        preview.style.backgroundImage = `url('${imgUrl}')`;

        // 2. 필요한 경우 오른쪽에 새 btn_box 추가
        const listItems = fileList.querySelectorAll('.list_item');
        if (attachedFiles.length < MAX_FILES) {
          const lastItem = listItems[listItems.length - 1];
          if (lastItem && lastItem === li) {
            const newBox = createBtnBox(false, '');
            fileList.appendChild(newBox);
          }
        }

        updateAttachVal();
      };
      reader.readAsDataURL(file);
    });

    removeBtn.addEventListener('click', () => {
      const bgImage = preview.style.backgroundImage;
      const url = bgImage.slice(5, -2);
      const index = attachedFiles.indexOf(url);
      if (index !== -1) attachedFiles.splice(index, 1);

      const allItems = Array.from(fileList.querySelectorAll('.list_item'));
      const currentIndex = allItems.indexOf(li);
      const nextLi = li.nextElementSibling;
      const lastLi = allItems[allItems.length - 1];

      // 오른쪽에 빈 사진추가 div 있는지 체크
      const hasRightEmptyDiv =
        nextLi &&
        !nextLi.querySelector('.file_item').classList.contains('attached');

      // 맨 끝이 빈 사진 추가 div인지 체크
      const lastIsEmpty =
        lastLi &&
        !lastLi.querySelector('.file_item').classList.contains('attached');

      if (hasRightEmptyDiv) {
        // 오른쪽에 빈 div 있으면 무조건 자기 삭제만
        fileList.removeChild(li);
      } else {
        if (currentIndex === 0) {
          // 첫 번째 div 삭제
          fileList.removeChild(li);
          // 맨 끝에 사진 추가 div 없으면 새로 추가
          if (!lastIsEmpty && attachedFiles.length < MAX_FILES) {
            fileList.appendChild(createBtnBox(false, ''));
          }
        } else if (currentIndex === 1) {
          // 두 번째 div 삭제
          fileList.removeChild(li);
          // 오른쪽에 빈 div 없으면 맨 끝에 새로 추가
          if (!hasRightEmptyDiv && attachedFiles.length < MAX_FILES) {
            fileList.appendChild(createBtnBox(false, ''));
          }
        } else if (currentIndex === 2) {
          // 세 번째 div: attached 제거, 내용 비우기
          fileItem.classList.remove('attached');
          preview.style.backgroundImage = '';
          attachBox.style.display = 'none';
          input.value = '';
        }
      }

      updateAttachVal();
    });




    return li;
  }

  // 초기 1개 빈 박스 생성
  fileList.innerHTML = '';
  fileList.appendChild(createBtnBox(false, ''));
  updateAttachVal();
});



/* 리뷰 답글 작성 */
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.reply_wrap').forEach(area => {
    const replyBtn = area.querySelector(".reply_btn");
    const textarea = area.querySelector(".reply_comments");
    const countSpan = area.querySelector('.reply_byte_check .count');
    const form = area.querySelector(".replyForm");

    console.log("초기 DOM 상태 확인:");
    console.log("textarea:", textarea);
    console.log("replyBtn:", replyBtn);
    console.log("countSpan:", countSpan);
    console.log("form:", form);


    function checkFormValid() {
      const reviewLength = textarea.value.trim().length;
      const reviewValid = reviewLength >= 10;
      replyBtn.disabled = !reviewValid;
      console.log("=== 유효성 검사 결과 ===");
      console.log("📝 리뷰 길이:", reviewLength, "-> 유효?", reviewValid);
      console.log("🔒 버튼 활성화됨?", reviewValid);
      if (countSpan) countSpan.textContent = reviewLength;
    }

    textarea.addEventListener("input", checkFormValid);

    function resetReplyForm() {
      textarea.value = "";
      if (countSpan) countSpan.textContent = "0";
      replyBtn.disabled = true;
    }

    // 버튼 클릭 시 알림 + 모달 닫기 + 초기화
    replyBtn.addEventListener("click", () => {
      // 유효하면 등록 처리
      alert("리뷰 등록이 완료되었습니다");

      // 폼 제출
      if (form) {
        form.submit();
      }
      resetReplyForm();
    });
  });
  checkFormValid();
});

document.addEventListener("DOMContentLoaded", () => {
  // 별점 바인딩 함수 (컨테이너별)
  function bindStarRating(container) {
    const stars = container.querySelectorAll(".rating-stars-review .star");
    const input = container.querySelector("input[type='hidden'][name='rating']");
    const valSpan = container.querySelector(".caption-review .val");
    const textSpan = container.querySelector(".caption-review-badge span > span:first-child");
    let currentValue = parseInt(input?.value || "0");

    function updateStars(value) {
      stars.forEach((s, idx) => {
        s.classList.toggle("active", idx < value);
      });
      if (input) input.value = value;
      if (valSpan) valSpan.textContent = value;
      if (textSpan) textSpan.textContent = `5점 중 ${value}점`;
      currentValue = value;
    }

    stars.forEach((star, idx) => {
      const hoverValue = idx + 1;
      star.addEventListener("mouseenter", function () {
        stars.forEach((s, i) => {
          s.classList.toggle("active", i < hoverValue);
        });
        if (input) input.value = hoverValue;
        if (valSpan) valSpan.textContent = hoverValue;
        if (textSpan) textSpan.textContent = `5점 중 ${hoverValue}점`;
      });
      star.addEventListener("mouseleave", function () {
        updateStars(currentValue);
      });
      star.addEventListener("click", function () {
        const newValue = idx + 1;
        stars.forEach((s, i) => {
          const shouldFade = (i < currentValue && i >= newValue) || (i >= currentValue && i < newValue);
          if (shouldFade) s.classList.add("fading-out");
        });
        setTimeout(() => {
          updateStars(newValue);
          stars.forEach(s => s.classList.remove("fading-out"));
        }, 120);
      });
    });
    updateStars(currentValue);
  }

  // 폼 바인딩 함수 (작성/수정 모달 모두 사용)
  function bindModalForm(modalId, formId, textareaId, ratingInputSelector, tagSelector, btnId) {
    const modal = document.getElementById(modalId);
    const form = document.getElementById(formId);
    const modalBtn = modal.querySelector(`#${btnId}`);
    const textarea = modal.querySelector(`#${textareaId}`);
    const ratingInput = modal.querySelector(ratingInputSelector);

    // 별점 세팅 함수
    function setRating(value) {
      ratingInput.value = value;
      const stars = modal.querySelectorAll(".rating-stars-review .star");
      stars.forEach((s, idx) => {
        s.classList.toggle("active", idx < value);
      });
      const valSpan = modal.querySelector(".caption-review .val");
      const textSpan = modal.querySelector(".caption-review-badge span > span:first-child");
      if (valSpan) valSpan.textContent = value;
      if (textSpan) textSpan.textContent = `5점 중 ${value}점`;
    }

    // 폼 초기화
    function resetForm() {
      setRating(0);
      // 태그 초기화
      modal.querySelectorAll('.tag_wrap.size_lg .tag.active').forEach(tag => tag.classList.remove("active"));
      // textarea 초기화
      if (textarea) textarea.value = "";
      const counter = modal.querySelector(".byte_check .count");
      if (counter) counter.textContent = "0";
      // 버튼 비활성화
      if (modalBtn) modalBtn.disabled = true;
      // 태그 input 값도 초기화
      const tagInput = modal.querySelector("input[name='tag']");
      if (tagInput) tagInput.value = "";
    }

    // 폼 값 세팅 (수정 모달용)
    function setFormData({ rating, tag, reviewText }) {
      if (typeof rating !== "undefined") setRating(parseInt(rating));
      // 태그
      if (tag) {
        modal.querySelectorAll('.tag_wrap.size_lg .tag').forEach(btn => {
          const tagText = btn.querySelector('.text')?.textContent.trim();
          if (tagText === tag) btn.classList.add("active");
          else btn.classList.remove("active");
        });
        // input[name='tag'] 값도 세팅
        const tagInput = modal.querySelector("input[name='tag']");
        if (tagInput) tagInput.value = tag;
      }
      // 텍스트
      if (textarea && typeof reviewText !== "undefined") {
        textarea.value = reviewText;
        const counter = modal.querySelector(".byte_check .count");
        if (counter) counter.textContent = reviewText.length;
      }
      checkFormValid();
    }

    // 유효성 검사
    function checkFormValid() {
      const ratingVal = parseInt(ratingInput?.value || "0");
      const ratingValid = ratingVal > 0;
      const tagSelected = modal.querySelector('.tag_wrap.size_lg .tag.active') !== null;
      const reviewLength = textarea?.value.trim().length || 0;
      const reviewValid = reviewLength >= 10;
      if (modalBtn) modalBtn.disabled = !(ratingValid && tagSelected && reviewValid);
    }

    // textarea 입력
    if (textarea) {
      textarea.addEventListener("input", () => {
        const len = textarea.value.length;
        const counter = modal.querySelector(".byte_check .count");
        if (counter) counter.textContent = len;
        checkFormValid();
      });
    }

    // 별점 클릭
    modal.querySelectorAll(".rating-stars-review .star").forEach(star => {
      star.addEventListener("click", () => checkFormValid());
    });

    // 태그 클릭
    modal.querySelectorAll('.tag_wrap.size_lg .tag').forEach(tag => {
      tag.addEventListener("click", () => {
        modal.querySelectorAll('.tag_wrap.size_lg .tag').forEach(btn => btn.classList.remove("active"));
        tag.classList.add("active");
        // input[name='tag'] 값도 변경
        const tagInput = modal.querySelector("input[name='tag']");
        if (tagInput) tagInput.value = tag.querySelector('.text')?.textContent.trim();
        checkFormValid();
      });
    });

    // 별점 바인딩
    const ratingContainer = modal.querySelector('.rating-container');
    if (ratingContainer) bindStarRating(ratingContainer);

    // 외부에서 호출할 수 있게 반환
    return { resetForm, setFormData, checkFormValid, setRating };
  }

  // === 작성 모달 바인딩 ===
  const reviewModalApi = bindModalForm(
    "reviewModal",          // 모달 ID
    "reviewForm",           // 폼 ID
    "review_comments",      // textarea ID
    "input[name='rating']", // 별점 input selector
    "input[name='tag']",    // 태그 input selector
    "review_btn"            // 등록 버튼 ID
  );

  // === 수정 모달 바인딩 ===
  const modifyModalApi = bindModalForm(
    "modifyModal",
    "modifyForm",
    "modify_comments",
    "input[name='rating']",
    "input[name='tag']",
    "modify_btn"
  );

  // 작성 모달 열기/닫기 버튼
  document.getElementById("openReviewBtn")?.addEventListener('click', () => {
    document.getElementById("reviewModal")?.classList.add('active');
    reviewModalApi.resetForm();
  });
  document.getElementById("closeReviewBtn")?.addEventListener('click', () => {
    document.getElementById("reviewModal")?.classList.remove('active');
    reviewModalApi.resetForm();
  });

  // 수정 모달 열기 버튼: data-* 값 세팅
  document.querySelectorAll('.modifyReviewBtn').forEach(btn => {
    btn.addEventListener('click', function() {
      let reviewData = {};
      try {
        reviewData = JSON.parse(btn.dataset.review);
      } catch (err) {
        alert("리뷰 데이터 파싱 오류!");
        return;
      }
      const modal = document.getElementById("modifyModal");
      modal?.classList.add('active');

      // 별점, 태그, 내용 등 값 세팅
      modifyModalApi.resetForm();
      modifyModalApi.setFormData({
        rating: reviewData.rating,
        tag: reviewData.tag,
        reviewText: reviewData.content
      });

      // review_id hidden input
      const reviewIdInput = modal.querySelector("#modal_review_id");
      if (reviewIdInput) reviewIdInput.value = reviewData.review_id;
    });
  });

  document.getElementById("closeModifyBtn")?.addEventListener('click', () => {
    document.getElementById("modifyModal")?.classList.remove('active');
    modifyModalApi.resetForm();
  });

  // ESC로 모달 닫기
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      document.getElementById("reviewModal")?.classList.remove('active');
      reviewModalApi.resetForm();
      document.getElementById("modifyModal")?.classList.remove('active');
      modifyModalApi.resetForm();
    }
  });

  // ========== 여기서부터는 작성/수정 모달 각각 분리된 등록 버튼 이벤트! ==========

  // 작성 모달 등록 버튼
  document.getElementById('review_btn')?.addEventListener('click', function(e) {
    if (this.disabled) {
      e.preventDefault();
      return;
    }
    alert("리뷰가 등록되었습니다."); // 작성에만!
    document.getElementById('reviewForm').submit();
  });

  // 수정 모달 등록 버튼
  document.getElementById('modify_btn')?.addEventListener('click', function(e) {
    if (this.disabled) {
      e.preventDefault();
      return;
    }
    alert("리뷰가 수정되었습니다."); // 수정에만!
    document.getElementById('modifyForm').submit();
  });

});