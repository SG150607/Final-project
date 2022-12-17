import sys, csv, sqlite3, datetime, random  # поместить потом все названия библиотек в файл
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QTextEdit, QComboBox, QListWidget


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # настраиваем экран
        self.setGeometry(200, 200, 801, 534)
        self.setWindowTitle('Гороскоп')

        # Картинка на заднем плане
        self.pixmap = QPixmap('Images/bg.jpg')
        self.image = QLabel(self)
        self.image.setScaledContents(True)
        self.image.setGeometry(0, 0, 801, 534)
        self.image.setPixmap(self.pixmap)

        # label'ы
        self.Tip_for_today_label = QLabel(self)
        self.Tip_for_today_label.setText("Ну чтож, усторим тебе гадание!")
        self.Tip_for_today_label.setStyleSheet("font-size: 26px;"
                                               "font-weight: bold;")
        self.Tip_for_today_label.setGeometry(220, 10, 411, 31)

        self.choose_categories_label = QLabel(self)
        self.choose_categories_label.setText("Выбери свой знак зодиака")
        self.choose_categories_label.setStyleSheet("font-size: 18px;")
        self.choose_categories_label.setGeometry(300, 56, 231, 20)

        # QPushButton'ы, при нажатии на которые сгенерируется ответ
        self.get_answer_btn = QPushButton('Овен', self)
        self.get_answer_btn.setGeometry(10, 110, 111, 61)
        self.get_answer_btn.clicked.connect(self.get_answer)

        self.get_answer_btn = QPushButton('Телец', self)
        self.get_answer_btn.setGeometry(140, 110, 111, 61)
        self.get_answer_btn.clicked.connect(self.get_answer)

        self.get_answer_btn = QPushButton('Близнецы', self)
        self.get_answer_btn.setGeometry(270, 110, 111, 61)
        self.get_answer_btn.clicked.connect(self.get_answer)

        self.get_answer_btn = QPushButton('Рак', self)
        self.get_answer_btn.setGeometry(400, 110, 111, 61)
        self.get_answer_btn.clicked.connect(self.get_answer)

        self.get_answer_btn = QPushButton('Лев', self)
        self.get_answer_btn.setGeometry(530, 110, 111, 61)
        self.get_answer_btn.clicked.connect(self.get_answer)

        self.get_answer_btn = QPushButton('Дева', self)
        self.get_answer_btn.setGeometry(660, 110, 111, 61)
        self.get_answer_btn.clicked.connect(self.get_answer)

        self.get_answer_btn = QPushButton('Весы', self)
        self.get_answer_btn.setGeometry(10, 190, 111, 61)
        self.get_answer_btn.clicked.connect(self.get_answer)

        self.get_answer_btn = QPushButton('Скорпион', self)
        self.get_answer_btn.setGeometry(140, 190, 111, 61)
        self.get_answer_btn.clicked.connect(self.get_answer)

        self.get_answer_btn = QPushButton('Стрелец', self)
        self.get_answer_btn.setGeometry(270, 190, 111, 61)
        self.get_answer_btn.clicked.connect(self.get_answer)

        self.get_answer_btn = QPushButton('Козерог', self)
        self.get_answer_btn.setGeometry(400, 190, 111, 61)
        self.get_answer_btn.clicked.connect(self.get_answer)

        self.get_answer_btn = QPushButton('Водолей', self)
        self.get_answer_btn.setGeometry(530, 190, 111, 61)
        self.get_answer_btn.clicked.connect(self.get_answer)

        self.get_answer_btn = QPushButton('Рыбы', self)
        self.get_answer_btn.setGeometry(660, 190, 111, 61)
        self.get_answer_btn.clicked.connect(self.get_answer)

        # список полученных советов
        self.result = QTextEdit(self)
        self.result.setGeometry(20, 280, 751, 201)
        self.result.hide()  # прячем, так как пользователь не просит совета во время запуска программы

        # сообщение о том, что уже получали предсказание
        self.wait_label = QLabel(self)
        self.wait_label.setText('Вы уже получили свое предсказание. Дождитесь завтра')
        self.wait_label.setStyleSheet("color: white;")
        self.wait_label.setGeometry(20, 490, 361, 16)
        self.wait_label.hide()  # прячем

    def get_answer(self):  # получаем предсказание, записанное в поле

        attempt = False  # можно ли получить сегодня предсказание

        with open('Horoscope_list.txt', "rt",
                  encoding="utf8") as records:  # проверка на наличие попыток для получение предсказания
            for day_tip in records.readlines():
                if day_tip.split(";")[0] == str(
                        datetime.datetime.now().date()):  # проверяем, получали ли мы уже предсказание
                    self.wait_label.show()  # показываем сообщение о том, что сегодня уже получили предсказание
                    break
            else:
                attempt = True  # можно получить предсказание
                self.wait_label.hide()  # скрываем надпись, потому что уже не нужна

        if attempt:
            # Заготовки предложений
            first = ["Сегодня — идеальный день для новых начинаний.",
                     "Оптимальный день для того, чтобы решиться на смелый поступок!",
                     "Будьте осторожны, сегодня звёзды могут повлиять на ваше финансовое состояние.",
                     "Лучшее время для того, чтобы начать новые отношения или разобраться со старыми.",
                     "Плодотворный день для того, чтобы разобраться с накопившимися делами."]

            second = ["Но помните, что даже в этом случае нужно не забывать про",
                      "Если поедете за город, заранее подумайте про",
                      "Те, кто сегодня нацелен выполнить множество дел, должны помнить про",
                      "Если у вас упадок сил, обратите внимание на",
                      "Помните, что мысли материальны, а значит вам в течение дня нужно постоянно думать про"]

            second_add = ["отношения с друзьями и близкими.",
                          "работу и деловые вопросы, которые могут так некстати помешать планам.",
                          "себя и своё здоровье, иначе к вечеру возможен полный раздрай.",
                          "бытовые вопросы — особенно те, которые вы не доделали вчера.",
                          "отдых, чтобы не превратить себя в загнанную лошадь в конце месяца."]

            third = ["Злые языки могут говорить вам обратное, но сегодня их слушать не нужно.",
                     "Знайте, что успех благоволит только настойчивым, поэтому посвятите этот день воспитанию духа.",
                     "Даже если вы не сможете уменьшить влияние ретроградного Меркурия, то хотя бы доведите дела до конца.",
                     "Не нужно бояться одиноких встреч — сегодня то самое время, когда они значат многое.",
                     "Если встретите незнакомца на пути — проявите участие, и тогда эта встреча посулит вам приятные хлопоты."]

            horoscope = random.choice(first) + random.choice(second) + random.choice(second_add) + random.choice(third)
            self.result.setText(horoscope)  # задаем текст
            self.result.show()
            with open('Horoscope_list.txt', "wt", encoding="utf8") as records:  # Записываем в файл
                records.write(f"{datetime.datetime.now().date()};{horoscope}")

        # Выводим предсказания
        self.result.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
