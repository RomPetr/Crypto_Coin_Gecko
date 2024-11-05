import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import requests


# Функция для получения списка криптовалют
def get_crypto_list():
    try:
        response = requests.get("https://api.coingecko.com/api/v3/coins/list")
        response.raise_for_status()
        get_coins = response.json()
        return get_coins
    except Exception as e:
        mb.showerror("Ошибка", f"Код ошибки: {e}")


# Создаем интерфейс
window = Tk()
window.title("Курс криптовалют")
window.geometry("300x200")

# Получаем список криптовалют
coins = get_crypto_list()
print(len(coins)) # Сколько всего криптовалют публикуется на CionGecko.com

# Выпадающий список для выбора группы
gr_label = Label(text=f"Выберите группу\n(в каждой группе по 50 криптовалют")
gr_label.pack(pady=5)
gr_combo = ttk.Combobox(values=[str(i) for i in range(1,21)])
gr_combo.current(0) # устанавливает начальное значение для выпадающего списка ('1')
gr_combo.pack()

# Выпадающий список для выбора криптовалюты
cr_label = Label(text="Выберите криптовалюту:")
cr_label.pack()
cr_combo = ttk.Combobox(state="readonly")
cr_combo.pack()

# Метка для отображения курса
price_label = Label(text="Курс: ")
price_label.pack()

# Запуск интерфейса
window.mainloop()