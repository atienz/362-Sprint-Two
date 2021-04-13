let currentTheme;

window.addEventListener('load', (event) => {
    console.log('page is fully loaded');
    currentTheme = document.getElementById("theme-link");
    console.log(currentTheme.getAttribute('href'));
  });

function clicked(){
    if(currentTheme.getAttribute('href') == '/static/light-theme.css'){
        currentTheme.setAttribute('href', '/static/dark-theme.css');
    }else{
      // do the opposite here
      currentTheme.setAttribute('href', '/static/light-theme.css');
    }
}
