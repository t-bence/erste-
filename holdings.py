from datetime import date

def read_holdings(filename: str):
    import polars as pl
    holdings = (
        pl
        .read_csv(filename)[
            ["Instrumentum", "Készletnap", "Darab", "Beker. ár",
            "Bek. árf. érték", "Bek. költség", "Piaci ár", "Deviza",
            "Deviza-árfolyam (HUF)"]]
        .drop_nulls()
    )

    holdings.columns = ("Instrument", "Date bought", "Number", "Unit cost",
         "Total cost", "Fee", "Current price", "Currency",
         "Current currency rate")

    holdings = (
        holdings
        .with_columns(pl.col("Unit cost").str.replace(" ", "").cast(pl.Float64))
        .with_columns(pl.col("Total cost").str.replace(" ", "").cast(pl.Float64))
        .with_columns(pl.col("Fee").str.replace(" ", "").cast(pl.Float64))
        .with_columns(pl.col("Current price").str.replace(" ", "").cast(pl.Float64))
        .with_columns(pl.col("Date bought").str.to_date(format="%Y.%m.%d"))
    )

    return holdings
