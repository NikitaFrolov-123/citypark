document.addEventListener('DOMContentLoaded', function() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const dishCards = Array.from(document.querySelectorAll('.dish-card'));
    const searchInput = document.getElementById('searchDishes');
    const sortSelect = document.getElementById('sortDishes');
    const grid = document.getElementById('dishesGrid');

    function getActiveCategory() {
        const activeButton = document.querySelector('.filter-btn.active');
        return activeButton ? activeButton.dataset.category : 'all';
    }

    function applyFilters() {
        const activeCategory = getActiveCategory();
        const searchValue = (searchInput?.value || '').trim().toLowerCase();

        dishCards.forEach(card => {
            const dishName = (card.dataset.dishName || '').toLowerCase();
            const dishCategory = card.dataset.category || 'none';

            const matchesCategory = activeCategory === 'all' || dishCategory === activeCategory;
            const matchesSearch = !searchValue || dishName.includes(searchValue);

            card.style.display = (matchesCategory && matchesSearch) ? '' : 'none';
        });
    }

    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            applyFilters();
        });
    });

    if (searchInput) {
        searchInput.addEventListener('input', applyFilters);
    }

    if (sortSelect && grid) {
        sortSelect.addEventListener('change', function() {
            const sortOrder = this.value;

            const cardsToSort = [...dishCards];
            cardsToSort.sort((a, b) => {
                const priceA = parseInt(a.querySelector('.dish-bottom span')?.textContent.replace(/[^\d]/g, '') || '0', 10);
                const priceB = parseInt(b.querySelector('.dish-bottom span')?.textContent.replace(/[^\d]/g, '') || '0', 10);
                const nameA = (a.querySelector('h3')?.textContent || '').trim().toLowerCase();
                const nameB = (b.querySelector('h3')?.textContent || '').trim().toLowerCase();

                if (sortOrder === 'price-asc') return priceA - priceB;
                if (sortOrder === 'price-desc') return priceB - priceA;
                if (sortOrder === 'name') return nameA.localeCompare(nameB);
                return 0;
            });

            cardsToSort.forEach(card => grid.appendChild(card));
            applyFilters();
        });
    }

    document.addEventListener('click', function(e) {
        const addBtn = e.target.closest('.add-to-cart-btn');
        if (!addBtn) return;

        e.preventDefault();

        const dishId = addBtn.getAttribute('data-dish-id');

        fetch('/cart/add/', {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                dish_id: dishId,
                quantity: 1
            })
        })
        .then(async response => {
            const data = await response.json().catch(() => ({}));
            if (!response.ok) throw new Error(data.message || `HTTP ${response.status}`);
            return data;
        })
        .then(() => {
            const text = addBtn.querySelector('.btn-text');
            if (text) {
                text.textContent = 'Добавлено!';
                setTimeout(() => {
                    text.textContent = 'В корзину';
                }, 1200);
            }
        })
        .catch(error => {
            console.error(error);
            alert('Ошибка добавления в корзину');
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    applyFilters();
});