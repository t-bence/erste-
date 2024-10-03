from datetime import date

class ExchangeRate:
    """Stores the exchange rates read from a file
    """
    rates: dict[date, float]
    start_date: date
    end_date: date

    def __init__(self, filename: str):
        import lxml.html
        doc = lxml.html.parse(filename)
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
        
        self.rates = dict((parse_date(d), parse_rate(r)) for (d, r) in zip(dates, rates))
        self.start_date = parse_date(dates[0])
        self.end_date = parse_date(dates[-1])

    def get_rate(self, day: date, iter:int=0) -> float:
        from datetime import timedelta
        if day < self.start_date:
            raise ValueError(f"{day} is earlier than start date")
        elif day > self.end_date:
            raise ValueError(f"{day} is later than end date")
        if iter > 3:
            raise ValueError(f"Iteration depth exceeded for {day}")
        if day in self.rates.keys():
            return self.rates[day]
        else:
            return self.get_rate(day - timedelta(days=1), iter+1)
