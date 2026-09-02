# Импортируем основную библиотеку для работы с VK API
import vk_api


# Импортируем Long Polling для получения событий в реальном времени
# VkLongPoll — класс для подключения к Long Polling
# VkEventType — список типов событий (новое сообщение, звонок и так далее)
from vk_api.longpoll import VkLongPoll, VkEventType


# Импортируем инструменты для создания кнопок
# VkKeyboard — класс для создания клавиатуры
# VkKeyboardColor — цвета кнопок (синий, белый, зелёный, красный)
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


# Токен доступа сообщества — секретный ключ для работы с API
# Получить можно в: Управление сообществом → Работа с API → Ключи доступа
TOKEN = ""

# Создаём сессию — устанавливаем соединение с VK через токен
vk_session = vk_api.VkApi(token=TOKEN)


# Получаем объект для вызова методов API (отправка сообщений и т.д.)
vk = vk_session.get_api()


# Запускаем Long Polling — бот начинает слушать входящие события
longpoll = VkLongPoll(vk_session)


def create_keyboard():
   """Создаём клавиатуру с кнопками"""


   # one_time=False — клавиатура остаётся на экране после каждого нажатия
   # one_time=True — клавиатура скрывается после первого нажатия
   keyboard = VkKeyboard(one_time=False)


   # Добавляем кнопку «Помощь» синего цвета (PRIMARY = синий)
   keyboard.add_button("Помощь", color=VkKeyboardColor.PRIMARY)


   # Добавляем кнопку «О боте» белого цвета (SECONDARY = белый)
   keyboard.add_button("О боте", color=VkKeyboardColor.SECONDARY)


   # Переходим на новую строку — следующие кнопки будут ниже
   keyboard.add_line()


   # Добавляем кнопку «Закрыть меню» красного цвета (NEGATIVE = красный)
   # Красный цвет визуально сигнализирует об отмене или закрытии
   keyboard.add_button("Закрыть меню", color=VkKeyboardColor.NEGATIVE)


   # Возвращаем клавиатуру в формате JSON для отправки через API
   return keyboard.get_keyboard()


# Запускаем бесконечный цикл прослушивания событий
for event in longpoll.listen():


   # Проверяем два условия одновременно:
   # event.type == VkEventType.MESSAGE_NEW — событие является новым сообщением
   # event.to_me — сообщение адресовано боту (не от бота)
   if event.type == VkEventType.MESSAGE_NEW and event.to_me:


       # Читаем текст сообщения и переводим в нижний регистр
       # Это нужно чтобы «Привет», «ПРИВЕТ» и «привет» воспринимались одинаково
       user_message = event.text.lower()


       # Сохраняем ID пользователя, чтобы знать кому отправлять ответ
       user_id = event.user_id


       # Проверяем приветственные слова — реагируем на несколько вариантов сразу
       if user_message in ["привет", "начать", "start"]:
           reply = "Привет! Выбери действие:"
           # Отправляем сообщение вместе с клавиатурой
           vk.messages.send(
               user_id=user_id,  # Кому отправляем
               message=reply,  # Текст сообщения
               keyboard=create_keyboard(),  # Прикрепляем клавиатуру с кнопками
               random_id=0  # Защита от дублирования (0 = учебный режим)
           )


       # Если пользователь нажал кнопку «Помощь» или написал это слово
       elif user_message == "помощь":
           reply = "Я помогаю отвечать на вопросы. Выбери нужный пункт в меню."


           # Отправляем ответ без клавиатуры — она уже есть на экране
           vk.messages.send(user_id=user_id, message=reply, random_id=0)


       # Если пользователь нажал кнопку «О боте» или написал это слово
       elif user_message == "о боте":
           reply = "Бот написан на Python с использованием библиотеки vk-api."
           vk.messages.send(user_id=user_id, message=reply, random_id=0)
