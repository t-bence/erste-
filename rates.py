from datetime import date
import polars as pl
import lxml.html as lh

def read_rates(filename: str) -> pl.DataFrame:
    doc = lh.parse(filename)

    dates = doc.xpath("//tr/td[1]/text()")
    rates = doc.xpath("//tr/td[2]/text()")

    months_hungarian = (
        "január",
        "február",
        "március",
        "április",
        "május",
        "június",
        "július",
        "augusztus",
        "szeptember",
        "október",
        "november",
        "december"
    )
    month_numbers = [f"{i}." for i in range(1, 13)]

    mapping = dict(zip(months_hungarian, month_numbers))

    return (
        pl
        .DataFrame(zip(dates, rates), schema=("Date", "EUR rate"))
        .with_columns(
            pl.col("EUR rate")
            .str.replace(",", ".")
            .cast(pl.Float64)
        )
        .with_columns(
            pl.col("Date")
            .str.replace_many(mapping)
            .str.split(",")
            .list.get(0)
        )
        .with_columns(
            pl.col("Date")
            .str.to_date(format="%Y. %-m. %-d.")
            .alias("Date bought")
        )
        .select("Date bought", "EUR rate")
    )
