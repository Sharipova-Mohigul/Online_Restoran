// Slideshow uchun JavaScript
let currentSlide = 0;
const slides = document.querySelectorAll('.slide');

function showSlide(n) {
    slides.forEach(slide => slide.classList.remove('active'));
    currentSlide = (n + slides.length) % slides.length;
    slides[currentSlide].classList.add('active');
}

function nextSlide() {
    showSlide(currentSlide + 1);
}

// Har 5 sekundda slaydni o'zgartirish
setInterval(nextSlide, 5000);

// Navigation scroll uchun
window.addEventListener('scroll', function() {
    const nav = document.querySelector('nav');
    if (window.scrollY > 50) {
        nav.style.background = 'rgba(0, 0, 0, 0.9)';
        nav.style.padding = '15px 50px';
    } else {
        nav.style.background = 'transparent';
        nav.style.padding = '20px 50px';
    }
});

// Menyu tablari uchun
const tabBtns = document.querySelectorAll('.tab-btn');
const menuItems = document.querySelectorAll('.menu-item');

tabBtns.forEach(btn => {
    btn.addEventListener('click', function() {
        // Faol tabni o'zgartirish
        tabBtns.forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        
        // Menyu elementlarini filtrlash
        const category = this.dataset.category;
        
        menuItems.forEach(item => {
            if (category === 'all' || item.dataset.category === category) {
                item.style.display = 'flex';
            } else {
                item.style.display = 'none';
            }
        });
    });
});

// Savatga qo'shish funksiyasi
document.querySelectorAll('.add-to-cart').forEach(btn => {
    btn.addEventListener('click', function() {
        const itemId = this.dataset.id;
        // Bu yerda AJAX so'rovi yuborish mumkin
        alert('Mahsulot savatga qo\'shildi! ID: ' + itemId);
    });
});

// Mobil menyu uchun
const menuToggle = document.querySelector('.menu-toggle');
const navLinks = document.querySelector('.nav-links');

menuToggle.addEventListener('click', () => {
    navLinks.classList.toggle('active');
    menuToggle.querySelector('i').classList.toggle('fa-times');
    menuToggle.querySelector('i').classList.toggle('fa-bars');
});

// Navigation linklari uchun smooth scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;
        
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
            window.scrollTo({
                top: targetElement.offsetTop - 80,
                behavior: 'smooth'
            });
            
            // Mobil menyuni yopish
            if (navLinks.classList.contains('active')) {
                navLinks.classList.remove('active');
                menuToggle.querySelector('i').classList.remove('fa-times');
                menuToggle.querySelector('i').classList.add('fa-bars');
            }
        }
    });
});