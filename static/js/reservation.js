document.addEventListener('DOMContentLoaded', function() {
    // Stol tanlash logikasi
    const tables = document.querySelectorAll('.table');
    const tableIdInput = document.getElementById('table_id');
    const submitBtn = document.getElementById('submit-btn');
    const selectedTableDisplay = document.getElementById('selected-table-display');
    const selectedTimeDisplay = document.getElementById('selected-time-display');
    const modal = document.getElementById('table-modal');
    const closeModal = document.querySelector('.close-modal');
    const confirmTableBtn = document.getElementById('confirm-table');
    
    let selectedTable = null;
    
    // Stol tanlash modalini ochish
    tables.forEach(table => {
        table.addEventListener('click', function() {
            if (this.classList.contains('reserved')) {
                alert('Bu stol band qilingan. Iltimos, boshqa stol tanlang.');
                return;
            }
            
            // Modalga ma'lumotlarni to'ldirish
            document.getElementById('modal-table-number').textContent = this.dataset.id;
            document.getElementById('modal-table-seats').textContent = this.dataset.seats + " o'rin";
            document.getElementById('modal-table-status').textContent = 
                this.classList.contains('reserved') ? 'Band' : 'Bo\'sh';
            
            // Stol shaklini moslashtirish
            const tableShape = this.querySelector('.table-shape').className.split(' ')[1];
            const modalShape = document.getElementById('modal-table-shape');
            modalShape.className = 'table-shape ' + tableShape;
            
            // Modalni ochish
            modal.style.display = 'block';
            selectedTable = this;
        });
    });
    
    // Stolni tasdiqlash
    confirmTableBtn.addEventListener('click', function() {
        if (selectedTable) {
            // Avval tanlangan stolni olib tashlash
            tables.forEach(t => t.classList.remove('selected'));
            
            // Yangi stolni tanlash
            selectedTable.classList.add('selected');
            tableIdInput.value = selectedTable.dataset.id;
            
            // Tanlangan stol ma'lumotlarini ko'rsatish
            selectedTableDisplay.textContent = `Stol #${selectedTable.dataset.id} (${selectedTable.dataset.seats} o'rin)`;
            
            // Submit tugmasini faollashtirish
            submitBtn.disabled = false;
            
            // Modalni yopish
            modal.style.display = 'none';
        }
    });
    
    // Vaqt tanlanganda ko'rsatish
    document.getElementById('time').addEventListener('change', function() {
        selectedTimeDisplay.textContent = this.value;
    });
    
    // Modalni yopish
    closeModal.addEventListener('click', function() {
        modal.style.display = 'none';
    });
    
    // Modal tashqarisiga bosilsa yopish
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
    
    // Stol shakllari uchun dinamik stil
    const tableShapes = document.querySelectorAll('.table-shape');
    tableShapes.forEach(shape => {
        const table = shape.closest('.table');
        const seats = parseInt(table.dataset.seats);
        
        if (seats <= 2) {
            shape.classList.add('small');
        } else if (seats <= 4) {
            shape.classList.add('medium');
        } else {
            shape.classList.add('large');
        }
    });
});