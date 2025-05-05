async function getOrders() {
    try {
        const response = await fetch('/orders/');
        if (!response.ok) {
            throw new Error('Не удалось получить заказы');
        }
        const orders = await response.json();
        displayOrders(orders);  // Функция для отображения заказов на странице
    } catch (error) {
        console.error(error);
    }
}

function displayOrders(orders) {
    const ordersContainer = document.getElementById('orders-container');
    ordersContainer.innerHTML = '';
    orders.forEach(order => {
        const orderElement = document.createElement('div');
        orderElement.classList.add('order');
        orderElement.innerHTML = `
            <p>Заказ №${order.id}</p>
            <p>Дата: ${order.date}</p>
            <p>Статус: ${order.status}</p>
            <button onclick="cancelOrder(${order.id})">Отменить</button>
        `;
        ordersContainer.appendChild(orderElement);
    });
}
async function getOrderById(orderId) {
    try {
        const response = await fetch(`/orders/${orderId}`);
        if (!response.ok) {
            throw new Error('Не удалось получить заказ');
        }
        const order = await response.json();
        displayOrder(order);  // Функция для отображения информации о заказе
    } catch (error) {
        console.error(error);
    }
}

function displayOrder(order) {
    const orderDetailsContainer = document.getElementById('order-details');
    orderDetailsContainer.innerHTML = `
        <p>Заказ №${order.id}</p>
        <p>Дата: ${order.date}</p>
        <p>Статус: ${order.status}</p>
        <p>Сумма: ${order.total_price} ₹</p>
        <button onclick="cancelOrder(${order.id})">Отменить заказ</button>
    `;
}
async function createOrder(orderData) {
    try {
        const response = await fetch('/orders/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(orderData),
        });
        if (!response.ok) {
            throw new Error('Не удалось создать заказ');
        }
        const order = await response.json();
        alert('Заказ создан!');  // Можно перенаправить на страницу заказа или обновить список
    } catch (error) {
        console.error(error);
    }
}
async function cancelOrder(orderId) {
    try {
        const response = await fetch(`/orders/${orderId}/cancel`, {
            method: 'POST',
        });
        if (!response.ok) {
            throw new Error('Не удалось отменить заказ');
        }
        const order = await response.json();
        alert('Заказ отменён!');
        // Обновить UI или список заказов
    } catch (error) {
        console.error(error);
    }
}
async function deleteOrder(orderId) {
    try {
        const response = await fetch(`/orders/${orderId}`, {
            method: 'DELETE',
        });
        if (!response.ok) {
            throw new Error('Не удалось удалить заказ');
        }
        alert('Заказ удалён');
        // Обновить UI или список заказов
    } catch (error) {
        console.error(error);
    }
}
