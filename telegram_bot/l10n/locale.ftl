# Userful links
# MarkdownV2 style:
# https://core.telegram.org/bots/api#markdownv2-style
# 
# HTML style:
# https://core.telegram.org/bots/api#html-style

# ===== REGISTRATION & PROFILE =====
hi = Привет, ну как там твоя учеба?
hi-user = Привет, { $fullname }, ну как там твоя учеба?
ask-name = Напиши свое ФИО, чтобы ты мог получить заслуженный мерч в конце нашей недели\!
tell-about-pc = Кстати, цены в магазине зависят от того, состоишь ли ты в профкоме, а мерч мы выдаем по студбилету, так что указывай корректные ФИО
thanks-name = Приятно познакомиться, { $fullname }\!
ask-pc = Ты состоишь в профкоме\?
ask-pc-profile = 📝 Ты точно состоишь в профкоме\?
wrong-name = ❌ Неверный формат имени\. Попробуйте ещё раз\.
send-for-manual-check = Если ты действительно состоишь в Профкоме, то я могу отправить запрос на ручную проверку
wait-until-checked = Отлично\! Членство в профкоме отправлено на ручную проверку\. Пока не подтвердится, что ты профкомовец, мерч будет без скидки
ask-to-join = Если хочешь вступить в профком, приходи в кабинет 3528
ask-valid-answer = Я тебя не понимаю\.\.\.😥
Выбери один из вариантов

# Registration buttons
btn-send-for-check = Отправить на ручную проверку
btn-just-kidding = Нет, я пошутил

# Admin text
apply-check = Заявка на проверку статуса **Профкомовца**
    {"*"}Статус*: { $status }
    {"*"}Запросил*: { $fullname } { $username ->
*[Any] \(@{ $username }\)
[None] {""}
    }
apply-checked = { apply-check }
    {"*"}Проверил*: { $verified_by }

# Profile text
profile-title = 📊 Профиль
welcome-account = Добро пожаловать в личный кабинет\!
    {"*"}Пользователь*: { $fullname }
    {"*"}Баланс*: { $balance }i
    {"*"}В Профкоме*: { $apply_status ->
[APPROVED] ✅
*[REJECTED] ❌
[PENDING] ⏳
    }
input-new-name = ✏️ Напишите новое ФИО, например: Иванов Иван Иванович
name-changed = ✅ Имя изменено на { $fullname }
apply-approved-clb = Рады видеть тебя среди членов профкома 😇
deeplink-invalid = Неверный QR код

# Account buttons
btn-edit-name = ✏️ Изменить ФИО
btn-already-in-pc = Я вообще-то в Профкоме 😎

# Profile messages
points-awarded = Баллы начислены
cant-give-points-now = В данный момент нет мероприятий за которые вы можете выдать баллы
already-received = Вы уже получали данные за это мероприятие
apply-on-check-clb = ⏳ Ваша заявка на проверке. Мы уведомим вас, когда она будет рассмотрена.
apply-rejected-clb = 🚫 Ваша заявка отклонена. Если это ошибка - обратитесь в поддержку: /support
# ===== REGISTRATION & PROFILE =====


# ===== PROMOCODES =====
no-promocodes = Нет промокодов
promocode-enter = Введите промокод
promocode-error-not-found = Твой промокод недействителен
promocode-error-deactivated = { promocode-error-not-found }
promocode-error-expired = { promocode-error-not-found }
promocode-error-max-uses = { promocode-error-not-found }
promocode-error-already-activated = Вы уже активировали промокод\!
promocode-error-user-not-found = Пользователь не найден, нажмите /start
promocode-activated = Поздравляю\! Промокод добавлен \({ $cost }i\)
    Ваш баланс: { $balance }i
# ===== PROMOCODES =====


# ===== SUPPORT =====
helping = Задай свой вопрос в поддержку
send-helping = Ваш вопрос отправлен в службу поддержки\. Ожидайте ответа\.
support-question = Новый вопрос от { $fullname }\:
    { $question }
    ||{ $metadata }||
support-sent = Ответ отправлен
support-sent-error = Ответ не отправлен \(пользователь удалил обращение\)
cancel-message = Запрос отменён
# ===== SUPPORT =====


# ===== SCHEDULE & EVENTS =====
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

event-value = Мероприятие
    { $event_name }
    Начинается: { $starts_at }
    Заканчивается: { $ends_at }
    { $desc }
    За посещение начисляется { $event_gives }i

# Event management 
event-creation = Создание мероприятия
delete-events = Удаление мероприятия
delete-this-event = Удалить это мероприятие
ask-for-event-name = Введите название мероприятия
ask-for-event-visit-points = Введите количество получаемых баллов за посещение мероприятия
wrong-points = Неправильный формат начисляемых баллов
wrong-datetime = Неправильный формат времени
ask-for-event-start-time = Введите, когда начинается мероприятие \(Формат\: ДД\.ММ\.ГГГГ ЧЧ\:ММ\)
ask-for-event-end-time = Введите, когда заканчивается мероприятие \(Формат\: ДД\.ММ\.ГГГГ ЧЧ\:ММ\)
ask-for-event-description = Введите описание мероприятия \(или отправьте "\-" для пропуска\):
event-description-too-long = Описание слишком длинное, максимум 1000 символов\.
event-created = Мероприятие создано\!
ask-for-event = За какое мероприятие хотите начислить
# ===== SCHEDULE & EVENTS =====


