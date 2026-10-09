from pydantic import BaseModel,Field
import json
import urllib.request


class CurrencyConverterSchema(BaseModel):
    amount : float = Field(description = "The numerical amount in foreign currency")
    from_currency : str = Field(description = " It is a three letter code representing a currency. eg(USD,EUR,GBP,JPY)")




def convert_currency_to_inr(amount:float,from_currency:str)->str:
    from_currency = from_currency.upper()
    if from_currency == "INR":
        return f"{amount} INR"

    try:
        url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency}&to=INR"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            print(data)


    except Exception as e:
        print(f"DEBUG - Actual error: {e}")
        return f"Error: Could not convert {from_currency} to INR."


print(convert_currency_to_inr(2,"JPY"))



