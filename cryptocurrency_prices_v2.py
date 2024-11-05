"""
Чтобы изменить программу для отображения топ-50 криптовалют по рыночной капитализации и выводить рыночную капитализацию,
 мы будем использовать дополнительный запрос к API CoinGecko для получения информации о рыночной капитализации.
 Эта версия программы организует криптовалюты в группы по рыночной капитализации и выводит её значение в отдельной метке Label.
"""
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import requests
import pprint


# Функция для получения списка криптовалют с сортировкой по рыночной капитализации
def get_crypto_market_data():
    try:
        response = requests.get("https://api.coingecko.com/api/v3/coins/markets", params={
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 1000,  # Получаем сразу 1000 криптовалют
            "page": 1
        })
        response.raise_for_status()
        return response.json()
    except Exception as e:
        mb.showerror("Ошибка", f"Код ошибки: {e}")


# Функция для получения списка криптовалют
def get_crypto_list():
    try:
        response = requests.get("https://api.coingecko.com/api/v3/coins/list")
        response.raise_for_status()
        get_coins = response.json()
        return get_coins
    except Exception as e:
        mb.showerror("Ошибка", f"Код ошибки: {e}")


# Функция для получения курса криптовалюты
def get_crypto_price(crypto_id):
    try:
        response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=usd")
        response.raise_for_status()
        price = response.json()
        # mb.showinfo("Цена", f"{price}")
        return price[crypto_id]["usd"]
    except Exception as e:
        mb.showerror("Ошибка", f"Код ошибки: {e}")


# Обновляем курс выбранной криптовалюты
def update_crypto_price_and_market_cap(event=None):
    selected_index = cr_combo.current()
    if selected_index != -1:
        crypto_id = cr_combo_idx[selected_index]
        price = get_crypto_price(crypto_id)
        price_label.config(text=f"Курс: ${price:.4f}")

# Обновляем список криптовалют по выбранной группе
def update_crypto_list(event):
    group = int(gr_combo.get()) - 1 # вычисление индекса выбранной группы из 50 криптовалют
    start = group * 50 # начальный индекс для группы криптовалют
    end = start + 50 # конечный индекс для группы криптовалют
    # создаем список очередных 50-ти имен (names:) выбранной группы криптовалют
    crypto_names = [crypto["name"] for crypto in coins[start:end]] # генератор списка создаёт новый список, состоящий только из названий криптовалют из выбранной группы
    # создаем список очередных 50-ти идентификаторов (id:) выбранной группы криптовалют
    crypto_ids = [crypto["id"] for crypto in coins[start:end]]
    # создаем список очередных 50-ти рыночных капитализаций выбранной группы криптовалют
    crypto_market_caps = [crypto["market_cap"] for crypto in coins[start:end]]

    # Обновляем выпадающий список с криптовалютами и сохраняем идентификаторы
    cr_combo["values"] = crypto_names # заполняет Combobox с криптовалютами очередными 50-ю наименованиями
    cr_combo.current(0) # устанавливает текущий выбранный элемент Combobox на первый элемент списка crypto_names, то есть с индексом 0

    cr_combo_idx.clear() # очищаем список идентификаторов от старых значений
    cr_combo_idx.extend(crypto_ids) # вставляем новые идентификаторы

    cr_combo_market_caps.clear() # очищаем список капитализаций от старых значений
    cr_combo_market_caps.extend(crypto_market_caps) # вставляем новые капитализации выбранной группы

    # Обновляем цену и рыночную капитализацию для первой криптовалюты в группе
    update_crypto_price_and_market_cap()


# Создаем интерфейс
window = Tk()
window.title("Курс криптовалют")
window.geometry("300x200")

# Получаем список криптовалют
coins = get_crypto_market_data()
# print(len(coins)) # Сколько всего криптовалют публикуется на CionGecko.com (15135 на 05.11.2024)
cr_combo_idx = [] # Создаем пустой список индексов
cr_combo_market_caps = [] # Создаем пустой список рыночных капитализаций

# p1 = pprint.PrettyPrinter(indent=4)
# p1.pprint(coins) # выведет в консоль список всех криптовалют в виде списка словарей

# Выпадающий список для выбора группы
gr_label = Label(text=f"Выберите группу\n(в каждой группе по 50 криптовалют")
gr_label.pack(pady=5)
gr_combo = ttk.Combobox(values=[str(i) for i in range(1,21)], state="readonly")
gr_combo.current(0) # устанавливает начальное значение для выпадающего списка ('1')
gr_combo.pack(pady=5)
gr_combo.bind("<<ComboboxSelected>>", update_crypto_list)

# Выпадающий список для выбора криптовалюты
cr_label = Label(text="Выберите криптовалюту:")
cr_label.pack(pady=5)
cr_combo = ttk.Combobox(state="readonly")
cr_combo.pack(pady=5)
cr_combo.bind("<<ComboboxSelected>>", update_crypto_price)

# Метка для отображения курса
price_label = Label(text="Курс: ")
price_label.pack(pady=5)

# Метка для отображения рыночной капитализации
market_cap_label = Label(text="Рыночная капитализация: ")
market_cap_label.pack(pady=5)

# Загрузка первой группы криптовалют
update_crypto_list(None)

# Запуск интерфейса
window.mainloop()