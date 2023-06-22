# Style-Transfer-Telegram-Bot
Проект - телеграм бот стилизации изображений. Стилизация изображений происходит за счет предварительно подготовленной свёрточной нейронной сети выделения признаков изображений - VGG16, обученной мною для пяти стилей. Обученные веса модели можно скачать [здесь](https://disk.yandex.ru/d/0HQSxoOTknugWw). Телеграм бот реализован с помощью библиотеки aiogram в асинхронном режиме. Для хранения запросов пользователей в виде «ключ-значение» используется хранилище данных Redis. Очереди сообщений реализуются с помощью брокера сообщений RabbitMQ. Загрузка обученных весов модели и хранение присылаемых пользователем изображений и сгенерированных изображений реализуются с помощью монтирования локальных папок.
## Структура репозитория
1. [Model](https://github.com/VetaShine/Style-Transfer-Telegram-Bot/tree/main/model) - модель нейронной сети стилизации изображений 
* [train](https://github.com/VetaShine/Style-Transfer-Telegram-Bot/blob/main/model/train.py) - обучение модели
* [models](https://github.com/VetaShine/Style-Transfer-Telegram-Bot/blob/main/model/models.py) - определение модели
* [utils](https://github.com/VetaShine/Style-Transfer-Telegram-Bot/blob/main/model/utils.py) - функции для работы с изображениями
* [test_on_image](https://github.com/VetaShine/Style-Transfer-Telegram-Bot/blob/main/model/test_on_image.py) - тестирование модели
* [style-images](https://github.com/VetaShine/Style-Transfer-Telegram-Bot/tree/main/model/style-images) - стилевые изображения
* [training](https://github.com/VetaShine/Style-Transfer-Telegram-Bot/blob/main/model/Neural_Style_Transfer_Training.ipynb) - notebook обучения модели 
* [launching](https://github.com/VetaShine/Style-Transfer-Telegram-Bot/blob/main/model/Neural_Style_Transfer_Launching.ipynb) - notebook запуска тестирования модели
2. [Bot](https://github.com/VetaShine/Style-Transfer-Telegram-Bot/tree/main/bot) - телеграм бот
* [app](https://github.com/VetaShine/Style-Transfer-Telegram-Bot/blob/main/bot/app.py) - запуск бота, создание диспетчера
* [client](https://github.com/VetaShine/Style-Transfer-Telegram-Bot/blob/main/bot/client.py) - общение с очередями сообщений в RabbitMQ
* [handler](https://github.com/VetaShine/Style-Transfer-Telegram-Bot/blob/main/bot/handler.py) - обработка сообщений телеграм бота 
3. [Server](https://github.com/VetaShine/Style-Transfer-Telegram-Bot/tree/main/server) - сервер, стилизирующий изображения 
* [server](https://github.com/VetaShine/Style-Transfer-Telegram-Bot/blob/main/server/server.py) - реализация сервера
## Архитектура проекта
![screenshot of sample](https://github.com/VetaShine/OOPch/blob/main/img.jpg)
## Запуск с помощью docker-compose
Перед запуском в файле docker-compose.yml нужно добавить токен бота в апострофы в 42 строке, установить пароль для хранилища данных Redis в 18 строке после ключа «--requirepass» и этот же пароль записать в апострофы в 45 строке, также поменять путь к папке хранения присылаемых и генерируемых изображений в 33, 52 строках и путь к папке с обученными весами модели в 34, 53 строках. Команды запуска проекта: `docker-compose build`, затем `docker-compose up`.
## Демонстрация работы телеграм бота
![screenshot of sample](https://github.com/VetaShine/OOPch/blob/main/1.jpg)
![screenshot of sample](https://github.com/VetaShine/OOPch/blob/main/2.jpg)
![screenshot of sample](https://github.com/VetaShine/OOPch/blob/main/3.jpg)
![screenshot of sample](https://github.com/VetaShine/OOPch/blob/main/4.jpg)
