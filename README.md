# Style-Transfer-Telegram-Bot
Проект по предмету "Объектно-ориентированное программирование" - телеграм бот стилизации изображений. Стилизация изображений происходит за счет предварительно подготовленной свёрточной нейронной сети выделения признаков изображений - VGG16 , обученной мною для пяти стилей. Обученные веса модели можно скачать [здесь](https://disk.yandex.ru/d/0HQSxoOTknugWw). Телеграм бот реализован с помощью библиотеки aiogram в асинхронном режиме.
## Структура проекта:
1. [Model](https://github.com/VetaShine/Style-Transfer-Telegram-Bot/tree/main/model) - модель нейронной сети стилизации изображений
* [models](https://github.com/VetaShine/Style-Transfer-Telegram-Bot/blob/main/model/models.py) -  
* [utils](https://github.com/VetaShine/Style-Transfer-Telegram-Bot/blob/main/model/utils.py) - 
* [train](https://github.com/VetaShine/Style-Transfer-Telegram-Bot/blob/main/model/train.py) - 
* [test_on_image](https://github.com/VetaShine/Style-Transfer-Telegram-Bot/blob/main/model/test_on_image.py) - 
* [style-images](https://github.com/VetaShine/Style-Transfer-Telegram-Bot/tree/main/model/style-images) - 
* [training]() - 
* [launching]() - 
