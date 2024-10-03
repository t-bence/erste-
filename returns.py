from typing import Any
import polars as pl
from rates import ExchangeRate

def compute_returns(holdings: pl.DataFrame, rates: ExchangeRate):
    
    def past_rate(row: tuple[Any]) -> float:
        return 350.0
        """
        if pl.col("Currency") == "HUF":
            return 1.0
        elif pl.col("Currency") == "EUR":
            return rates.get_rate(pl.col("Date bought"))
        else:
            raise ValueError(f"Not supported currency: {pl.col("Currency")}")
        """
                
    holdings = (
        holdings
        .with_columns(
            pl
            .when(pl.col("Currency") == "HUF").then(pl.lit(1.0))
            .when(pl.col("Currency") == "EUR").then(
                pl.col("Date bought").map_elements(rates.rates.get)
            )
            .otherwise(pl.lit(None))
            .alias("Purchase currency rate")
        )
        .with_columns(
            (pl.col("Unit cost") * (pl.col("Current currency rate") - pl.col("Purchase currency rate")))
            .alias("EURHUF gain")
        )
        .with_columns(
            ((pl.col("Current price") - pl.col("Unit cost")) * pl.col("Current currency rate"))
            .alias("Underlying gain")
        )
    )

    pl.Config.set_tbl_rows(100)
    
    print(holdings)