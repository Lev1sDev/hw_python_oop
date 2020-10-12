import datetime as dt
DATE_FORMAT = '%d.%m.%Y'


class Calculator:

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        return self.records.append(record)

    def get_today_stats(self):
        today_date = dt.date.today()
        today_sum = sum(
            record.amount for record in self.records
            if record.date == today_date
        )
        return today_sum

    def get_week_stats(self):
        today_date = dt.date.today()
        seven_days = dt.timedelta(days=7)
        week_ago = today_date - seven_days
        week_sum = sum(
            day.amount for day in self.records
            if week_ago < day.date <= today_date
        )
        return week_sum


class Record:

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, DATE_FORMAT).date()

    def show(self):
        print(f"{self.amount}, {self.comment}, {self.date}.")


class CaloriesCalculator(Calculator):
    A = (
        'Сегодня можно съесть что-нибудь ещё,'
        ' но с общей калорийностью не более {val} кКал'
    )
    B = ('Хватит есть!')

    def get_calories_remained(self):
        remained = self.limit - self.get_today_stats()
        if remained > 0:
            return self.A.format(val=remained)
        return self.B


class CashCalculator(Calculator):
    USD_RATE = 60.0
    EURO_RATE = 70.0
    CURRENCIES = {
        "rub": (1, "руб"),
        "usd": (USD_RATE, "USD"),
        "eur": (EURO_RATE, "Euro")
    }
    C = ('Валюта "{val}" не поддерживается')
    D = ('Денег нет, держись')
    E = ('На сегодня осталось {val1} {val2}')
    F = ('Денег нет, держись: твой долг - {val1} {val2}')

    def get_today_cash_remained(self, currency):
        if currency not in self.CURRENCIES:
            raise ValueError(self.C.format(val=currency))
        currencies_value = self.CURRENCIES[currency][1]
        today_balance = self.limit - self.get_today_stats()
        if today_balance == 0:
            return self.D
        currency_balance = round(
            today_balance / self.CURRENCIES[currency][0], 2
        )
        if today_balance > 0:
            return self.E.format(
                val1=currency_balance, val2=currencies_value
            )
        currency_credit = abs(currency_balance)
        return self.F.format(
            val1=currency_credit, val2=currencies_value
        )


if __name__ == "__main__":

    calories_calculator = CaloriesCalculator(2000)
    r4 = Record(amount=1200, comment="Кусок тортика. И ещё один.")
    r5 = Record(amount=84, comment="Йогурт")
    r6 = Record(amount=1140, comment="Баночка чипсов.", date="08.10.2020")

    calories_calculator.add_record(r4)
    calories_calculator.add_record(r5)
    calories_calculator.add_record(r6)

    print(calories_calculator.get_today_stats())

    print(calories_calculator.get_calories_remained())

    cach_calculator = CashCalculator(5000)

    r1 = Record(amount=145, comment="Безудержный шопинг", date="08.10.2020")
    r2 = Record(amount=5600, comment="Наполнение потребительской корзины")
    r3 = Record(amount=691, comment="Катание на такси", date="07.10.2020")

    cach_calculator.add_record(r1)
    cach_calculator.add_record(r2)
    cach_calculator.add_record(r3)

    print(cach_calculator.get_week_stats())

    print(cach_calculator.get_today_cash_remained("eur"))
