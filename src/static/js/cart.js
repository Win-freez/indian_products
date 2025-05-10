const checkoutBtn = document.getElementById('checkout-btn');
const cartItemsContainer = document.getElementById('cart-items-container');
const totalPriceElement = document.getElementById('total-price');

// Функция для получения корзины
async function fetchCart() {
    const response = await fetch('/v1/cart');
    const data = await response.json();

    renderCartItems(data.cart_items);
    calculateTotalPrice(data.cart_items);
}

// Рендеринг товаров в корзине
function renderCartItems(cartItems) {
    cartItemsContainer.innerHTML = ''; // Очищаем контейнер
    cartItems.forEach(item => {
        const itemElement = document.createElement('div');
        itemElement.classList.add('cart-item');
        itemElement.innerHTML = `
            <div class="d-flex justify-content-between">
                <span>${item.product_name_snapshot} (x${item.quantity})</span>
                <span>${item.price_at_time * item.quantity} ₽</span>
            </div>
        `;
        cartItemsContainer.appendChild(itemElement);
    });
}

// Расчёт общей стоимости
function calculateTotalPrice(cartItems) {
    let total = 0;
    cartItems.forEach(item => {
        total += item.price_at_time * item.quantity;
    });
    totalPriceElement.textContent = total.toFixed(2);
}

// Оформление заказа
async function checkout() {
    const response = await fetch('/v1/cart/from-cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('token') // Используем токен из localStorage
        }
    });

    if (response.ok) {
        const order = await response.json();
        window.location.href = `/v1/orders/${order.id}`; // Перенаправляем на страницу заказа
    } else {
        alert('Ошибка оформления заказа');
    }
}

// Инициализация корзины и обработчик кнопки
checkoutBtn.addEventListener('click', checkout);

// Загружаем корзину при загрузке страницы
fetchCart();
