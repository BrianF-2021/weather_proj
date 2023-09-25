
const toggle = document.querySelector('.toggle');
const navLinks = document.querySelector('.nav-links');
console.log(navLinks);
toggle.addEventListener('click', () => {
    navLinks.classList.toggle('active');
});