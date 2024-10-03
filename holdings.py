import polars as pl

def read_holdings(filename: str):
    old_cols = ("Instrumentum", "Készletnap", "Darab", "Beker. ár",
            "Bek. árf. érték", "Bek. költség", "Piaci ár", "Deviza",
            "Deviza-árfolyam (HUF)")
    new_cols = ("Instrument", "Date bought", "Number", "Unit cost",
         "Total cost", "Fee", "Current price", "Currency",
         "Current currency rate")
    
    def numeric(name: str):
        return pl.col(name).str.replace(" ", "").cast(pl.Float64)
    
    return (
        pl
        .read_csv(filename, columns=old_cols)
        .drop_nulls()
        .rename(dict(zip(old_cols, new_cols)))
        .select(*new_cols)
        .with_columns(numeric("Unit cost"), numeric("Total cost"), numeric("Fee"), numeric("Current price"))
        .with_columns(pl.col("Date bought").str.to_date(format="%Y.%m.%d"))
    )
