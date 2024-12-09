let startX = 0;
let endX = 0;
let SLIDE_WIDTH = 50

function openTab(evt, tabName) {
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(content => content.classList.remove('active'));

    const tabLinks = document.querySelectorAll('.tab-link');
    tabLinks.forEach(link => link.classList.remove('active'));

    document.getElementById(tabName).classList.add('active');
    evt?.currentTarget?.classList.add('active');
}

const mapElement = document.getElementById('map');

function switchTab(direction) {
    const activeTab = document.querySelector('.tab-link.active');
    const tabs = Array.from(document.querySelectorAll('.tab-link'));

    let currentIndex = tabs.indexOf(activeTab);
    let newIndex = currentIndex;

    if (direction === 'left') {
        newIndex = currentIndex + 1;
        if(newIndex > tabs.length - 1){
            newIndex = 0;
        }
    } else if (direction === 'right') {
        newIndex = currentIndex - 1;
        if(newIndex < 0){
            newIndex = tabs.length - 1;
        }
    }

    if (newIndex !== currentIndex) {
        tabs[newIndex].click();
    }
}

document.addEventListener('touchstart', (e) => {
    endX = e.touches[0].clientX;
    startX = e.touches[0].clientX;
});

document.addEventListener('touchend', (e) => {
    let direction = '';
    const endX = e.changedTouches[0].clientX;

    if(!mapElement.contains(e.target)) {
        if (startX - endX > SLIDE_WIDTH) {
            direction = 'left';
        } else if (endX - startX > SLIDE_WIDTH) {
            direction = 'right';
        }
    }

    if (direction) {
        switchTab(direction);
    }

    startX = e.touches[0].clientX;
});