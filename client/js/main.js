function onSearch() {
  let input = document.getElementById('search_input');
  if(input.value) {
    localStorage.setItem('search', input.value);
    location.href = 'home.html';
  }
}

