document.addEventListener('DOMContentLoaded', function() {
    // Bugungi sanani o'rnatish
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('date').min = today;
    document.getElementById('date').value = today;
    
    // Agar bugun tanlangan bo'lsa, faqat kelajakdagi vaqtlarni ko'rsatish
    document.getElementById('date').addEventListener('change', function() {
        const timeInput = document.getElementById('time');
        if (this.value === today) {
            const now = new Date();
            const currentHour = now.getHours();
            timeInput.min = `${currentHour + 1}:00`;
        } else {
            timeInput.removeAttribute('min');
        }
    });
    
    // Stol tanlash logikasi
    const tables = document.querySelectorAll('.table:not(.reserved)');
    const tableIdInput = document.getElementById('tableId');
    const guestsInput = document.getElementById('guests');
    const submitBtn = document.getElementById('submitBtn');
    
    tables.forEach(table => {
        table.addEventListener('click', function() {
            // Avval barcha tanlovlarni olib tashlash
            tables.forEach(t => t.classList.remove('selected'));
            
            // Yangisini tanlash
            this.classList.add('selected');
            tableIdInput.value = this.dataset.tableId;
            
            // Mehmonlar sonini stol sig'imiga moslashtirish
            guestsInput.max = this.dataset.capacity;
            guestsInput.value = Math.min(parseInt(guestsInput.value) || 1, parseInt(this.dataset.capacity));
            
            // Band qilish tugmasini yoqish
            submitBtn.disabled = false;
        });
    });
    
    // Mehmonlar sonini tekshirish
    guestsInput.addEventListener('change', function() {
        if (this.value > this.max) {
            this.value = this.max;
        }
    });
    
    // Formani yuborish
    document.getElementById('bookingForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        if (!tableIdInput.value) {
            alert('Iltimos, stolni tanlang!');
            return;
        }
        
        // AJAX orqali yuborish
        const formData = new FormData(this);
        
        fetch(this.action, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Stol muvaffaqiyatli band qilindi!');
                window.location.href = '/';
            } else {
                alert('Xatolik: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Xatolik:', error);
            alert('Server xatosi yuz berdi');
        });
    });
});