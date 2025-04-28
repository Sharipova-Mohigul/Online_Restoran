// Telegram bildirishnomalari
function showTelegramNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'telegram-notification';
    notification.innerHTML = `
        <i class="fab fa-telegram"></i>
        <span>${message}</span>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideIn 0.5s reverse forwards';
        setTimeout(() => notification.remove(), 500);
    }, 5000);
}

// Telegram botga ulanish
function connectTelegramBot() {
    // WebSocket orqali real vaqtda aloqa
    const socket = new WebSocket(`wss://your-websocket-server.com/telegram`);
    
    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === 'notification') {
            showTelegramNotification(data.message);
        }
    };
    
    socket.onclose = () => {
        setTimeout(connectTelegramBot, 5000); // 5 sekunddan qayta ulanish
    };
}

// Agar foydalanuvchi Telegramda bo'lsa
if (window.Telegram && window.Telegram.WebApp) {
    const tgWebApp = window.Telegram.WebApp;
    
    // Foydalanuvchi ma'lumotlarini olish
    const user = tgWebApp.initDataUnsafe.user;
    if (user) {
        // Foydalanuvchi Telegram profili bilan avtorizatsiya
        fetch('/api/telegram_auth', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                id: user.id,
                first_name: user.first_name,
                last_name: user.last_name,
                username: user.username
            })
        });
    }
    
    // Telegram tugmalarini sozlash
    tgWebApp.MainButton.setText("Stol band qilish");
    tgWebApp.MainButton.show();
    tgWebApp.MainButton.onClick(() => {
        window.location.href = '/reservation';
    });
} else {
    // Oddiy brauzerda ishlayotgan foydalanuvchilar uchun
    connectTelegramBot();
}