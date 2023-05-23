from API import api_exchenge_key
import requests
import json
import re

class APIException(Exception):
    pass


class ValuesCurrency:

    @staticmethod
    def change(base, quote, amount, api_exchenge_key):
        base = base.upper()
        quote = quote.upper()

        if base == quote:
            raise ValueError(f"Невозможно перевести {base} в {quote}")

        if re.search(r"[^a-zA-Z]", base) or re.search(r"[^a-zA-Z]", quote):
            raise SyntaxError('Для получения данных валютных пар используйте латинскую раскладку')

        if base not in list(ValuesCurrency.all_currency(api_exchenge_key)):
            raise KeyError(f"Валюта {base} отсутствует в списке")

        if quote not in list(ValuesCurrency.all_currency(api_exchenge_key)):
            raise KeyError(f'Валюта {quote} отсутствует в списке')

        meaning_currency = requests.get(f"https://v6.exchangerate-api.com/v6/{api_exchenge_key}/latest/{base}")
        dict_currency = json.loads(meaning_currency.content)
        dict_currency = dict_currency['conversion_rates']
        get_amount = dict_currency[quote] * float(amount)
        return f"В результате обмена {base} на {quote} в количестве {amount} вы получите {'{0:.3f}'.format(get_amount)}"

    @staticmethod
    def all_currency(api_exchenge_key):
        meaning_currency = requests.get(f"https://v6.exchangerate-api.com/v6/{api_exchenge_key}/latest/USD")
        dict_currency = json.loads(meaning_currency.content)
        currency = []
        for i in dict_currency['conversion_rates']:
            currency.append(i)
        return currency