document.getElementById("login-form").addEventListener("submit", async function(event) {
    event.preventDefault();

    const formData = new FormData();
    formData.append("email", document.getElementById("email").value);
    formData.append("password", document.getElementById("password").value);

    try {
        const response = await fetch("/v1/auth/login", {
            method: "POST",
            body: formData
        });

        const result = await response.json();

        if (response.ok) {
            alert(result.message || "Успешный вход!");
            window.location.href = "/pages/profile";  // предположим, у тебя есть профиль
        } else {
            alert(result.message || "Неверный email или пароль");
        }
    } catch (error) {
        console.error("Ошибка:", error);
        alert("Ошибка при авторизации");
    }
});
