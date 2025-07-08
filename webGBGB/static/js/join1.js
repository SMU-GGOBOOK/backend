document.getElementById("agreeFrm").addEventListener("submit", function(event) {
      const checkboxes = document.querySelectorAll(".saveAgree");
      const allChecked = Array.from(checkboxes).every(checkbox => checkbox.checked);

      if (!allChecked) {
        event.preventDefault(); // 제출 중단
        alert("모든 약관에 동의해야 가입할 수 있습니다.");
      }
    });