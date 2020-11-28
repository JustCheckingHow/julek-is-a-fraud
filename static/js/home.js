function onSearch() {
  let input = document.getElementById('search_input');
  if(input.value) {
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
  let mock = [data];
  let list = document.getElementById('search_list');
  list.innerHTML = '';

  mock.map(el => {
    let btn = document.createElement("BUTTON");
    btn.innerHTML = el.name;
    btn.className = "list-group-item list-group-item-action";
    btn.type = "text";
    btn.onclick = () => onRecordSelected(el);
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
