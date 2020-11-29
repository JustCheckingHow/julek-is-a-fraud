
function capitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

function addToTable(company_data, key) {
  const companyDetailsTable = document.getElementById('company_details_table');
  let tr = document.createElement("TR");
  let td_name = document.createElement("TD");
  let td_value = document.createElement("TD");

  td_name.innerHTML = capitalizeFirstLetter(key).replace(/_/gi, ' ');

  if (company_data[key][0] === "[" && company_data[key].slice(-1) === "]") {
    company_data[key] = company_data[key].slice(1, -1);
  }
  td_value.innerHTML = company_data[key]
  tr.appendChild(td_name);
  tr.appendChild(td_value);
  companyDetailsTable.appendChild(tr);
}

function addToTableGen(company_data, key) {
  let tr = document.createElement("TR");
  let td_name = document.createElement("TD");
  let td_value = document.createElement("TD");

  td_name.innerHTML = capitalizeFirstLetter(key).replace(/_/gi, ' ');

  if (company_data[key][0] === "[" && company_data[key].slice(-1) === "]") {
    company_data[key] = company_data[key].slice(1, -1);
  }
  td_value.innerHTML = company_data[key]
  tr.appendChild(td_name);
  tr.appendChild(td_value);
  return tr;
}

let company_title = document.getElementById('company_title');
let company_data = JSON.parse(localStorage.getItem('company'));
company_title.innerHTML = company_data.name;
// 
// LOG THE SHIT
//

const alexaBoxRate = document.getElementById('alexa_box_rate');
const alexaBoxState = document.getElementById('alexa_box_state');
const alexaProgressbar = document.getElementById('alexa_progressbar');

let progress = (parseInt(company_data['AlexaRank']) * 100) / 4

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

scamWatcherLabel.innerHTML = company_data["Scamwatcher"] === 'True' ? "Found on ScamWatcher blacklist" : "Does not appear on ScamWatcher blacklist";
scamWatcherIcon.className = company_data["Scamwatcher"] === 'True' ? 'fa fa-exclamation-triangle' : 'fa fa-check-circle';

const inPolandValue = document.getElementById('in_poland_value');
if (!company_data["PolandCheck"]) {
  inPolandValue.innerHTML = '-'
}
else {
  inPolandValue.innerHTML = company_data["PolandCheck"] === 'True' ? "YES" : "NO";
}

addToTable(company_data, 'CompanyName');
company_data["WhoIs"] = company_data["WhoIs"]
  .slice(1, -1).replace(/'/gi, "\"")
  .replace(/False/gi, "\"False\"")
  .replace(/True/gi, "\"True\"")
  .replace(/\[/gi, "\"\[")
  .replace(/\]/gi, "\]\"");

if(company_data["WhoIs"]) {
  let who_is_company_data = JSON.parse(company_data["WhoIs"]);
  for (const [key, value] of Object.entries(who_is_company_data)) {
    addToTable(who_is_company_data, key);
  }
}

if(company_data["KNF_whitelist"]) {
  let knf_whitelist_table = JSON.parse(company_data["KNF_whitelist"]).slice(1, -1).replace(/'/gi, "\"")
      .replace(/False/gi, "\"False\"")
      .replace(/True/gi, "\"True\"");

  const knfListTable = document.getElementById('knf_list_table');
  for (const [key, value] of Object.entries(knf_whitelist)) {
    let tr = addToTableGen(knf_whitelist, key);
    knf_whitelist_table.appendChild(tr);
  }
}


const whiteList = document.getElementById('white_list');
whiteList.innerHTML = company_data['top_white'];

const inPolandReasonValue = document.getElementById('in_poland_reason_value');
if(company_data['Reason']) inPolandReasonValue.innerHTML = `because of ${company_data['Reason']}`;

const builtWithCard = document.getElementById('built_with_card');
builtWithCard.innerHTML = company_data['BuiltWith'].replace(/\{'programming-languages': \[\'/gi, "").replace(/\]\}/gi, "")