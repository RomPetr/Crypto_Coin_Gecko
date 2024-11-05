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
def update_crypto_price(event=None):
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
    crypto_names = [crypto["name"] for crypto in coins[start:end]] # генератор списка создаёт новый список, состоящий только из названий криптовалют из выбранной группы
    crypto_ids = [crypto["id"] for crypto in coins[start:end]]
    cr_combo["values"] = crypto_names
    cr_combo.current(0)
    cr_combo_idx.clear()
    cr_combo_idx.extend(crypto_ids)
    update_crypto_price()


# Создаем интерфейс
window = Tk()
window.title("Курс криптовалют")
window.geometry("300x200")

# Получаем список словарей криптовалют
coins = get_crypto_list() # ... , {'id': 'zerpaay', 'name': 'Zerpaay', 'symbol': 'zrpy'}, {'id': 'zesh', 'name': 'Zesh', 'symbol': 'zesh'}, ...
# print(len(coins)) # Сколько всего криптовалют публикуется на CionGecko.com (15135 на 05.11.2024)
cr_combo_idx = [] # Создаем пустой список индексов

# p1 = pprint.PrettyPrinter(indent=4)
# p1.pprint(coins) # выведет в консоль список всех криптовалют в виде списка словарей

# Выпадающий список для выбора группы
gr_label = Label(text=f"Выберите группу\n(в каждой группе по 50 криптовалют")
gr_label.pack(pady=5)
gr_combo = ttk.Combobox(values=[str(i) for i in range(1,21)])
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

# c_price = get_crypto_price('bitcoin')
# mb.showinfo("Крипта", c_price)

# Загрузка первой группы криптовалют
update_crypto_list(None)

# Запуск интерфейса
window.mainloop()