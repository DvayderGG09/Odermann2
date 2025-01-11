document.addEventListener("DOMContentLoaded", function() {
    const sortMaxButton = document.querySelector('.sort-max');
    const sortMinButton = document.querySelector('.sort-min');

    function sortPizzas() {
        const sortingPizza = localStorage.getItem('sorting-pizza');
        const pizzaPosts = document.querySelectorAll(".pizza-post"); // Получаем NodeList, а точнее коллекцию элементов которые имеют класс
        const pizzaArray = Array.from(pizzaPosts); // Из NodeList преобразуем в массив

        if (sortingPizza === 'max') {
            // Сортировка пицц по цене (от наивысшей к низшей)
            pizzaArray.sort((a, b) => {
                const priceA = parseInt(a.querySelector('.pizza-price').textContent.replace('₽', '').trim());
                const priceB = parseInt(b.querySelector('.pizza-price').textContent.replace('₽', '').trim());
                return priceB - priceA; // сортировка по убыванию цены
            });
        } else {
            // Сортировка пицц по цене (от низшей к наивысшей)
            pizzaArray.sort((a, b) => {
                const priceA = parseInt(a.querySelector('.pizza-price').textContent.replace('₽', '').trim());
                const priceB = parseInt(b.querySelector('.pizza-price').textContent.replace('₽', '').trim());
                return priceA - priceB; // сортировка по убыванию цены
            });
        }

        const pizzaContainer = document.querySelector('.pizza-container');
        pizzaArray.forEach(pizza => {
            pizza.style.display = 'block'; // Показываем пиццу после сортировки
            pizzaContainer.appendChild(pizza); // Вставляем в DOM отсортированно
        });
    }

    sortPizzas();

    sortMaxButton.addEventListener('click', function() {
        localStorage.setItem('sorting-pizza', 'max');
        sortPizzas();
    });
    sortMinButton.addEventListener('click', function() {
        localStorage.setItem('sorting-pizza', 'min');
        sortPizzas();
    });
});

