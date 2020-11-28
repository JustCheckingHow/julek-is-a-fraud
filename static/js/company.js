function capitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

function addToTable(company_data, key) {
  let tr = document.createElement("TR");
  let td_name = document.createElement("TD");
  let td_value = document.createElement("TD");

  td_name.innerHTML = capitalizeFirstLetter(key);

  if (company_data[key][0] === "[" && company_data[key].slice(-1) === "]") {
    company_data[key] = company_data[key].slice(1, -1);
  }
  td_value.innerHTML = company_data[key]
  tr.appendChild(td_name);
  tr.appendChild(td_value);
  companyDetailsTable.appendChild(tr);
}


let company_title = document.getElementById('company_title');
let company_data = JSON.parse(localStorage.getItem('company'));
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

const companyDetailsTable = document.getElementById('company_details_table');


addToTable(company_data, "Company Name");
addToTable(company_data, "webpage");
addToTable(company_data, "WhoIs");


// const webPage = document.getElementById('web_page');
// webPage.innerHTML = company_data['webpage'].slice(1, -1);
//
// const whoIs = document.getElementById('who_is');
// whoIs.innerHTML = company_data['WhoIs'].slice(1, -1);