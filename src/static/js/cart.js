// Загрузка корзины
document.addEventListener("DOMContentLoaded", fetchCart);

const checkoutBtn = document.getElementById('checkout-btn');
const clearCartBtn = document.getElementById('clear-cart-btn');  // Кнопка для очистки корзины
const cartItemsContainer = document.getElementById('cart-items-container');
const totalPriceElement = document.getElementById('total-price');

// Получение корзины
async function fetchCart() {
    const response = await fetch('/v1/cart', {
        headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('token')
        }
    });

    if (response.ok) {
        const data = await response.json();
        renderCartItems(data.cart_items);
        calculateTotalPrice(data.cart_items);
    } else {
        alert('Ошибка при загрузке корзины');
    }
}

// Отображение товаров
function renderCartItems(cartItems) {
    cartItemsContainer.innerHTML = '';
    cartItems.forEach((item, index) => {
        const price = parseFloat(item.price_at_time);
        const sum = price * item.quantity;

        const itemElement = document.createElement('tr');
        itemElement.innerHTML = `
            <th scope="row">${index + 1}</th>
            <td>${item.product_name_snapshot}</td>
            <td>${price.toFixed(2)} ₽</td>
            <td>
                <input type="number" min="1" value="${item.quantity}" class="form-control" style="width: 80px;"
                    onchange="changeItemInCart('${item.product_slug}', this.value)">
            </td>
            <td>${sum.toFixed(2)} ₽</td>
            <td>
                <button class="btn btn-danger btn-sm" onclick="removeItemFromCart('${item.product_slug}')">Удалить</button>
            </td>
        `;
        cartItemsContainer.appendChild(itemElement);
    });
}

// Расчёт общей суммы
function calculateTotalPrice(cartItems) {
    let total = 0;
    cartItems.forEach(item => {
        total += parseFloat(item.price_at_time) * item.quantity;
    });
    totalPriceElement.textContent = total.toFixed(2);
}

// Добавить товар
async function addItemToCart(slug, quantity = 1) {
    const response = await fetch('/v1/cart/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('token')
        },
        body: JSON.stringify({ product_slug: slug, quantity })
    });

    if (response.ok) {
        await fetchCart();
    } else {
        alert('Ошибка при добавлении товара в корзину');
    }
}

// Изменить количество
async function changeItemInCart(slug, quantity) {
    const response = await fetch('/v1/cart/', {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('token')
        },
        body: JSON.stringify({ product_slug: slug, quantity: parseInt(quantity) })
    });

    if (response.ok) {
        await fetchCart();
    } else {
        alert('Ошибка при изменении количества товара');
    }
}

// Удалить товар
async function removeItemFromCart(slug) {
    const response = await fetch(`/v1/cart/${slug}`, {
        method: 'DELETE',
        headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('token')
        }
    });

    if (response.ok) {
        await fetchCart();
    } else {
        alert('Ошибка при удалении товара');
    }
}

// Очистить корзину
async function clearCart() {
    const response = await fetch('/v1/cart/', {
        method: 'DELETE',
        headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('token')
        }
    });

    if (response.ok) {
        await fetchCart();
    } else {
        alert('Ошибка при очистке корзины');
    }
}

// Оформить заказ
async function checkout() {
    const response = await fetch('/v1/orders/from-cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('token')
        }
    });

    if (response.ok) {
        const order = await response.json();
        // Отображаем сообщение о том, что заказ успешно оформлен
        alert(`Заказ успешно оформлен! Ваш заказ №${order.id} на сумму ${order.total_price} ₽`);

        // Выводим список товаров в заказе
        let orderDetails = '<h3>Список товаров в заказе:</h3><ul>';
        order.order_items.forEach(item => {
            orderDetails += `<li>${item.product_name_snapshot} (x${item.quantity}) - ${item.price_at_time} ₽</li>`;
        });
        orderDetails += '</ul>';

        // Отображаем информацию о заказе на странице
        const orderContainer = document.createElement('div');
        orderContainer.classList.add('order-details');
        orderContainer.innerHTML = `
            <h2>Заказ №${order.id}</h2>
            <p>Статус: ${order.status}</p>
            <p>Общая сумма: ${order.total_price} ₽</p>
            ${orderDetails}
        `;
        document.body.appendChild(orderContainer);

        // Перенаправление на страницу заказа
        window.location.href = `/pages/orders/${order.id}`;
    } else {
        alert('Ошибка оформления заказа');
    }
}


checkoutBtn.addEventListener('click', checkout);
clearCartBtn.addEventListener('click', clearCart);  // Добавляем обработчик для очистки корзины
