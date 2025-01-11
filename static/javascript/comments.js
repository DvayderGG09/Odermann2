document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("descriptionInput").addEventListener("input", function() {
        const textarea = this;
        const maxRows = 5;
        const lines = textarea.value.split(/\r\n|\r|\n/);

        if (lines.length > maxRows) {
            // Ограничиваем количество строк
            textarea.value = lines.slice(0, maxRows).join("\n");

            // Перемещаем курсор в конец текста
            textarea.selectionStart = textarea.selectionEnd = textarea.value.length;
        }
    });

    const BtnAddReview = document.querySelector('.btn-add-review');
    const MenuAddReview = document.querySelector('.menu-add-review');
    const FonMenuAddReview = document.querySelector('.fon-menu-add-review');
    const CloseMenuAddReview = document.querySelector('.close-menu-add-review');
    const Description = document.getElementById('descriptionInput');
    const Stars = document.querySelectorAll('.star');
    const StarsSelectedField = document.querySelector('input[name="starsSelected"]');
    document.getElementById('avatar-path').value = document.querySelector('.menu-add-review-avatar').getAttribute('src');
    let StarsSelected = 0;

    BtnAddReview.onclick = function() {
        MenuAddReview.style.display = 'flex';
        FonMenuAddReview.style.display = 'block';
        document.getElementById('descriptionInput').innerText = '';
    }

    CloseMenuAddReview.onclick = function() {
        MenuAddReview.style.display = 'none';
        FonMenuAddReview.style.display = 'none';
        Description.value = '';
        Stars.forEach(star => {
            star.src = '/static/images/star.png'
        });
    }

    FonMenuAddReview.onclick = function() {
        MenuAddReview.style.display = 'none';
        FonMenuAddReview.style.display = 'none';
        Description.value = '';
        Stars.forEach(star => {
            star.src = '/static/images/star.png'
        });
    }

    Stars.forEach((star, index) => {
        star.addEventListener('click', () => {
            Stars.forEach((s, i) => {
                if (i <= index) {
                    s.src = '/static/images/star-full.png';
                    StarsSelected = index + 1;
                } else {
                    s.src = '/static/images/star.png';
                }
            });
            StarsSelectedField.value = StarsSelected;
        });
    });

//    document.getElementById('AddReviewForm').addEventListener('submit', async function(event) {
//        event.preventDefault();
//
//        if (StarsSelected <= 0) {
//            alert('Пожалуйста, выберите количество звезд для отзыва.');
//            return;
//        }
//
//        const DescriptionText = document.getElementById('descriptionInput').value;
//        const selfNickname = document.querySelector('.menu-add-review-nickname').textContent;
//        const selfAvatar = document.querySelector('.menu-add-review-avatar');
//        const selfAvatarSrc = selfAvatar.src;
//        const selfAvatarName = selfAvatarSrc.split('/').pop();
//
//        try {
//            const formData = new FormData();
//            formData.append('description', DescriptionText);
//            formData.append('starsSelected', StarsSelected);
//
//            const response = await fetch('/comments', {
//                method: 'POST',
//                body: formData,
//            });
//
//            if (response.ok) {
//                const data = await response.json();
//                if (data.answer) {
//                    alert('Отзыв успешно оставлен.');
//                    location.reload();
//                }
//            } else {
//                const errorData = await response.json();
//                alert(errorData.error);
//            }
//        } catch (error) {
//            console.error('Ошибка при отправке запроса:', error);
//        }
//    });







//    document.getElementById('AddReviewForm').addEventListener('submit', async function(event) {
//        event.preventDefault();
//        if (StarsSelected <= 0) {
//            alert('Пожалуйста, выберите количество звезд для отзыва.');
//            return;
//        }
//        const DescriptionText = document.getElementById('descriptionInput').value;
//        const selfNickname = document.querySelector('.menu-add-review-nickname').textContent;
//        const selfAvatar = document.querySelector('.menu-add-review-avatar');
//        const selfAvatarSrc = selfAvatar.src;
//        const selfAvatarName = selfAvatarSrc.split('/').pop();
//        try {
//            const formData = new FormData();
//            formData.append('nickname', selfNickname);
//            formData.append('avatar', selfAvatarName);
//            formData.append('description', DescriptionText);
//            formData.append('grade', StarsSelected);
//
//            const response = await fetch('/AddReview', {
//                method: 'POST',
//                body: formData,
//            });
//            if (response.ok) {
//                const data = await response.json();
//
//                if (data.answer) {
//                    alert('Отзыв успешно оставлен.');
//                    location.reload();
//                } else {
//                    console.error('Ошибка на сервере.');
//                }
//            } else {
//                console.error('Ошибка при получении ответа от сервера:', response.statusText);
//            }
//        } catch (error) {
//            console.error('Ошибка при отправке запроса:', error);
//        }
//    });
});