import json
import os
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram import types
from client import MyRpcClient

class Gen(StatesGroup):
    wait_for_style = State()
    wait_for_answer = State()

class HandlerMessages:
    def __init__(
            self,
            dispatcher: Dispatcher,
            sendler: MyRpcClient
    ):
        self._dispatcher = dispatcher
        self._sendler = sendler

    def register_start_message_handler(self) -> None:
        """Начало работы с ботом"""
        @self._dispatcher.message_handler(commands = "start")
        async def starting_bot(message: types.Message):
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
            buttons = ["Да, конечно!", "Нет, не хочу."]
            keyboard.add(*buttons)
            await message.answer("Привет! Я умею стилизировать изображения, хочешь попробовать?", reply_markup = keyboard)

    def input_photo(self) -> None: 
        "Получение от пользователя фотографии, перевод пользователя в состояние ожидания выбора стиля"      
        @self._dispatcher.message_handler(content_types = ['photo'])
        async def get_user_photo(message):
            await message.photo[-1].download('/Users/macbookpro/work_bot/content_image' + str(message.from_user.id) + '.jpg')
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width = 1)
            button = ["В.В.Кандинский «Композиция VII»", "К.Хокусай «Большая волна в Канагаве»", "И.К.Айвазовский «Океан»", "Акварельные краски", "Э.Р.Кальзадо «Начало»"]
            markup.add(*button)
            await Gen.wait_for_style.set()
            await message.answer("Отлично! У меня есть несколько стилей, которые я могу предложить тебе. Выбери заинтересовавший стиль.",  reply_markup = markup)

    def input_message_and_wait_handler(self) -> None:
        """Пользователь согласился на стилизацию"""
        @self._dispatcher.message_handler(Text(equals = "Да, конечно!"))
        async def await_input_from_user(message: types.Message):
            await message.answer("Замечательно! Отправь мне изображение, которое хочешь стилизовать.")

    async def get_answer_and_reply(self, id: int, message: str, state: FSMContext) -> None:
        """Получение ответа от сервера, отправка результата пользователю, сброс состояния"""
        response = await self._sendler.call(message, id)
        answer = json.loads(response.decode("UTF-8"))
        await self._dispatcher.bot.send_photo(answer['user_id'], photo = open('/Users/macbookpro/work_bot/stylized_image' + str(answer['user_id']) + '.jpg', 'rb'))
        await self._dispatcher.bot.send_message(answer['user_id'], 'Мне нравится результат! Отправь новую фотографию для стилизации.')
        os.remove('/Users/macbookpro/work_bot/content_image' + str(answer['user_id']) + '.jpg')
        os.remove('/Users/macbookpro/work_bot/stylized_image' + str(answer['user_id']) + '.jpg')
        await state.finish()

    def send_and_reply_message(self) -> None:
        """Получение ответа от пользователя, отправка запроса к серверу"""
        @self._dispatcher.message_handler(state = Gen.wait_for_style)
        async def answer_on_input(message: types.Message, state: FSMContext):
            await message.answer("Нужно чуточку подождать!")
            await state.finish()
            await Gen.wait_for_answer.set()
            # Запрос к серверу
            if(message.text == "В.В.Кандинский «Композиция VII»"):
                await self.get_answer_and_reply(message.from_user.id, 'kandinskyVII_10000.pth', state)
            elif(message.text == "К.Хокусай «Большая волна в Канагаве»"):
                await self.get_answer_and_reply(message.from_user.id, '/Users/macbookpro/checkpoints/результаты/wave_10000.pth', state)
            elif(message.text == "И.К.Айвазовский «Океан»"):
                await self.get_answer_and_reply(message.from_user.id, '/Users/macbookpro/checkpoints/результаты/aivazovsky-ocean_5000.pth', state)
            elif(message.text == "Акварельные краски"):
                await self.get_answer_and_reply(message.from_user.id, '/Users/macbookpro/checkpoints/результаты/akvarel_9000.pth', state)
            elif(message.text == "Э.Р.Кальзадо «Начало»"):
                await self.get_answer_and_reply(message.from_user.id, '/Users/macbookpro/checkpoints/результаты/kalzado_10000.pth', state)
    
    def send_bot_about(self) -> None:
        """Пользователь отказался от стилизации"""
        @self._dispatcher.message_handler(Text(equals = "Нет, не хочу."))
        async def not_bot(message: types.Message):
            await message.answer("Жаль! Отправь мне «/start», если всё-таки захочешь приступить к стилизации изображения.")   

    def first_register_start_message_handler(self) -> None:
        """Начало работы с ботом при наличии состояния"""
        @self._dispatcher.message_handler(commands = "start", state = Gen.wait_for_answer)
        async def first_starting_bot(message: types.Message, state: FSMContext):
            await state.finish()
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
            buttons = ["Да, конечно!", "Нет, не хочу."]
            keyboard.add(*buttons)
            await message.answer("Привет! Я умею стилизировать изображения, хочешь попробовать?", reply_markup = keyboard) 
    
    def block_message_for_generation(self) -> None:
        """Блокирование пользователю новых запросов, пока не будет получен ответ от сервера"""
        @self._dispatcher.message_handler(content_types=['text'], state = Gen.wait_for_answer)
        async def warning_gen(message: types.Message, state: FSMContext):
            await message.answer("Сначала необходимо дождаться окончания генерации!")
            
    def register_all_handlers(self) -> None:
        self.register_start_message_handler()
        self.input_photo()
        self.input_message_and_wait_handler()
        self.send_and_reply_message()
        self.send_bot_about()
        self.first_register_start_message_handler()
        self.block_message_for_generation()
