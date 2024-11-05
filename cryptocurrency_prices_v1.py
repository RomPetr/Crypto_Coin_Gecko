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
        mb.showinfo("Цена", f"{price}")
        return price[crypto_id]["usd"]
    except Exception as e:
        mb.showerror("Ошибка", f"Код ошибки: {e}")


# Обновляем курс выбранной криптовалюты
def update_crypto_price(event=None):
    selected_index = cr_combo.current()
    if selected_index != -1:
        crypto_id = cr_combo_idx[selected_index]
        price = get_crypto_price(crypto_id)
        price_label.config(text=f"Курс: ${price:.2f}")


# Создаем интерфейс
window = Tk()
window.title("Курс криптовалют")
window.geometry("300x200")

# Получаем список криптовалют
coins = get_crypto_list()
print(len(coins)) # Сколько всего криптовалют публикуется на CionGecko.com (15135 на 05.11.2024)
cr_combo_idx = [] # Создаем пустой список индексов

# p1 = pprint.PrettyPrinter(indent=4)
# p1.pprint(coins)

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

c_price = get_crypto_price('bitcoin')
mb.showinfo("Крипта", c_price)

# Запуск интерфейса
window.mainloop()