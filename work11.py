from abc import ABC, abstractmethod

class SmartPhone:
    def __init__(self, name: str, battery: int, password: str):
        self.name = name
        self._battery = 0
        self.battery = battery
        self.__password = password

    @property
    def battery(self):
        return self._battery

    @battery.setter
    def battery(self, value):
        if 0<= value <= 100:
            self._battery = value
        else:
            print(f'Ошибка: Нельзя установить заряд {value}%. Значение должно быть в диапазоне от 0 до 100.')

class Notifire(ABC):
    @abstractmethod
    def send(self, message: str):
        pass

class SMSNotifire(Notifire):
    def send(self, message: str):
        print(f'[SMS] Отправлено сообщение: {message}')

class TelegramNotifire(Notifire):
    def send(self, message: str):
        print(f'[Telegram] Отправлено сообщение: {message}')


if __name__ == '__main__':
    print('=== 1. Проверка работы SmartPhone===')
    phone = SmartPhone(name ='iPhone 13', battery =50, password= '12345')

    print(f'Название телефона: {phone.name}')
    print(f'Заряд батареи: {phone.battery}%')
    phone.battery = 150
    phone.battery -20
    print(f'Заряд после ошибечных попыток: {phone.battery}%')
    print('\n--- Проверка работы инкапсуляции пароля ---')
    try:
        print(phone.__password)
    except AttributeError:
        print('Ошибка: Невозможно получить доступ к защищенному атрибуту.')
    print(f'Доступ к приватной переменной через искажение имени (Name Mangling): {phone._SmartPhone__password}')
    print('\n=== 2. Проверка работы Notifire ===')
    sms = SMSNotifire()
    tg = TelegramNotifire()
    sms.send('Привет, я отправляю тебе SMS сообщение!')
    tg.send('Привет, я отправляю тебе Telegram сообщение!')