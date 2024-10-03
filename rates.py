from datetime import date
import polars as pl
import lxml.html as lh

def read_rates(filename: str) -> pl.DataFrame:
    doc = lh.parse(filename)

    dates = doc.xpath("//tr/td[1]/text()")
    rates = doc.xpath("//tr/td[2]/text()")

    months_hungarian = {
        "január": 1,
        "február": 2,
        "március": 3,
        "április": 4,
        "május": 5,
        "június": 6,
        "július": 7,
        "augusztus": 8,
        "szeptember": 9,
        "október": 10,
        "november": 11,
        "december": 12
    }

    return (
        pl
        .DataFrame(zip(dates, rates), schema=("Date", "EUR rate"))
        .with_columns(pl.col("EUR rate").str.replace(",", ".").cast(pl.Float64))
        .with_columns(pl.col("Date").str.replace_many([".", ","], "").str.split(" "))
        .with_columns(pl.col("Date").list.get(1).replace(months_hungarian).alias("month"))
        .with_columns(pl.date(pl.col("Date").list.get(0), "month", pl.col("Date").list.get(2)).alias("Date bought"))
        .select("Date bought", "EUR rate")
    )
