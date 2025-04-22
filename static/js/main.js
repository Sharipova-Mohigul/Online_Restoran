document.addEventListener('DOMContentLoaded', function() {
    // Buyurtma berish funksiyasi
    document.querySelectorAll('.order-btn').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.dataset.productId;
            const productName = this.dataset.productName;
            const productPrice = this.dataset.productPrice;
            
            // Modalni ochish yoki savatga qo'shish
            addToCart(productId, productName, productPrice);
        });
    });

    // Savat funksiyalari
    function addToCart(productId, productName, productPrice) {
        let cart = JSON.parse(localStorage.getItem('cart')) || [];
        
        // Mahsulot savatda bormi?
        const existingItem = cart.find(item => item.id === productId);
        
        if (existingItem) {
            existingItem.quantity += 1;
        } else {
            cart.push({
                id: productId,
            name: productName,
                price: productPrice,
                quantity: 1
            });
        }
        
        localStorage.setItem('cart', JSON.stringify(cart));
        updateCartCounter();
        showToast(`${productName} savatga qo'shildi`);
    }

    // Savatdagi mahsulotlar sonini yangilash
    function updateCartCounter() {
        const cart = JSON.parse(localStorage.getItem('cart')) || [];
        const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
        document.querySelectorAll('.cart-counter').forEach(el => {
            el.textContent = totalItems;
            el.style.display = totalItems > 0 ? 'inline-block' : 'none';
        });
    }

    // Xabarnoma ko'rsatish
    function showToast(message) {
        const toast = document.createElement('div');
        toast.className = 'toast-notification';
        toast.textContent = message;
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.classList.add('show');
            setTimeout(() => {
                toast.remove();
            }, 3000);
        }, 100);
    }

    // Dastlabki savat sonini yangilash
    updateCartCounter();
});