
// const toggle = document.querySelector('.toggle');
// const navLinks = document.querySelector('.nav-links');
// console.log(navLinks);
// toggle.addEventListener('click', () => {
//     navLinks.classList.toggle('active');
// });




const toggleButton = document.getElementsByClassName('toggle-button')[0]
const navbarLinks = document.getElementsByClassName('navbar-links')[0]

toggleButton.addEventListener('click', () => {
  navbarLinks.classList.toggle('active')
})