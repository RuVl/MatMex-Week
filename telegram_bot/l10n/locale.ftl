#register messages
hi = Привет, ну как там твоя учеба?
hi-user = Привет, { $fullname }, ну как там твоя учеба?
ask-name = Напиши свое ФИО, чтобы ты мог получить заслуженный мерч в конце нашей недели\!
tell-about-pc = Кстати, цены в магазине зависят от того, состоишь ли ты в профкоме, а мерч мы выдаем по студбилету, так что указывай корректные ФИО

выдаем по студбилету, так что не ошибайся при вводе данных\!
roll-back-name = Введи ФИО

helping = Задай свой вопрос в поддержку
send-helping = Ваш вопрос отправлен в службу поддержки\. Ожидайте ответа\.
new-support-question = Новый вопрос в поддержку\. Ответьте на следующее сообщение:  

cancel = Отмена
cancel-message = Запрос отменён
promocode_enter = Введите промокод
sad-promo-message = Твой промокод недействителен\(
good-promo-message = Поздравляю! Промокод добавлен
code_message = Твой промокод:
phrase_profile = Привет, это твой профиль
thanks-name = Приятно познакомиться
thanks-name-html = Приятно познакомиться { $fullname }!
ask-pc = Ты состоишь в профкоме\?
wrong-name = Неправильный формат ФИО, попробуй еще раз
send-for-manual-check = Если ты действительно состоишь в Профкоме, то я могу отправить запрос на ручную проверку
wait-until-checked = Отлично\! Членство в профкоме отправлено на ручную проверку\. Пока не подтвердится, что ты профкомовец, мерч будет без скидки
ask-to-join = Если хочешь вступить в профком, приходи в кабинет 3528
ask-valid-answer = Я тебя не понимаю\.\.\.😥
Выбери один из вариантов
already-in-pc = Рады видеть тебя среди членов профкома\)

# Account/Profile messages
phrase_profile = Привет, это твой профиль
account-temp = Мой аккаунт
input-new-name = Введите новое ФИО
cancel-change-name = Редактирование ФИО отменено
name-changed = ФИО успешо изменено\! Приятно познакомиться
user_is = Пользователь:
balance_is = Баланс:
deeplink-valid = Баллы начислены
deeplink-invalid = Баллы не начислены Ошибка на стороне сервера
deeplink-badrequest = Вы уже получали данные за это мероприятие

# Support messages
helping = Задай свой вопрос в поддержку
sent-helping = Ваш вопрос отправлен в службу поддержки\. Ожидайте ответа\.
support-question = Новый вопрос от { $fullname }\:
    { $question }
    ||{ $metadata }||
support-sent = Ответ отправлен

# Promocode messages
promocode_enter = Введите промокод
sad-promo-message = Твой промокод недействителен \({ $message }\)
good-promo-message = Поздравляю! Промокод добавлен \({ $cost } баллов\)
    Ваш баланс: { $balance } баллов
code_message = Твой промокод:

# Schedule 
schedule-keyboard = Информация о меоприятиях
schedule-text-html = 🎉 65-я Неделя Матмеха
    Солнечные лучи заливают улицы, весна уверенно вступает в свои права! ☀️
    А значит — самое время поделиться новостями о предстоящей 65-й Неделе Матмеха!

    💫 С 21 по 30 апреля вас ждут интеллектуальные, музыкальные, творческие и спортивные мероприятия —
    прекрасная возможность отвлечься от учебы и отлично провести время.

    📆 Программа мероприятий:

    🔸 21.04 (пн) — «Что? Где? Когда?» (1 тур)
    🔸 22.04 (вт) — Литмуз
    🔸 23.04 (ср) — День Карьеры
    🔸 24.04 (чт) — Псевдонаучная конференция, Турнир по настольному теннису
    🔸 25.04 (пт) — День Матмеха
    🔸 26.04 (сб) — Турнир по шахматам
    🔸 27.04 (вс) — Турнир по волейболу
    🔸 28.04 (пн) — «Что? Где? Когда?» (финал)
    🔸 29.04 (вт) — Турнир по баскетболу
    🔸 30.04 (ср) — Дискотека

    Следите за анонсами в нашей группе и Телеграм-канале Профкома.

