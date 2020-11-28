function onSearch() {
  let input = document.getElementById('search_input');
  console.log(input.value);
  if(input.value) {
    localStorage.setItem('search', input.value);
    location.href = 'home.html';
  }
}
