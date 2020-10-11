import datetime as dt
date_format = '%d.%m.%Y'


class Calculator:

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)
        print("Запись успешно добавлена")

    def get_today_stats(self):
        today_stats = 0
        today_date = dt.datetime.now().date()
        for record in self.records:
            if record.date == today_date:
                today_stats += record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today_date = dt.datetime.now().date()
        seven_days = dt.timedelta(days=7)
        week_ago = today_date - seven_days
        for day in self.records:
            if week_ago < day.date <= today_date:
                week_stats += day.amount
        return week_stats


class Record:

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, date_format).date()

    def show(self):
        print(f"{self.amount}, {self.comment}, {self.date}.")


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        remained = self.limit - self.get_today_stats()
        if remained > 0:
            return (
                    f"Сегодня можно съесть что-нибудь ещё,"
                    f" но с общей калорийностью не более {remained} кКал"
                   )
        return ("Хватит есть!")


class CashCalculator(Calculator):
    USD_RATE = 76.80
    EURO_RATE = 90.50

    def get_today_cash_remained(self, currency):
        currency_dict = {
                         "rub": (1, "руб"),
                         "usd": (self.USD_RATE, "USD"),
                         "eur": (self.EURO_RATE, "Euro")
                        }
        if currency not in currency_dict.keys():
            return ("Валюта не поддерживается")
        today_balance = self.limit - self.get_today_stats()
        if today_balance == 0:
            return ("Денег нет, держись")
        currency_balance = round(today_balance / currency_dict[currency][0], 2)
        if today_balance > 0:
            return (
                    f"На сегодня осталось {currency_balance}"
                    f" {currency_dict[currency][1]}"
                   )
        currency_credit = abs(currency_balance)
        return (
                f"Денег нет, держись: твой долг - {currency_credit}"
                f" {currency_dict[currency][1]}"
               )


if __name__ == "__main__":

    calories_calculator = CaloriesCalculator(2000)
    r4 = Record(amount=1186, comment="Кусок тортика. И ещё один.")
    r5 = Record(amount=84, comment="Йогурт")
    r6 = Record(amount=1140, comment="Баночка чипсов.", date="08.10.2020")

    calories_calculator.add_record(r4)
    calories_calculator.add_record(r5)
    calories_calculator.add_record(r6)

    print(calories_calculator.get_calories_remained())

    cach_calculator = CashCalculator(5000)

    r1 = Record(amount=145, comment="Безудержный шопинг", date="08.10.2020")
    r2 = Record(amount=4000, comment="Наполнение потребительской корзины")
    r3 = Record(amount=691, comment="Катание на такси", date="07.10.2020")

    cach_calculator.add_record(r1)
    cach_calculator.add_record(r2)
    cach_calculator.add_record(r3)

    print(cach_calculator.get_today_stats())

    print(cach_calculator.get_today_cash_remained("eur"))
