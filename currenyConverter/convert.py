import tkinter
from tkinter import *
from tkinter import messagebox
from forex_python.converter import CurrencyRates
from forex_python.converter import RatesNotAvailableError
import requests
import threading

currencies = ['USD', 'EUR', 'AED', 'GBP', 'AUD', 'JPY', 'CHF', 'ALL', 'RSD', 'RUB']


def show_currencies():
    def fetch_currencies():
        try:
            from_cur = from_currency.get()
            to_cur = to_currency.get()
            amount = float(amount_entry.get())

            cur_rates = CurrencyRates()
            rates = cur_rates.get_rate(from_currency, to_currency)

            converted_amount = amount * rates
            result_label.config(text=f'{amount} {from_currency} = {converted_amount:.2f} {to_currency}')

        except requests.exceptions.ConnectionError:
            result_label.config(text='Error: Network issue, unable to connect to currency rates service')
        except RatesNotAvailableError:
            result_label.config(text='Error: Currency rates not available for the selected currencies')
        except Exception as e:
            result_label.config(text=f'Error: {e}')

    threading.Thread(target=fetch_currencies).start()


def click_button():
    show_currencies()


root = Tk()
root.title("Currency Converter")
root.geometry("500x500")
root.config(background="#d3ffce")

from_currency = tkinter.StringVar(root)
from_currency.set('USD')
from_menu = tkinter.OptionMenu(root, from_currency, *currencies)
from_menu.pack(pady=5)

to_currency = tkinter.StringVar(root)
to_currency.set('EUR')
to_menu = tkinter.OptionMenu(root, to_currency, *currencies)
to_menu.pack(pady=10)

amount_label = tkinter.Label(root, text='Enter the amount= ')
amount_label.pack(pady=15)

amount_entry = tkinter.Entry(root)
amount_entry.pack(pady=16)

convert_button = tkinter.Button(root, text='Click to convert', command=click_button)
convert_button.pack(pady=20)

result_label = Label(root,width=25 ,text="")
result_label.pack(pady=22)

root.mainloop()
