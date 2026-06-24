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

document.addEventListener('DOMContentLoaded', function() {
    const csrfToken = getCookie('csrftoken');

    document.querySelectorAll('.add-to-cart-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();

            const dishId = this.getAttribute('data-dish-id');
            const quantityInput = this.closest('.dish-actions, .dish-detail-info, .dish-body')?.querySelector('.qty-input');
            const quantity = quantityInput ? parseInt(quantityInput.value, 10) : 1;

            fetch('/cart/add/', {
                method: 'POST',
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    dish_id: dishId,
                    quantity: quantity
                })
            })
            .then(async response => {
                const data = await response.json();
                if (!response.ok) throw new Error(data.message || 'Request failed');
                return data;
            })
            .then(() => {
                const text = this.querySelector('.btn-text');
                if (text) text.textContent = 'Добавлено!';
                setTimeout(() => {
                    if (text) text.textContent = 'В корзину';
                }, 1500);
            })
            .catch(error => {
                console.error(error);
                alert('Ошибка добавления в корзину');
            });
        });
    });

    document.querySelectorAll('.remove-btn').forEach(button => {
        button.addEventListener('click', function() {
            const dishId = this.getAttribute('data-dish-id');

            fetch('/cart/remove/', {
                method: 'POST',
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    dish_id: dishId
                })
            })
            .then(async response => {
                const data = await response.json();
                if (!response.ok) throw new Error(data.message || 'Request failed');
                return data;
            })
            .then(() => {
                const item = this.closest('.cart-item');
                if (item) item.remove();
                setTimeout(() => location.reload(), 300);
            })
            .catch(error => {
                console.error(error);
                alert('Ошибка удаления из корзины');
            });
        });
    });

    document.querySelectorAll('.qty-btn').forEach(button => {
        button.addEventListener('click', function() {
            const input = this.closest('.quantity-control')?.querySelector('.qty-input');
            if (!input) return;

            let value = parseInt(input.value, 10);

            if (this.classList.contains('qty-minus')) {
                value = Math.max(1, value - 1);
            } else {
                value = Math.min(10, value + 1);
            }

            input.value = value;

            fetch('/cart/update/', {
                method: 'POST',
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    dish_id: this.getAttribute('data-dish-id'),
                    quantity: value
                })
            })
            .then(async response => {
                const data = await response.json();
                if (!response.ok) throw new Error(data.message || 'Request failed');
                return data;
            })
            .then(() => location.reload())
            .catch(error => {
                console.error(error);
                alert('Ошибка обновления количества');
            });
        });
    });
});