# Admin messages
ask-promo-for-creating = Введите промокод для создания
hello-admin = Показываю меню организатора\. Вы самые лучшие\.\.\.

ask-for-event = За какое мероприятие хотите начислить
ask-for-id = Введите код участника
wrong-event-or-no-rights = У вас нет прав начисления баллов за это меро, либо такого меро не существует
give-points = Баллы успешно начислены
wrong-id = Участника с таким кодом не существует, попробуйте еще раз
cancel-code-scanner-message = Сканирование кода отменено 
back-to-menu = Возвращаю обратно в меню
check-pk-apply = Пользователь { $fullname } запросил проверку на наличие статуса 
Профкомовца
something-went-wrong = Ошибка, проверьте логи
select-status-cb = Одобрите или отклоните заяку (сейчас статус не изменен)
ask-for-attend-promocode = Вы точно хотите создать этот промокод\?
ask-for-cost-promocode = Введите стоимость промокода
ask-for-max-uses = Введите максимальное количество использований
wrong-cost = Введи допустимое число для цены
promo_added = Промокод добавлен\. Возвращаю тебя в меню админов
promo_exist = Такой промокод существует
wrong-usages = Некорректное число максимальных использований
you-have-not-rights = У тебя нет прав

# Grant privilege messages
ask-for-full-name = Введите ФИО человека, которого ходите наделить правами
wrong-full-name = Человека с таким именем нет в базе данных, попробуйте еще раз
user-privileges = Права пользователя: 
choose-name-from-list = Выберите пользователя из списка
cant-change-privileges-of-yourself = Вы не можете менять свои же права
cant-change-privileges = Вы не можете менять права этого человека
privilege-grant-privileges = Выдача прав
privilege-edit-promocodes = Создание промокодов
privilege-edit-shop = Редактирование магазина
privilege-edit-events = Редактирование меро
privilege-edit-pk-apply = Рассмотрение заявок в пк
privilege-edit-moderators = Выдача прав ласточкам

# Shop messages
edit-shop-menu = Редактирование магазина
cancel_edit_shop = Редактирование отменено
ask-for-category-create = Введите название категории и прикрепите изображение категории
creating-category-cancelled = Создание категории отменено
category-created = Категория создана
edit-category = Редактирование категории
item-creation = Создание товара
ask-for-name-item = Введите название
ask-for-size = Введите размер
ask-for-price = Введите цену
ask-for-count = Введите количество
delete-item = Товар удален
cancel-edit-item = Отменено
create-item = Товар создан
no-photo = Фото не прикреплено, попробуйте еще раз
no-text = У категории нет названия, попробуйте еще раз
failed-download = Ошибка загрузки фото, попробуйте еще раз
ask-for-category = Выберите категорию
category-name-already-exists = Категория с таким названием уже существует, попробуйте еще раз
category-deleted = Категория успешно удалена
category-not-exists = Категории с таким именем не существует, попробуйте еще раз
ask-for-item-name = Введите название товара
ask-for-item-size = Укажите размер товара
ask-for-item-full-price = Введите цену товара
ask-for-item-discount-price = Введите цену товара по скидке
ask-for-item-available-count = Введите, сколько товара есть на складе
ask-for-item-in-stock = Укажите, активна ли продажа
ask-for-item-image = Прикрепите изображение товара
item-create-error = Не получилось создать товар, товар с таким именем уже существует
item-created = Товар успешно создан
item-not-exists = Товар с таким именем не существует, попробуйте еще раз
item-deleted = Товар успешно удален
not-a-number = Пожалуйста введите число
not-a-yes-no = Введите Да или Нет

# Scedule messages:
event-creation = Создание мероприятия
delete-events = Удаление мероприятия
delete-this-event = Удалить это мероприятие
ask-for-event-name = Введите название мероприятия
wrong-datetime = Неправильный формат времени
ask-for-event-start-time = Введите, когда начинается мероприятие \(Формат\: ДД\.ММ\.ГГГГ ЧЧ\:ММ\)
ask-for-event-end-time = Введите, когда заканчивается мероприятие \(Формат\: ДД\.ММ\.ГГГГ ЧЧ\:ММ\)
ask-for-event-grants = Введите, сколько баллов дает мероприятие
event-created = Мероприятие создано\!
event-value = Мероприятие
    { $eventname }
    Начинается: { $startsat }
    Заканчивается: { $endsat }
    За посещение начисляется { $eventgives }i

