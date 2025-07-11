document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
        // Закрытие мобильного меню при переходе
        if(window.innerWidth <= 600) {
            document.getElementById('mobileMenu').classList.remove('open');
            document.getElementById('burgerBtn').setAttribute('aria-expanded', 'false');
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
burgerBtn.addEventListener('click', function() {
    mobileMenu.classList.toggle('open');
    const expanded = burgerBtn.getAttribute('aria-expanded') === 'true';
    burgerBtn.setAttribute('aria-expanded', !expanded);
    mobileMenu.setAttribute('aria-hidden', expanded);
});
window.addEventListener('resize', function() {
    if(window.innerWidth > 600) {
        mobileMenu.classList.remove('open');
        burgerBtn.setAttribute('aria-expanded', 'false');
        mobileMenu.setAttribute('aria-hidden', 'true');
    }
});