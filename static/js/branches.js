let map;
let branches = [
    {
        id: 1,
        name: "MOSEMAOR Yunusobod",
        address: "Yunusobod tumani, Navoiy ko'chasi 45",
        lat: 41.3385,
        lng: 69.3343,
        phone: "+998901234567",
        hours: "09:00 - 23:00"
    },
    {
        id: 2,
        name: "MOSEMAOR Chilonzor",
        address: "Chilonzor tumani, Bunyodkor shoh ko'chasi 12",
        lat: 41.2987,
        lng: 69.2401,
        phone: "+998901234568",
        hours: "10:00 - 22:00"
    },
    {
        id: 3,
        name: "MOSEMAOR Mirzo Ulug'bek",
        address: "Mirzo Ulug'bek tumani, Amir Temur shoh ko'chasi 78",
        lat: 41.3153,
        lng: 69.2817,
        phone: "+998901234569",
        hours: "08:00 - 24:00"
    }
];

function initMap() {
    // Xaritani ishga tushirish
    map = new google.maps.Map(document.getElementById('branches-map'), {
        center: {lat: 41.311081, lng: 69.240562}, // Toshkent markazi
        zoom: 12
    });
    
    // Filliallarni xaritada ko'rsatish
    displayBranches(branches);
    
    // Avtomatik joylashuv aniqlash
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const userLocation = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                };
                
                // Foydalanuvchi joylashuvini belgilash
                new google.maps.Marker({
                    position: userLocation,
                    map: map,
                    title: "Siz bu yerdasiz",
                    icon: {
                        url: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png"
                    }
                });
                
                // Eng yaqin 3 ta fillialni topish
                findNearestBranches(userLocation);
            },
            () => {
                console.log("Geolocation permission denied");
            }
        );
    }
    
    // Joylashuv qidirish funksiyasi
    const input = document.getElementById('location-input');
    const searchBox = new google.maps.places.SearchBox(input);
    
    map.addListener('bounds_changed', () => {
        searchBox.setBounds(map.getBounds());
    });
    
    document.getElementById('find-branches').addEventListener('click', () => {
        const geocoder = new google.maps.Geocoder();
        geocoder.geocode({ address: input.value }, (results, status) => {
            if (status === 'OK' && results[0]) {
                const location = {
                    lat: results[0].geometry.location.lat(),
                    lng: results[0].geometry.location.lng()
                };
                
                map.setCenter(location);
                map.setZoom(14);
                
                // Eng yaqin filliallarni topish
                findNearestBranches(location);
            }
        });
    });
}

function displayBranches(branchesToShow) {
    const branchList = document.getElementById('branch-list');
    branchList.innerHTML = '';
    
    branchesToShow.forEach(branch => {
        // Xaritada marker qo'shish
        const marker = new google.maps.Marker({
            position: { lat: branch.lat, lng: branch.lng },
            map: map,
            title: branch.name
        });
        
        // Marker uchun info oyna
        const infowindow = new google.maps.InfoWindow({
            content: `
                <div class="branch-info-window">
                    <h4>${branch.name}</h4>
                    <p>${branch.address}</p>
                    <p>${branch.phone}</p>
                    <p>Ish vaqti: ${branch.hours}</p>
                    <button onclick="reserveAtBranch(${branch.id})" class="btn-small">Stol band qilish</button>
                </div>
            `
        });
        
        marker.addListener('click', () => {
            infowindow.open(map, marker);
        });
        
        // Filliallar ro'yxatiga qo'shish
        const branchElement = document.createElement('div');
        branchElement.className = 'branch-item';
        branchElement.innerHTML = `
            <h4>${branch.name}</h4>
            <p><i class="fas fa-map-marker-alt"></i> ${branch.address}</p>
            <p><i class="fas fa-phone"></i> ${branch.phone}</p>
            <p><i class="fas fa-clock"></i> ${branch.hours}</p>
            <button onclick="reserveAtBranch(${branch.id})" class="btn-small">Stol band qilish</button>
        `;
        
        branchList.appendChild(branchElement);
    });
}

function findNearestBranches(userLocation) {
    // Masofani hisoblash
    branches.forEach(branch => {
        branch.distance = calculateDistance(
            userLocation.lat, userLocation.lng,
            branch.lat, branch.lng
        );
    });
    
    // Eng yaqin 3 ta fillialni saralash
    const nearestBranches = [...branches]
        .sort((a, b) => a.distance - b.distance)
        .slice(0, 3);
    
    displayBranches(nearestBranches);
    
    // Xaritani eng yaqin fillial atrofida markazlash
    const bounds = new google.maps.LatLngBounds();
    nearestBranches.forEach(branch => {
        bounds.extend(new google.maps.LatLng(branch.lat, branch.lng));
    });
    bounds.extend(new google.maps.LatLng(userLocation.lat, userLocation.lng));
    map.fitBounds(bounds);
}

function calculateDistance(lat1, lon1, lat2, lon2) {
    const R = 6371; // Earth radius in km
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = 
        Math.sin(dLat/2) * Math.sin(dLat/2) +
        Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * 
        Math.sin(dLon/2) * Math.sin(dLon/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    return R * c; // Distance in km
}

function reserveAtBranch(branchId) {
    // Tanlangan fillialni saqlash
    sessionStorage.setItem('selectedBranch', branchId);
    // Stol band qilish sahifasiga yo'naltirish
    window.location.href = '/reservation';
}