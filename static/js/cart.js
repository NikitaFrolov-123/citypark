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

    function postJson(url, payload) {
        return fetch(url, {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(payload)
        }).then(async response => {
            const data = await response.json();
            if (!response.ok) throw new Error(data.message || 'Request failed');
            return data;
        });
    }

    document.querySelectorAll('.add-to-cart-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const dishId = this.getAttribute('data-dish-id');
            const quantityInput = this.closest('.dish-actions, .dish-body, .dish-detail-info')?.querySelector('.qty-input');
            const quantity = quantityInput ? parseInt(quantityInput.value, 10) : 1;

            postJson('/cart/add/', {dish_id: dishId, quantity})
                .then(() => {
                    const text = this.querySelector('.btn-text');
                    if (text) {
                        text.textContent = 'Добавлено!';
                        setTimeout(() => text.textContent = 'В корзину', 1200);
                    }
                })
                .catch(error => {
                    console.error(error);
                    alert('Ошибка добавления в корзину');
                });
        });
    });

    document.querySelectorAll('.remove-from-cart-btn').forEach(button => {
        button.addEventListener('click', function() {
            const dishId = this.getAttribute('data-dish-id');
            postJson('/cart/remove/', {dish_id: dishId})
                .then(() => {
                    const item = this.closest('.cart-item');
                    if (item) item.remove();
                    location.reload();
                })
                .catch(error => {
                    console.error(error);
                    alert('Ошибка удаления из корзины');
                });
        });
    });

    document.querySelectorAll('.qty-btn').forEach(button => {
        button.addEventListener('click', function() {
            const wrapper = this.closest('.cart-quantity, .quantity-control');
            const input = wrapper?.querySelector('.qty-input');
            if (!input) return;

            let value = parseInt(input.value, 10);

            if (this.classList.contains('qty-minus')) value = Math.max(1, value - 1);
            if (this.classList.contains('qty-plus')) value = Math.min(10, value + 1);

            input.value = value;

            postJson('/cart/update/', {
                dish_id: this.getAttribute('data-dish-id'),
                quantity: value
            })
                .then(() => location.reload())
                .catch(error => {
                    console.error(error);
                    alert('Ошибка обновления количества');
                });
        });
    });

    document.querySelectorAll('.clear-cart-btn').forEach(button => {
        button.addEventListener('click', function() {
            postJson('/cart/clear/', {})
                .then(() => location.reload())
                .catch(error => {
                    console.error(error);
                    alert('Ошибка очистки корзины');
                });
        });
    });
});