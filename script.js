// Плавный скролл
function closeMobileMenu() {
  document.getElementById('mobileMenu').classList.remove('open');
  document.getElementById('burgerBtn').classList.remove('active');
  document.getElementById('burgerBtn').setAttribute('aria-expanded', 'false');
  document.getElementById('mobileMenu').setAttribute('aria-hidden', 'true');
  document.getElementById('mobileMenuBackdrop').style.display = 'none';
}
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    const menu = document.getElementById('mobileMenu');
    if (window.innerWidth <= 600 && menu.classList.contains('open')) {
      closeMobileMenu();
    }
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth' });
    }
  });
});
// Анимация появления блоков
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('show');
    }
  });
}, { threshold: 0.1 });
document.querySelectorAll('.feature, .advantage, .team__member, .review, .faq__item, .start__block').forEach(el => {
  observer.observe(el);
});
// Мобильное меню
const burgerBtn = document.getElementById('burgerBtn');
const mobileMenu = document.getElementById('mobileMenu');
const mobileMenuBackdrop = document.getElementById('mobileMenuBackdrop');
burgerBtn.addEventListener('click', function() {
  const isOpen = mobileMenu.classList.toggle('open');
  burgerBtn.classList.toggle('active', isOpen);
  burgerBtn.setAttribute('aria-expanded', isOpen);
  mobileMenu.setAttribute('aria-hidden', !isOpen);
  mobileMenuBackdrop.style.display = isOpen ? 'block' : 'none';
});
mobileMenuBackdrop.addEventListener('click', closeMobileMenu);
window.addEventListener('resize', function() {
  if(window.innerWidth > 600) {
    closeMobileMenu();
  }
});
// Закрытие меню свайпом вверх (для UX)
let touchStartY = null;
mobileMenu.addEventListener('touchstart', function(e) {
  if (e.touches.length === 1) touchStartY = e.touches[0].clientY;
});
mobileMenu.addEventListener('touchmove', function(e) {
  if (touchStartY !== null && e.touches.length === 1) {
    const deltaY = e.touches[0].clientY - touchStartY;
    if (deltaY < -60) {
      closeMobileMenu();
      touchStartY = null;
    }
  }
});