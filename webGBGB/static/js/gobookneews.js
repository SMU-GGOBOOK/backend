// 차트 인스턴스 저장용
const chartInstances = {};

function drawChart(url, canvasId, type, label = "", bgColor = "#3498db", borderColor = "#3498db") {
  // 기존 차트 파괴
  if (chartInstances[canvasId]) {
    chartInstances[canvasId].destroy();
  }

  fetch(url)
    .then(res => {
      if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
      return res.json();
    })
    .then(data => {
      // 데이터 검증
      if (!data || !data.labels || !data.data) {
        console.error('Invalid data format:', data);
        return;
      }

      const ctx = document.getElementById(canvasId);
      if (!ctx) {
        console.error(`Canvas element not found: ${canvasId}`);
        return;
      }

      // 차트 생성 및 인스턴스 저장
      chartInstances[canvasId] = new Chart(ctx, {
        type: type,
        data: {
          labels: data.labels,
          datasets: [{
            label: label,
            data: data.data,
            backgroundColor: type === "pie" || type === "doughnut" || type === "bar"
              ? generateColors(data.data.length)
              : bgColor,
            borderColor: type === "pie" || type === "doughnut"
              ? generateColors(data.data.length)
              : borderColor,
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          indexAxis: type === "bar" ? 'y' : 'x',
          plugins: {
            legend: { display: false }
          },
          scales: type === "line" || type === "bar" ? {
            y: { beginAtZero: true }
          } : {}
        }
      });
    })
    .catch(error => {
      console.error('Chart loading error:', error);
    });
}

// 페이지 로드 시 차트 그리기 예시
document.addEventListener('DOMContentLoaded', () => {
  const urlParams = new URLSearchParams(window.location.search);
  const year = urlParams.get('year') || new Date().getFullYear();
  const month = urlParams.get('month') || (new Date().getMonth() + 1);
  // select에서 선택되게 만들기
  const select = document.getElementById('ctgr_inq');
  if (select) {
    const valueToSelect = `${year}-${month.toString().padStart(2, '0')}`;
    select.value = valueToSelect;
  }

  drawAllCharts(year, month);
});


function drawAllCharts(year, month) {
  // 1) 가입인원 추이 (선형 차트)
  drawChart(`/neews/chart/join/?year=${year}&month=${month}`, 'joinChart', 'line', '가입 인원');

  // 2) 선호 장르 (원형 차트)
  drawChart(`/neews/chart/genre/?year=${year}&month=${month}`, 'genChart', 'bar', '선호 장르');

  // 3) 교환독서 그룹 생성 추이 (선형 차트)
  drawChart(`/neews/chart/share/?year=${year}&month=${month}`, 'shareChart', 'line', '교환독서 그룹 생성');

  // 4) 
  drawChart(`/neews/chart/tag/?year=${year}&month=${month}`, 'sharetagChart', 'doughnut', '이달의 태그');

  // 5) 리뷰 작성 수 추이 ()
  drawChart(`/neews/chart/review/?year=${year}&month=${month}`, 'reviewChart', 'line', '리뷰 수');

}


function generateColors(num) {
  const colors = [
    '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
    '#FF9F40', '#66FF66', '#FF6666', '#6699FF', '#FFCC99'
  ];
  return Array.from({length: num}, (_, i) => colors[i % colors.length]);
}

document.getElementById('applyBtn').addEventListener('click', function () {
  const value = document.getElementById('ctgr_inq').value;
  const [year, month] = value.split('-');
  window.location.href = `/neews/?year=${year}&month=${month}`;
});