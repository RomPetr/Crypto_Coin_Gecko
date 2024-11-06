"""
Чтобы добавить отображение изображения выбранной криптовалюты, необходимо модифицировать код так,
чтобы программа получала ссылку на изображение для каждой криптовалюты. При изменении выбора
криптовалюты программа будет загружать и отображать соответствующее изображение с помощью библиотеки PIL.
"""

from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import requests
from PIL import Image, ImageTk
from io import BytesIO


# Функция для получения списка криптовалют с сортировкой по рыночной капитализации
def get_crypto_market_data():
    try:
        response = requests.get("https://api.coingecko.com/api/v3/coins/markets", params={
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 100,  # Получаем сразу 100 криптовалют
            "page": 1
        })
        response.raise_for_status()
        return response.json()
    except Exception as e:
        mb.showerror("Ошибка", f"Код ошибки: {e}")


# Функция для загрузки и отображения изображения криптовалюты
def update_crypto_image(image_url):
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        image_data = response.content
        image = Image.open(BytesIO(image_data))
        image = image.resize((200, 200), Image.Resampling.LANCZOS)  # Изменяем размер изображения
        photo = ImageTk.PhotoImage(image)
        image_label.config(image=photo)  # вставляем картинку в image_label
        image_label.image = photo  # Сохраняем ссылку на изображение для предотвращения его удаления
    except Exception as e:
        mb.showerror("Ошибка", f"Код ошибки: {e}")


# Функция для получения курса криптовалюты
def get_crypto_price(crypto_id):
    try:
        response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=usd")
        response.raise_for_status()
        price = response.json()
        return price[crypto_id]["usd"]
    except Exception as e:
        mb.showerror("Ошибка", f"Код ошибки: {e}")


# Функция для получения и отображения курса, рыночной капитализации и изображения выбранной криптовалюты
def update_crypto_price_and_market_cap(event=None):
    selected_index = cr_combo.current()
    if selected_index != -1:
        crypto_id = cr_combo_ids[selected_index]  # забираем id крипты из ранее созданного списка идентификаторов
        market_cap = cr_combo_market_caps[selected_index]  # забираем из ранее созданного списка рыночных капитализаций
        image_url = cr_combo_images[selected_index]  # забираем URl картинки выбранной криптовалюты
        price = get_crypto_price(crypto_id)  # получаем стоимость криптовалюты к доллару

        # заполняем информацией соответствующие метки главного окна
        price_label.config(text=f"Курс: ${price:.4f}")
        market_cap_label.config(text=f"Рыночная капитализация: ${market_cap:,.0f}")
        update_crypto_image(image_url)  # через функцию обновляем картинку выбранной криптовалюты


# Функция для обновления списка криптовалют по выбранной группе
def update_crypto_list(event):
    group = int(gr_combo.get()) - 1  # вычисление индекса выбранной группы из 10 криптовалют
    start = group * 10  # начальный индекс для группы криптовалют
    end = start + 10  # конечный индекс для группы криптовалют
    # создаем список очередных 10-ти имен (names:) выбранной группы криптовалют
    # генератор списка создаёт новый список, состоящий только из названий криптовалют из выбранной группы
    crypto_names = [crypto["name"] for crypto in coins[start:end]]
    # создаем список очередных 10-ти идентификаторов (id:) выбранной группы криптовалют
    crypto_ids = [crypto["id"] for crypto in coins[start:end]]
    # создаем список очередных 10-ти рыночных капитализаций выбранной группы криптовалют
    crypto_market_caps = [crypto["market_cap"] for crypto in coins[start:end]]
    # при загрузке данных о криптовалютах теперь мы также сохраняем URL-адреса изображений каждой из них
    crypto_images = [crypto["image"] for crypto in coins[start:end]]

    # Обновляем выпадающий список с криптовалютами и сохраняем идентификаторы
    cr_combo["values"] = crypto_names  # заполняет Combobox с криптовалютами очередными 10-ю наименованиями

    # устанавливает текущий выбранный элемент выпадающего списка crypto_combobox на первый элемент из
    # обновлённого списка криптовалют
    cr_combo.current(0)

    cr_combo_ids.clear()  # очищаем список идентификаторов от старых значений
    cr_combo_ids.extend(crypto_ids)  # вставляем новые идентификаторы

    cr_combo_market_caps.clear()  # очищаем список капитализаций от старых значений
    cr_combo_market_caps.extend(crypto_market_caps)  # вставляем новые капитализации выбранной группы

    cr_combo_images.clear()  # очищаем список URL изображений
    cr_combo_images.extend(crypto_images)  # вставляем новые URL изображений очередных 10-ти криптовалют

    # Обновляем цену, рыночную капитализацию и изображение для первой криптовалюты в группе
    update_crypto_price_and_market_cap()


# Создаем интерфейс
window = Tk()
window.title("Курс криптовалют")
window.geometry("350x420")

# Получаем список криптовалют
coins = get_crypto_market_data()
# print(len(coins)) # Сколько всего криптовалют публикуется на CionGecko.com (15135 на 05.11.2024)
cr_combo_ids = []  # Создаем пустой список id криптовалют
cr_combo_market_caps = []  # Создаем пустой список рыночных капитализаций
cr_combo_images = []  # Создаем пустой список URL изображений криптовалют

# Выпадающий список для выбора группы
gr_label = Label(text=f"Выберите группу\n(в каждой группе по 10 криптовалют)")
gr_label.pack(pady=5)
gr_combo = ttk.Combobox(values=[str(i) for i in range(1, 11)], state="readonly")
gr_combo.current(0)  # устанавливает начальное значение для выпадающего списка ('1')
gr_combo.pack(pady=5)
gr_combo.bind("<<ComboboxSelected>>", update_crypto_list)

# Выпадающий список для выбора криптовалюты
cr_label = Label(text="Выберите криптовалюту:")
cr_label.pack(pady=5)
cr_combo = ttk.Combobox(state="readonly")
cr_combo.pack(pady=5)
cr_combo.bind("<<ComboboxSelected>>", update_crypto_price_and_market_cap)

# Метка для отображения курса
price_label = Label(text="Курс: ")
price_label.pack(pady=5)

# Метка для отображения рыночной капитализации
market_cap_label = Label(text="Рыночная капитализация: ")
market_cap_label.pack(pady=5)

# Метка для отображения изображения криптовалюты
image_label = Label()
image_label.pack(pady=10)


# Загрузка первой группы криптовалют
update_crypto_list(None)

# Запуск интерфейса
window.mainloop()

"""
Пояснения к обновленному коду:
1. get_crypto_market_data: эта функция запрашивает сразу 100 криптовалют, отсортированных по рыночной капитализации, 
   что упрощает деление на группы.
2. update_crypto_image: функция загружает изображение по URL и преобразует его для отображения в Tkinter с 
   использованием библиотеки PIL обновляя метку image_label
3. get_crypto_price: через GET запрос к API сайта CoinGecko.com получает цену нужной криптовалюты
4. update_crypto_list: обновляет второй Combobox с криптовалютами в выбранной группе, а также сохраняет идентификаторы,
   значения рыночной капитализации и адреса картинок.
5. update_crypto_price_and_market_cap: показывает курс и рыночную капитализацию выбранной криптовалюты, обновляя метки 
   price_label и market_cap_label. Эта функция так же получает URl картинки выбранной криптовалюты и передает этот 
   URL как аргумент функции update_crypto_image
Программа теперь правильно разделяет криптовалюты на группы по 10 и отображает их рыночную капитализацию.
"""