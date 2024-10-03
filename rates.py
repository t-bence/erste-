def read_rates(filename: str):
    import lxml.html
    doc = lxml.html.parse("EURHUF.html")
    from datetime import date

    dates = doc.xpath("//tr/td[1]/text()")
    rates = doc.xpath("//tr/td[2]/text()")

    def parse_date(input: str) -> date:
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

        items = input.strip().replace(".", "").replace(",", "").split(" ")
        year = int(items[0])
        month = months_hungarian[items[1]]
        day = int(items[2])
        return date(year, month, day)
    
    def parse_rate(input: str) -> float:
        return float(input.strip().replace(",", "."))
    
    return [(parse_date(d), parse_rate(r)) for (d, r) in zip(dates, rates)]
