// Обработка формы входа
document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Останавливаем стандартное поведение формы

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const formData = new URLSearchParams();
    formData.append('email', email);
    formData.append('password', password);

    // Отправляем запрос на сервер
    fetch('/v1/auth/login', {  // Убедитесь, что путь правильный
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded' // Отправляем как форму
        },
        body: formData.toString()  // Преобразуем в строку формата x-www-form-urlencoded
    })
    .then(response => response.json())
    .then(data => {
        if (data.access_token) {
            // Сохраняем токен в localStorage
            localStorage.setItem("access_token", data.access_token);

            // Перенаправляем на главную страницу
            window.location.href = "/pages";  // Главная страница
        } else {
            alert("Неверный email или пароль");
        }
    })
    .catch(error => {
        console.error("Ошибка:", error);
    });
});

// Обработка формы регистрации
document.getElementById('registerForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Останавливаем стандартное поведение формы

    const formData = {
        email: document.getElementById('reg_email').value,
        password: document.getElementById('password_reg').value,
        phone_number: document.getElementById('phone_number').value,
        first_name: document.getElementById('first_name').value,
        last_name: document.getElementById('last_name').value
    };

    // Отправляем данные в формате JSON
    fetch('/v1/auth/register', {  // Убедитесь, что путь правильный
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)  // Отправляем данные как JSON
    })
    .then(response => response.json())
    .then(data => {
        if (data.ok) {
            alert("Регистрация прошла успешно!");
            window.location.href = "/";  // Редирект на главную страницу
        } else {
            alert("Ошибка регистрации: " + data.message || "Неизвестная ошибка");
        }
    })
    .catch(error => {
        console.error("Ошибка:", error);
        alert("Ошибка при отправке запроса. Пожалуйста, попробуйте снова.");
    });
});
