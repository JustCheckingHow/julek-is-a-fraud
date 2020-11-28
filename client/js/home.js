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
    url: "http://127.0.0.1:5000/",
    type: "GET",
    success: (el) => {
      loader.style.display = 'none';
      displayList();
    },
    error: function(result) {
      console.log('error');
    }
  });

}

function displayList() {
  let mock = ['test', 'test', 'test', 'test', 'test', 'test'];
  let list = document.getElementById('search_list');
  list.innerHTML = '';

  mock.map(el => {
    let btn = document.createElement("BUTTON");
    btn.innerHTML = el;
    btn.className = "list-group-item list-group-item-action";
    btn.type = "text";
    btn.onclick = () => onRecordSelected(el);
    list.appendChild(btn);
  });
}

function onRecordSelected(el) {
  localStorage.setItem('company', el);
  location.href = 'company.html';
}

let search_value = localStorage.getItem('search');
document.getElementById('search_input').value = search_value;
onSearch();
