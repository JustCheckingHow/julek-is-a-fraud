let company_title = document.getElementById('company_title');
let company_data = JSON.parse(localStorage.getItem('company'));
console.log(company_data)
company_title.innerHTML = company_data.name;

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

const alexaBoxRate = document.getElementById('alexa_box_rate');
const alexaBoxState = document.getElementById('alexa_box_state');
const alexaProgressbar = document.getElementById('alexa_progressbar');

let progress = (parseInt(company_data['AlexaRank']) * 100)/4
alexaProgressbar.style.width = `${progress.toString()}%`;

alexaBoxRate.innerHTML = company_data['AlexaRank'];

if (parseInt(company_data['AlexaRank']) === 0) {
  alexaBoxState.innerHTML = "high risk";
}
else if (parseInt(company_data['AlexaRank']) === 1) {
  alexaBoxState.innerHTML = "moderate risk";
}
else if (parseInt(company_data['AlexaRank']) === 2) {
  alexaBoxState.innerHTML = "low risk";
}
else if (parseInt(company_data['AlexaRank']) === 3) {
  alexaBoxState.innerHTML = "very low risk";
}
else if (parseInt(company_data['AlexaRank']) === 4) {
  alexaBoxState.innerHTML = "not indexed risk";
}

const scamWatcherIcon = document.getElementById('scam_watcher_icon');
const scamWatcherLabel = document.getElementById('scam_watcher_label');

scamWatcherLabel.innerHTML = company_data["Scamwatcher"] === 'True' ? "Found on ScamWatcher blacklist": "Does not appear on ScamWatcher blacklist";
scamWatcherIcon.className = company_data["Scamwatcher"] === 'True' ? 'fa fa-exclamation-triangle': 'fa fa-check-circle';

const inPolandValue = document.getElementById('in_poland_value');

if (!company_data["in_poland"]){
  inPolandValue.innerHTML = '-'
}
else {
  inPolandValue.innerHTML = company_data["in_poland"] === 'True' ? "YES": "NO";
}