# Account messages
welcome-account = Добро пожаловать в личный кабинет\!
    Пользователь: { $fullname }
    Баланс: { $balance }i
input-new-name = Введите новое ФИО
cancel-change-name = Редактирование ФИО отменено
name-changed = ФИО успешо изменено\! Приятно познакомиться, { $fullname }\!
already-in-pc = Мы знаем\) Это отмечено в твоем профиле

# Common buttons
btn-cancel = Отмена
btn-yes = Да
btn-no = Нет
btn-back = Назад
cancel = Отмена
btn-user-codes = Использованные коды
btn-emoji-yes = ✅
btn-emoji-no = ❌

#shop messages
shop-hello = Магазин
item-value = Товар
    Название: { $itemname }
    Размер: { $itemsize }
    Цена: { $fullprice }
    Цена по скидке: { $discountprice }
    На складе: { $availablecount }

# Menu buttons
btn-support = Поддержка
btn-schedule = Расписание
btn-my-code = Мой код
btn-enter-promocode = Ввести Промокод
btn-profile = Профиль
btn-shop = Магазин

# Account buttons
btn-edit-name = Редактировать ФИО
btn-already-in-pc = Я вообще-то в пк

# Registration buttons
btn-send-for-check = Отправить на ручную проверку
btn-just-kidding = Нет, я пошутил
apply-check = Заявка на проверку статуса **Профкомовца**
    {"*"}*Статус**: { $status }
    {"*"}*Запросил**: { $fullname } \(@{ $username }\)
apply-checked =  { apply-check }
    {"*"}*Проверил**: { $verified_by }

# Admin buttons
btn-admin-panel = Админ панель
btn-back-to-menu = В меню
btn-edit-shop = Редактировать магазин
btn-edit-events = Редактировать мероприятия
btn-give-rights = Выдать права
btn-create-promocode = Создание промокода
btn-list-promocodes = Список промокодов
btn-grant-rights = Выдать права
btn-add-category = Добавить категорию
btn-edit-category = Редактировать категорию
btn-add-item = Добавить товар
btn-add-event = Добавить мероприятие
btn-delete-event = Удалить мероприятие
btn-edit-item = Редактировать товар
btn-delete-item-or-category = Удалить товар или категорию
btn-delete-category = Удалить эту категорию
btn-delete-item = Удалить этот товар
btn-add-custom-prize = Добавить приз
btn-send-support = Отправить ответ
btn-cancel-support = Отмена
btn-approve-apply = Принять
btn-decline-apply = Оклонить
btn-review-apply = Пересмотреть
btn-create-promo = Создать промокод
btn-delete-category = Удалить категорию

# Account buttons
btn-edit-name = Редактировать ФИО
btn-already-in-pc = Я вообще-то в пк

# Registration buttons
btn-send-for-check = Отправить на ручную проверку
btn-just-kidding = Нет, я пошутил

# Shop category buttons
btn-tshirts = Футболки
btn-bracelets = Браслеты
btn-id-covers = Обложки на студ.билеты
btn-shoppers = Шопперы

# Placeholders
placeholder-menu = Выберите элемент меню
placeholder-category = Выберите категорию
placeholder-code = Введите промокод
placeholder-item = Выберите товар
placeholder-item-size = Выберите размер товара
placeholder-get-back-to-item = Назад к товарам
placeholder-event = Выберите мероприятие

# Log messages
log-handler-called = Вызван обработчик
log-handler-completed = Обработчик завершил работу
log-user-message-received = Получено сообщение от пользователя
log-state-changed = Изменено состояние пользователя
log-command-executed = Выполнена команда
log-promocode-entered = Введен промокод
log-promocode-invalid = Недействительный промокод
log-promocode-valid = Действительный промокод
log-user-data-fetched = Получены данные пользователя
log-admin-action = Выполнено действие администратора
log-profile-action = Действие в профиле
log-name-changed = Изменено имя пользователя

# Profile messages
points-awarded = Баллы начислены
no-rights = Нет достаточных прав
deeplink-invalid = Баллы не начислены Ошибка на стороне сервера
already-received = Вы уже получали данные за это мероприятие