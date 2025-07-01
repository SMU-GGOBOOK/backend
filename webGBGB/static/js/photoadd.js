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
          <input id="${id}" type="file" accept="image/*" />
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
      input.value = '';
    });

    removeBtn.addEventListener('click', () => {
      const bgImage = preview.style.backgroundImage;
      const url = bgImage.slice(5, -2); // "url('...')" 제거
      const index = attachedFiles.indexOf(url);

      if (index !== -1) {
        attachedFiles.splice(index, 1);
      }

      // 1. 현재 요소는 비워주기
      fileItem.classList.remove('attached');
      preview.style.backgroundImage = '';
      attachBox.style.display = 'none';
      li.querySelector('input').value = '';

      // 2. 오른쪽 요소가 빈 btn_box일 경우 삭제
      const nextLi = li.nextElementSibling;
      if (nextLi && !nextLi.querySelector('.file_item')?.classList.contains('attached')) {
        fileList.removeChild(nextLi);
      }
      updateAttachVal();

    });


    return li;
  }

  // 초기 1개 빈 박스 생성
  fileList.innerHTML = '';
  fileList.appendChild(createBtnBox(false, ''));
});
