let company_title = document.getElementById('company_title');
company_title.innerHTML = localStorage.getItem('company');

const doughnutChart = new Chart(document.getElementById('canvas-3'), {
  type: 'doughnut',
  data: {
    datasets: [{
      data: [70, 30],
      backgroundColor: ['#FF6384', 'transparent'],
      hoverBackgroundColor: ['#FF6384', 'transparent']
    }]
  },
  options: {
    responsive: true
  }
});