# ===== SHOP =====
shop-hello = Магазин в разработке
item-value = Товар
    Название: { $item_name }
    Размер: { $item_size }
    Цена: { $full_price }
    Цена по скидке: { $discount_price }
    На складе: { $available_count }

# Shop management
edit-shop-menu = Редактирование магазина
cancel-edit-shop = Редактирование отменено
ask-for-category-create = Введите название категории и прикрепите изображение категории
category-created = Категория создана
item-creation = Создание товара
no-photo = Фото не прикреплено, попробуйте еще раз
no-text = У категории нет названия, попробуйте еще раз
ask-for-category = Выберите категорию
ask-for-item-name = Введите название товара
ask-for-item-size = Укажите размер товара
ask-for-item-full-price = Введите цену товара
ask-for-item-discount-price = Введите цену товара по скидке
ask-for-item-available-count = Введите, сколько товара есть на складе
ask-for-item-in-stock = Укажите, активна ли продажа
ask-for-item-image = Прикрепите изображение товара
item-created = Товар успешно создан
not-a-number = Пожалуйста введите число
# ===== SHOP =====


# ===== ADMIN =====
hello-admin = Показываю меню организатора\. Вы самые лучшие\.\.\.
back-to-menu = Возвращаю в меню\.\.\.
edit-events-menu = Редактирование мероприятия

# Admin buttons
btn-admin-panel = Админ панель
btn-back-to-menu = ◀️ Назад в меню
btn-edit-shop = Редактировать магазин
btn-edit-events = Редактировать мероприятия
btn-give-rights = Выдать права
btn-add-category = Добавить категорию
btn-add-item = Добавить товар
btn-add-event = Добавить мероприятие
btn-delete-event = Удалить мероприятие
btn-delete-item-or-category = Удалить товар или категорию
btn-delete-category = Удалить категорию
btn-delete-item = Удалить этот товар
btn-approve-apply = Принять
btn-decline-apply = Оклонить
btn-review-apply = Пересмотреть
btn-create-promo = Создать промокод
btn-give-event-privileges = Выдать право начислять баллы
# ===== ADMIN =====


# ===== PRIVILEGES =====
ask-for-full-name = Введите ФИО человека, которого ходите наделить правами
wrong-full-name = Человека с таким именем нет в базе данных, попробуйте еще раз
user-privileges = Права пользователя { $fullname }: 
choose-name-from-list = Выберите пользователя из списка
cant-change-privileges-of-yourself = Вы не можете менять свои же права
cant-change-privileges = Вы не можете менять права этого человека

# Privilege types
privilege-grant-privileges = Выдача прав
privilege-edit-promocodes = Создание промокодов
privilege-edit-shop = Редактирование магазина
privilege-edit-events = Редактирование меро
privilege-edit-pk-apply = Рассмотрение заявок в пк
privilege-edit-moderators = Выдача прав ласточкам
# ===== PRIVILEGES =====


# ===== PROMOCODE MANAGEMENT =====
ask-promo-for-creating = Введите промокод для создания
ask-for-attend-promocode = Вы точно хотите создать этот промокод\?
ask-for-cost-promocode = Введите стоимость промокода
ask-for-max-uses = Введите максимальное количество использований
wrong-cost = Введи допустимое число для цены
promo-added = Промокод добавлен\. Возвращаю тебя в меню админов
promo-exist = Такой промокод существует
wrong-usages = Некорректное число максимальных использований
you-have-not-rights = У тебя нет прав
promocode-too-short = Прокомод слишком короткий \(не менее 5 символов\)
promocode-too-long = Промокод слишком длинный \(не более 25 символов\)
promocode-creation-error = Что\-то пошло не так\. Промокод не создан
show-this-qr = Для активации промокода можно отсканировать данный QR\-код
# ===== PROMOCODE MANAGEMENT =====


# ===== COMMON UI =====
# Common buttons
btn-cancel = Отмена
btn-yes = Да
btn-no = Нет
btn-back = Назад
cancel = Отмена
btn-user-codes = Использованные коды
btn-emoji-yes = ✅
btn-emoji-no = ❌

# Menu buttons
btn-support = Поддержка
btn-schedule = Расписание
btn-my-code = Мой код
btn-enter-promocode = Ввести Промокод
btn-profile = Профиль
btn-shop = Магазин

# Placeholders
placeholder-menu = Выберите элемент меню
placeholder-category = Выберите категорию
placeholder-item = Выберите товар
placeholder-item-size = Выберите размер товара
placeholder-get-back-to-item = Назад к товарам
placeholder-event = Выберите мероприятие
# ===== COMMON UI =====


# ===== LOGGING =====
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
# ===== LOGGING =====