setTimeout(() => {
    Array.from(document.getElementsByClassName("temporary")).forEach(element => {
        element.style.display = "none";
    });
}, 2500);

function toggle_arrow(button) {
    var svg = button.getElementsByTagName('svg')[0];

    if (svg.classList.contains('bi-caret-down')) {
        svg.classList.remove('bi-caret-down');
        svg.classList.add('bi-caret-up-fill');
        svg.innerHTML = '<path d="m7.247 4.86-4.796 5.481c-.566.647-.106 1.659.753 1.659h9.592a1 1 0 0 0 .753-1.659l-4.796-5.48a1 1 0 0 0-1.506 0z"/>';
    } else {
        svg.classList.remove('bi-caret-up-fill');
        svg.classList.add('bi-caret-down');
        svg.innerHTML = '<path d="M3.204 5h9.592L8 10.481zm-.753.659 4.796 5.48a1 1 0 0 0 1.506 0l4.796-5.48c.566-.647.106-1.659-.753-1.659H3.204a1 1 0 0 0-.753 1.659"/>';
    }
}
