document.addEventListener('DOMContentLoaded', function() {
    const input = document.querySelector('.profile-container-avatar-change');
    const overlay = document.querySelector('.profile-container-avatar-overlay');
    const avatar = document.querySelector('.profile-container-avatar');
    const emailContainer = document.querySelector('.profile-container-email')
    const email = emailContainer.textContent;

    overlay.onclick = function() {
        input.click();
    }

    input.addEventListener('change', function() {
        const file = input.files[0];
        if (file) {
            const reader = new FileReader();

            reader.onload = async function(e) {
                try {
                    const formData = new FormData();
                    formData.append('avatar', file);
                    formData.append('email', email);

                    const response = await fetch('/updateAvatar', {
                        method: 'POST',
                        body: formData,
                    });
                    if (response.ok) {
                        const data = await response.json();

                        if (data.answer) {
                            avatar.src = e.target.result;
                        } else {
                            console.error('Ошибка загрузки на сервере.');
                        }
                    } else {
                        console.error('Ошибка при получении ответа от сервера:', response.statusText);
                    }
                } catch (error) {
                    console.error('Ошибка при отправке запроса:', error);
                }
            };
            reader.readAsDataURL(file);
        }
    });
});