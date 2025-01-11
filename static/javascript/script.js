document.getElementById('registerForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const nickname = document.getElementById('nicknameInput').value;
    const email = document.querySelector('input[name="email"]').value; // Получаем значение email
    const password = document.querySelector('input[name="password"]').value; // Получаем значение пароля
    const password_2 = document.querySelector('input[name="password_2"]').value; // Получаем значение подтверждения пароля

    function setError(message) {
        document.getElementById('modalMessage').innerText = message;
        document.getElementById('modal').style.display = 'flex';
    }

    // 1. Проверка явности ника
    if (nickname.trim() === "") {
        setError("Будь ласка, введіть нікнейм.");
        return;
    }

    // 2. Проверка длины ника
    if (nickname.length < 3 || nickname.length > 15) {
        setError("Нікнейм повинен містити від 3 до 15 символів.");
        return;
    }

    // 3. Асинхронная проверка ника в базе данных
    try {
        const response = await fetch('/check-nickname', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ nickname })
        });
        const data = await response.json();

        if (data.exists) {
            setError("Цей нікнейм вже зайнятий. Будь ласка, виберіть інший.");
            return;
        }
    } catch (error) {
        console.error("Помилка під час перевірки нікнейма:", error);
        setError("Помилка під час перевірки нікнейма.");
        return;
    }

    // 4. Проверка явности email
    if (email.trim() === "") {
        setError("Будь ласка, введіть ваш email.");
        return;
    }

    // 5. Проверка формата email
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        setError("Некоректний формат email.");
        return;
    }

    // 6. Асинхронная проверка email в базе данных
    try {
        const emailResponse = await fetch('/check-email', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email })
        });
        const emailData = await emailResponse.json();

        if (emailData.exists) {
            setError("Цей email вже зареєстровано.");
            return;
        }
    } catch (error) {
        console.error("Помилка під час перевірки email:", error);
        setError("Помилка під час перевірки email.");
        return;
    }
    // 7. Проверка явности пароля
    if (password.trim() === "") {
        setError("Будь ласка, придумайте і введіть пароль.");
        return;
    }

    // 8. Проверка длины пароля
    if (password.length < 8) {
        setError("Пароль повинен складатися мінімум з 8 символів.");
        return;
    }

    // 9. Проверка явности повторного пароля
    if (password_2.trim() === "") {
        setError("Будь ласка, введіть пароль повторно в 4 ряд.");
        return;
    }
    // 10. Проверка совпадения паролей
    if (password !== password_2) {
        setError("Ваш пароль і повторний пароль не збігаються.");
        return;
    }

    // 11. Если все проверки пройдены, регистрируем пользователя
    try {
        // Отправляем данные на сервер для регистрации
        const response = await fetch('/register-user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                nickname: nickname,
                email: email,
                password: password
            })
        });

        const data = await response.json();
        alert("Реєстрація пройшла успішно!");
        window.location.href = '/';

    } catch (error) {
        console.error("Помилка під час реєстрації:", error.message);
        alert(`Ошибка: ${error.message}`); // Выводим сообщение об ошибке
    }
});

function closeModal() {
    document.getElementById('modal').style.display = 'none'; // Закрываем модальное окно
}