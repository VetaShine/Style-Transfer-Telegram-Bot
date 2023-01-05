# Style-Transfer-Telegram-Bot
Проект по предмету "Объектно-ориентированное программирование" - телеграм бот стилизации изображений. Стилизация изображений происходит за счет предварительно подготовленной свёрточной нейронной сети выделения признаков изображений - VGG16 , обученной мною для пяти стилей. Обученные веса модели можно скачать [здесь](https://disk.yandex.ru/d/0HQSxoOTknugWw). Телеграм бот реализован с помощью библиотеки aiogram в асинхронном режиме.
## Структура проекта:
1. [Model](https://github.com/VetaShine/Style-Transfer-Telegram-Bot/tree/main/model) - модель нейронной сети стилизации изображений 
* [train](https://github.com/VetaShine/Style-Transfer-Telegram-Bot/blob/main/model/train.py) - программа обучения модели
* [models](https://github.com/VetaShine/Style-Transfer-Telegram-Bot/blob/main/model/models.py) - программа определения модели
* [utils](https://github.com/VetaShine/Style-Transfer-Telegram-Bot/blob/main/model/utils.py) - программа 
* [test_on_image](https://github.com/VetaShine/Style-Transfer-Telegram-Bot/blob/main/model/test_on_image.py) - программа тестирования модели
* [style-images](https://github.com/VetaShine/Style-Transfer-Telegram-Bot/tree/main/model/style-images) - стилевые изображения
* [training](https://github.com/VetaShine/Style-Transfer-Telegram-Bot/blob/main/model/Neural_Style_Transfer_Training.ipynb) - notebook обучения модели 
* [launching](https://github.com/VetaShine/Style-Transfer-Telegram-Bot/blob/main/model/Neural_Style_Transfer_Launching.ipynb) - notebook запуска тестирования модели
