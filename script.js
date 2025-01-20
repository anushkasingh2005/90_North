// script.js
function toggleMenu() {
    const leftMenu = document.getElementById('leftMenu');
    leftMenu.classList.toggle('collapsed');
}

function adjustPageSize() {
    const screenWidth = window.innerWidth;
    let scale = 1;

    if (screenWidth >= 992 && screenWidth <= 1600) {
        scale = 0.9;
    } else if (screenWidth >= 700 && screenWidth <= 767) {
        scale = 0.8;
    } else if (screenWidth >= 600 && screenWidth < 700) {
        scale = 0.75;
    } else if (screenWidth <= 600) {
        scale = 0.5;
    }

    document.body.style.transform = `scale(${scale})`;
    document.body.style.transformOrigin = 'top left';
}

window.addEventListener('resize', adjustPageSize);
window.addEventListener('load', adjustPageSize); // Call on load as well