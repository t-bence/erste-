import pandas as pd
from rates import ExchangeRate

def compute_returns(holdings: pd.DataFrame, rates: ExchangeRate):
    
    def past_rate(df: pd.DataFrame) -> float:
        if df["Currency"] == "HUF":
            return 1.0
        elif df["Currency"] == "EUR":
            return rates.get_rate(df["Date bought"])
        else:
            raise ValueError(f"Not supported currency: {df["Currency"]}")
    
    holdings["Purchase currency rate"] = holdings.apply(past_rate, axis=1)

    holdings["EURHUF gain"] = holdings[["Unit cost"]].multiply(holdings["Current currency rate"] - holdings["Purchase currency rate"], axis="index")
    holdings["Underlying gain"] = (holdings["Current price"] - holdings["Unit cost"]).multiply(holdings["Current currency rate"], axis="index")

    print(holdings)