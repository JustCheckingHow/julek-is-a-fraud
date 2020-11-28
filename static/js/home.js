function onSearch() {
  let input = document.getElementById('search_input');
  if(input.value) {
    localStorage.setItem('search', input.value);
    getResult(input.value);
  }
}

function getResult(value) {
  let loader = document.getElementById('loader');
  loader.style.display = 'block';

  $.ajax({
    url: `http://127.0.0.1:5000/get_record?name=${value}`,
    type: "GET",
    success: (response) => {
      loader.style.display = 'none';
      displayList(response);
    },
    error: function(result) {
      console.log('error');
    }
  });

}

function displayList(data) {
  let result = [data];
  let list = document.getElementById('search_list');
  list.innerHTML = '';

  result.map(el => {
    let btn = document.createElement("BUTTON");
    btn.innerHTML = '<div>\n' +
                    `<div style="float: left; padding: 2%;">${el.name}</div>\n` +
                    '  <div class="card-body" style="width: 20%; float: right">\n' +
                    '    <div class="progress progress-xs my-2" style="background: white !important">\n' +
                    '      <div class="progress-bar bg-info" role="progressbar" style="width: 40%;" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>\n' +
                    '    </div>\n' +
                    '    <small>Trust rate</small>\n' +
                    '    <small style="float: right">12</small>\n' +
                    '  </div>\n' +
                  '  </div>';
    btn.className = "list-group-item list-group-item-action";
    btn.type = "text";
    btn.onclick = () => onRecordSelected(el);
    btn.style.color = "black";
    btn.style.borderColor = "#7c7c7c";
    btn.style.fontSize = "130%";
    btn.style.width = "80%";
    btn.style.margin = "auto";
    btn.style.boxShadow = "0px 8px 15px rgba(0, 0, 0, 0.2)";
    list.appendChild(btn);
  });
}

function onRecordSelected(el) {
  localStorage.setItem('company', JSON.stringify(el));
  location.href = 'company.html';
}

let search_value = localStorage.getItem('search');
document.getElementById('search_input').value = search_value;
onSearch();
