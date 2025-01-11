document.getElementById('LoginForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const login = document.getElementById('loginInput').value;
    const password = document.getElementById('passwordInput').value;
    const errorMessage = document.getElementById('modalMessage');

    function setError(message) {
        errorMessage.innerText = message;
        document.getElementById('modal').style.display = 'flex'; // Открываем модальное окно
    }

    // 1. Проверка явности ника
    if (login.trim() === "") {
        setError("Будь ласка, введіть нікнейм або email.");
        return;
    }

    // 2. Проверка явности пароля
    if (password.trim() === "") {
        setError("Будь ласка, введіть пароль.");
        return;
    }

    // 3. Верификация
    try {
        const response = await fetch('/check-login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ login, password })
        });
        const data = await response.json();

        if (data.exists === "no-login") {
            setError("Неправильний нікнейм або email");
            return;
        }
        if (data.exists === "wrong-password") {
            setError("Неправильний пароль");
            return;
        }
        if (data.exists === "is-login") {
            alert("Ви успішно авторизувалися");
            window.location.href = '/';
            return;
        }
    } catch (error) {
        console.error("Помилка під час перевірки нікнейма:", error);
        setError("Помилка під час перевірки нікнейма.");
        return;
    }
});

function closeModal() {
    document.getElementById('modal').style.display = 'none'; // Закрываем модальное окно
}
