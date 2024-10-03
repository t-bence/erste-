from datetime import date

def read_holdings(filename: str):
    import pandas as pd
    holdings = (
        pd
        .read_csv(filename)[
            ["Instrumentum", "Készletnap", "Darab", "Beker. ár",
            "Bek. árf. érték", "Bek. költség", "Piaci ár", "Deviza",
            "Deviza-árfolyam (HUF)"]]
        .dropna()
    )

    holdings.columns = ("Instrument", "Date bought", "Number", "Unit cost",
         "Total cost", "Fee", "Current price", "Currency",
         "Current currency rate")
    
    def text_to_date(input: str) -> date:
        pieces = [int(x) for x in input.strip().split(".")]
        return date(*pieces)
    
    holdings["Date bought"] = holdings["Date bought"].apply(text_to_date)

    holdings["Unit cost"] = pd.to_numeric(holdings["Unit cost"].str.replace(" ", ""))
    holdings["Total cost"] = pd.to_numeric(holdings["Total cost"].str.replace(" ", ""))
    holdings["Fee"] = pd.to_numeric(holdings["Fee"].str.replace(" ", ""))
    holdings["Current price"] = pd.to_numeric(holdings["Current price"].str.replace(" ", ""))
    
    return holdings
