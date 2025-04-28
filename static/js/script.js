document.addEventListener('DOMContentLoaded', function() {
    // Mobil menyu
    const burger = document.querySelector('.burger');
    const nav = document.querySelector('.nav-links');
    
    if (burger && nav) {
        burger.addEventListener('click', () => {
            nav.classList.toggle('nav-active');
            burger.classList.toggle('toggle');
        });
    }
    
    // Galereya slayderi
    const slides = document.querySelectorAll('.slide');
    let currentSlide = 0;
    
    function showSlide(n) {
        slides.forEach(slide => slide.style.display = 'none');
        currentSlide = (n + slides.length) % slides.length;
        slides[currentSlide].style.display = 'block';
    }
    
    if (slides.length > 0) {
        showSlide(0);
        setInterval(() => showSlide(currentSlide + 1), 3000);
    }
    
    // Stol band qilish sanasi
    const dateInput = document.getElementById('date');
    if (dateInput) {
        const today = new Date().toISOString().split('T')[0];
        dateInput.setAttribute('min', today);
    }
    
    // 3D menyu kartalari
    const menuCards = document.querySelectorAll('.menu-card');
    menuCards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const xAxis = (window.innerWidth / 2 - e.pageX) / 25;
            const yAxis = (window.innerHeight / 2 - e.pageY) / 25;
            card.style.transform = `rotateY(${xAxis}deg) rotateX(${yAxis}deg)`;
        });
        
        card.addEventListener('mouseenter', () => {
            card.style.transition = 'none';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transition = 'transform 0.5s ease';
            card.style.transform = 'rotateY(0deg) rotateX(0deg)';
        });
    });
});