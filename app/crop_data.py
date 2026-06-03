"""
База данных культур и сортов.
Содержит информацию о периоде полива и времени созревания.
"""

CROP_CATALOG = [
    # Томаты
    {"crop_name": "Томат", "variety": "Бычье сердце", "watering_interval_days": 4, "days_to_harvest": 120, "emoji": "🍅",
     "description": "Крупноплодный сорт, мясистый. Для салатов и сока."},
    {"crop_name": "Томат", "variety": "Черри Красный", "watering_interval_days": 3, "days_to_harvest": 90, "emoji": "🍅",
     "description": "Мелкоплодный, очень сладкий. Идеален для салатов."},
    {"crop_name": "Томат", "variety": "Де Барао", "watering_interval_days": 4, "days_to_harvest": 115, "emoji": "🍅",
     "description": "Высокорослый, устойчивый. Хорош для консервирования."},
    {"crop_name": "Томат", "variety": "Санька", "watering_interval_days": 4, "days_to_harvest": 80, "emoji": "🍅",
     "description": "Ультраранний, неприхотливый, компактный."},
    {"crop_name": "Томат", "variety": "Розовый гигант", "watering_interval_days": 4, "days_to_harvest": 110, "emoji": "🍅",
     "description": "Крупные розовые плоды, сладкий вкус."},

    # Огурцы
    {"crop_name": "Огурец", "variety": "Кураж F1", "watering_interval_days": 2, "days_to_harvest": 45, "emoji": "🥒",
     "description": "Самоопыляемый, высокоурожайный гибрид для теплиц."},
    {"crop_name": "Огурец", "variety": "Нежинский", "watering_interval_days": 2, "days_to_harvest": 50, "emoji": "🥒",
     "description": "Классический засолочный сорт. Пчелоопыляемый."},
    {"crop_name": "Огурец", "variety": "Маша F1", "watering_interval_days": 2, "days_to_harvest": 40, "emoji": "🥒",
     "description": "Раннеспелый гибрид, хрустящий, без горечи."},
    {"crop_name": "Огурец", "variety": "Зозуля F1", "watering_interval_days": 2, "days_to_harvest": 48, "emoji": "🥒",
     "description": "Длинноплодный, для салатов. Теплица."},

    # Перец
    {"crop_name": "Перец сладкий", "variety": "Калифорнийское чудо", "watering_interval_days": 3, "days_to_harvest": 130, "emoji": "🫑",
     "description": "Толстостенный, крупный, сладкий."},
    {"crop_name": "Перец сладкий", "variety": "Богатырь", "watering_interval_days": 3, "days_to_harvest": 120, "emoji": "🫑",
     "description": "Среднеспелый, крупноплодный, устойчивый."},
    {"crop_name": "Перец сладкий", "variety": "Ласточка", "watering_interval_days": 3, "days_to_harvest": 110, "emoji": "🫑",
     "description": "Раннеспелый, конусовидный, урожайный."},

    # Морковь
    {"crop_name": "Морковь", "variety": "Нантская 4", "watering_interval_days": 5, "days_to_harvest": 100, "emoji": "🥕",
     "description": "Классический среднеспелый сорт, сладкая, ровная."},
    {"crop_name": "Морковь", "variety": "Шантанэ", "watering_interval_days": 5, "days_to_harvest": 110, "emoji": "🥕",
     "description": "Конусовидная, крупная, хорошо хранится."},
    {"crop_name": "Морковь", "variety": "Лосиноостровская 13", "watering_interval_days": 5, "days_to_harvest": 95, "emoji": "🥕",
     "description": "Высокое содержание каротина, сочная."},

    # Картофель
    {"crop_name": "Картофель", "variety": "Невский", "watering_interval_days": 7, "days_to_harvest": 80, "emoji": "🥔",
     "description": "Среднеранний, белая мякоть, высокоурожайный."},
    {"crop_name": "Картофель", "variety": "Ред Скарлетт", "watering_interval_days": 7, "days_to_harvest": 75, "emoji": "🥔",
     "description": "Раннеспелый, красная кожура, жёлтая мякоть."},
    {"crop_name": "Картофель", "variety": "Адретта", "watering_interval_days": 7, "days_to_harvest": 70, "emoji": "🥔",
     "description": "Рассыпчатый, великолепный вкус, раннеспелый."},

    # Капуста
    {"crop_name": "Капуста белокочанная", "variety": "Слава 1305", "watering_interval_days": 3, "days_to_harvest": 120, "emoji": "🥬",
     "description": "Среднеспелая, для квашения и хранения."},
    {"crop_name": "Капуста белокочанная", "variety": "Июньская", "watering_interval_days": 3, "days_to_harvest": 90, "emoji": "🥬",
     "description": "Раннеспелая, нежные листья, для салатов."},

    # Свёкла
    {"crop_name": "Свёкла", "variety": "Бордо 237", "watering_interval_days": 5, "days_to_harvest": 100, "emoji": "🟣",
     "description": "Тёмно-красная, сладкая, хорошо хранится."},
    {"crop_name": "Свёкла", "variety": "Цилиндра", "watering_interval_days": 5, "days_to_harvest": 110, "emoji": "🟣",
     "description": "Удлинённая форма, равномерная мякоть."},

    # Лук
    {"crop_name": "Лук репчатый", "variety": "Штутгартер Ризен", "watering_interval_days": 5, "days_to_harvest": 95, "emoji": "🧅",
     "description": "Золотистый, острый, хорошо хранится."},
    {"crop_name": "Лук репчатый", "variety": "Ред Барон", "watering_interval_days": 5, "days_to_harvest": 100, "emoji": "🧅",
     "description": "Красный, полуострый, для салатов."},

    # Чеснок
    {"crop_name": "Чеснок", "variety": "Любаша", "watering_interval_days": 7, "days_to_harvest": 100, "emoji": "🧄",
     "description": "Озимый, крупный, морозоустойчивый."},
    {"crop_name": "Чеснок", "variety": "Комсомолец", "watering_interval_days": 7, "days_to_harvest": 110, "emoji": "🧄",
     "description": "Озимый, острый, стрелкующийся."},

    # Зелень
    {"crop_name": "Укроп", "variety": "Грибовский", "watering_interval_days": 3, "days_to_harvest": 40, "emoji": "🌿",
     "description": "Раннеспелый, ароматный, универсальный."},
    {"crop_name": "Петрушка", "variety": "Обыкновенная листовая", "watering_interval_days": 4, "days_to_harvest": 60, "emoji": "🌿",
     "description": "Листовая, ароматная, неприхотливая."},
    {"crop_name": "Базилик", "variety": "Фиолетовый", "watering_interval_days": 2, "days_to_harvest": 50, "emoji": "🌿",
     "description": "Яркий аромат, фиолетовые листья."},
    {"crop_name": "Салат", "variety": "Айсберг", "watering_interval_days": 2, "days_to_harvest": 45, "emoji": "🥬",
     "description": "Хрустящий кочанный салат."},
    {"crop_name": "Салат", "variety": "Лолло Росса", "watering_interval_days": 2, "days_to_harvest": 40, "emoji": "🥬",
     "description": "Листовой, красноватый, нежный вкус."},

    # Кабачки и тыква
    {"crop_name": "Кабачок", "variety": "Цукеша", "watering_interval_days": 4, "days_to_harvest": 50, "emoji": "🟢",
     "description": "Цуккини, раннеспелый, компактный куст."},
    {"crop_name": "Кабачок", "variety": "Грибовский 37", "watering_interval_days": 4, "days_to_harvest": 55, "emoji": "🟢",
     "description": "Белоплодный, неприхотливый, для консервации."},
    {"crop_name": "Тыква", "variety": "Мускатная", "watering_interval_days": 5, "days_to_harvest": 120, "emoji": "🎃",
     "description": "Сладкая, ароматная, для каш и выпечки."},
    {"crop_name": "Тыква", "variety": "Стофунтовая", "watering_interval_days": 5, "days_to_harvest": 130, "emoji": "🎃",
     "description": "Очень крупная, для хранения и переработки."},

    # Горох и фасоль
    {"crop_name": "Горох", "variety": "Альфа", "watering_interval_days": 4, "days_to_harvest": 55, "emoji": "🟢",
     "description": "Раннеспелый, лущильный, сладкий."},
    {"crop_name": "Фасоль", "variety": "Сакса", "watering_interval_days": 4, "days_to_harvest": 50, "emoji": "🫘",
     "description": "Спаржевая, без волокон, нежная."},

    # Редис
    {"crop_name": "Редис", "variety": "Жара", "watering_interval_days": 2, "days_to_harvest": 25, "emoji": "🔴",
     "description": "Ультраранний, круглый, красный."},
    {"crop_name": "Редис", "variety": "Французский завтрак", "watering_interval_days": 2, "days_to_harvest": 25, "emoji": "🔴",
     "description": "Удлинённый, красно-белый, нежный."},

    # Клубника
    {"crop_name": "Клубника", "variety": "Виктория", "watering_interval_days": 3, "days_to_harvest": 90, "emoji": "🍓",
     "description": "Крупноплодная, ароматная, среднеспелая."},
    {"crop_name": "Клубника", "variety": "Елизавета II", "watering_interval_days": 3, "days_to_harvest": 60, "emoji": "🍓",
     "description": "Ремонтантная, плодоносит до осени."},

    # Арбуз и дыня
    {"crop_name": "Арбуз", "variety": "Огонёк", "watering_interval_days": 5, "days_to_harvest": 80, "emoji": "🍉",
     "description": "Скороспелый, небольшой, сладкий."},
    {"crop_name": "Дыня", "variety": "Колхозница", "watering_interval_days": 5, "days_to_harvest": 95, "emoji": "🍈",
     "description": "Среднеспелая, округлая, ароматная."},

    # Подсолнечник
    {"crop_name": "Подсолнечник", "variety": "Лакомка", "watering_interval_days": 7, "days_to_harvest": 110, "emoji": "🌻",
     "description": "Крупноплодный, для семечек."},
    # Кукуруза
    {"crop_name": "Кукуруза", "variety": "Спирит F1", "watering_interval_days": 5, "days_to_harvest": 70, "emoji": "🌽",
     "description": "Суперсладкая, раннеспелая, для варки."},
]
