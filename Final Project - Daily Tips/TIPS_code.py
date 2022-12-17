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
        self.setWindowTitle('Совет на день')

        # Картинка на заднем плане
        self.pixmap = QPixmap('Images/bg.jpg')
        self.image = QLabel(self)
        self.image.setScaledContents(True)
        self.image.setGeometry(0, 0, 801, 534)
        self.image.setPixmap(self.pixmap)

        # label'ы
        self.Tip_for_today_label = QLabel(self)
        self.Tip_for_today_label.setText("~Какой же совет ты ждешь от меня сегодня?")
        self.Tip_for_today_label.setStyleSheet("color: white;"
                                               "font-size: 26px;"
                                               "font-weight: bold;")
        self.Tip_for_today_label.setGeometry(100, 60, 591, 41)

        self.choose_categories_label = QLabel(self)
        self.choose_categories_label.setText("Выбери интересующую тебя категорию")
        self.choose_categories_label.setStyleSheet("color: white;"
                                                   "font-size: 18px;")
        self.choose_categories_label.setGeometry(230, 110, 341, 21)

        # Combobox для более конкретного выбора
        self.genre_combobox = QComboBox(self)
        self.genre_combobox.addItems(('Совет', 'Мотивация', 'Цитаты великих людей', 'Народная мудрость'))
        self.genre_combobox.setGeometry(270, 140, 261, 35)

        # результаты - label и сам результат в QTextEdit
        self.result_label = QLabel(self)
        self.result_label.setText("Накопленные знания:")
        self.result_label.setStyleSheet("color: white;"
                                        "font-size: 16px;")
        self.result_label.setGeometry(110, 240, 171, 20)
        self.result_label.hide()  # прячем, так как пользователь не просит совета во время запуска программы

        # список полученных советов
        self.result = QListWidget(self)
        self.result.setGeometry(110, 270, 571, 211)
        self.result.hide()  # прячем, так как пользователь не просит совета во время запуска программы

        # записываем данные, которые уже были в файле
        with open('Tips_list.txt', "rt", encoding="utf8") as records:
            for day_tip in records.readlines():
                self.result.insertItem(0, f"{day_tip.split(';')[0]}: {day_tip.split(';')[1]}")  # добавляем в список

        # сообщение о том, что уже получали совет
        self.wait_label = QLabel(self)
        self.wait_label.setText('Вы уже получили свой совет. Дождитесь завтра')
        self.wait_label.setStyleSheet("color: white;")
        self.wait_label.setGeometry(110, 490, 311, 16)
        self.wait_label.hide()  # прячем

        # QPushButton, при нажатии на которую сгенерируется ответ
        self.get_answer_btn = QPushButton('Получить благословение богов', self)
        self.get_answer_btn.setGeometry(280, 190, 231, 41)
        self.get_answer_btn.clicked.connect(self.get_answer)

    def get_answer(self):  # получаем совет, записанный в поле

        # отображаем поле ответа
        self.result_label.show()
        self.result.show()

        attempt = False  # можно ли получить сегодня совет

        with open('Tips_list.txt', "rt",
                  encoding="utf8") as records:  # проверка на наличие попыток для получение совета
            for day_tip in records.readlines():
                if day_tip.split(";")[0] == str(datetime.datetime.now().date()):  # проверяем, получали ли мы уже совет
                    self.wait_label.show()  # показываем сообщение о том, что сегодня уже получили совет
                    break
            else:
                attempt = True  # можно получить совет
                self.wait_label.hide()  # скрываем надпись, потому что уже не нужна

        if attempt:
            Type = self.genre_combobox.currentText()
            with open('Tips_list.txt', "wt", encoding="utf8") as records:  # Записываем совет в файл
                with sqlite3.connect('Database.db') as con:  # Подключение к БД
                    cur = con.cursor()  # Создание курсора
                    advices = cur.execute(
                        f"""select Tip from Tips where Type = '{Type}'""").fetchall()  # Выполнение запроса
                    advice = random.choice(advices)  # получаем один рандомный совет из подходящих
                    self.result.insertItem(0, f"{datetime.datetime.now().date()}: {advice[0]}")
                records.write(f"{datetime.datetime.now().date()};{advice[0]}")  # Записываем в файл

        # Выводим советы
        self.result.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
