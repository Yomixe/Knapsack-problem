#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import random

from PySide2.QtCore import Slot
from PySide2.QtGui import QColor

from PySide2.QtWidgets import (QApplication, QHeaderView, QHBoxLayout, QLabel, QLineEdit,
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget, QFileDialog)


class Widget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Problem plecakowy")

        """Inicjlizacja zmiennych, na których będą dokynowane obliczenia oraz utworzenie obiektów
        (tabela,pola edycyjne,przyciski)"""

        self.p = []
        self.w = []
        self.W = 0


        self.table = QTableWidget()
        self.n = QLineEdit()
        self.U = QLineEdit()

        self.file_name = QLineEdit()
        self.from_keys = QPushButton("Wprowadź dane")
        self.random = QPushButton("Generuj losowe wartości")
        self.from_file = QPushButton("Wprowadź dane z pliku")
        self.clear = QPushButton("Wyczyść")
        self.quit = QPushButton("Zamknij")
        self.solve1 = QPushButton("Rozwiąż korzystając z programowania zachłannego")
        self.solve2 = QPushButton("Rozwiąż korzystając z programowania dynamicznego")
        self.save = QPushButton("Zapis macierz do pliku")

        self.result_text = QLabel("Wartość plecaka:")
        self.result1 = QLabel()
        self.result2 = QLabel()

        """Tworzenie layoutów a następnie dodawanie do nich widgetów"""

        self.left = QVBoxLayout()
        self.left.addWidget(QLabel("Ilość rzeczy"))
        self.left.addWidget(self.n)
        self.left.addWidget(QLabel("Maksymalny udżwig"))
        self.left.addWidget(self.U)
        self.left.addWidget(self.from_keys)
        self.left.addWidget(self.random)
        self.left.addWidget(self.from_file)
        self.left.addWidget(self.clear)
        self.left.addWidget(self.quit)
        self.center = QVBoxLayout()
        self.right = QVBoxLayout()
        """Tworzenie  głównego layoutu a następnie dodawanie do nich trzech utworzonych wcześniej"""
        self.layout = QHBoxLayout()
        self.layout.addLayout(self.left)
        self.layout.addLayout(self.center)
        self.layout.addLayout(self.right)

        self.setLayout(self.layout)

        """Komunikacja pomiędzy obiektami"""
        self.from_keys.clicked.connect(self.create_table)

        self.random.clicked.connect(self.create_table)
        self.random.clicked.connect(self.random_values)

        self.from_file.clicked.connect(self.create_table)
        self.from_file.clicked.connect(self.values_from_file)

        self.solve1.clicked.connect(self.zapakuj_zachlannie)
        self.solve2.clicked.connect(self.zapakuj_dynamicznie)

        self.n.textChanged[str].connect(self.check_disable)
        self.U.textChanged[str].connect(self.check_disable)


:
        self.save.clicked.connect(self.save_to_file)
        self.quit.clicked.connect(self.quit_application)

    """Dodawanie do layoutu przycisków umożliwiających wybór metody obliczeń, zapisu do pliku oraz tekstu z wynikami"""

    def create_right_layout(self):

        self.layout.addLayout(self.right)
        self.right.addWidget(self.solve1)
        self.right.addWidget(self.solve2)
        self.right.addWidget(self.save)
        self.right.addWidget(self.result_text)
        self.right.addWidget(self.result1)
        self.right.addWidget(self.result2)
        self.result_text.hide()
        self.result1.hide()  # wyniki ukryte dopóki użytkownik nie zażąda rozwiązania
        self.result2.hide()

    """Tworzenie tabeli o ilości kolumn n, podanych przez użytkownika"""

    @Slot()
    def create_table(self):
        self.table.setColumnCount(int(self.n.text()))
        self.table.setRowCount(2)
        self.table.setVerticalHeaderLabels(["p[i]", "w[i]]"])

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.center.addWidget(self.table)
        self.create_right_layout()

    """Uzupełnianie pustych wartości obiektowej tabeli wartościami losowymi, konwertując te liczby na string, aby dane
           były poprawnie wyświetlone w oknie"""

    @Slot()
    def random_values(self):

        for i in range(self.table.columnCount()):
            self.table.setItem(0, i, QTableWidgetItem(str(random.randint(1, 100))))
            self.table.setItem(1, i, QTableWidgetItem(str(random.randint(1, 100))))

    """Uzupełnianie obiektowej tabeli wartościami z pliku"""

    @Slot()
    def values_from_file(self):
        self.left.insertWidget(8, self.file_name)  # dodawanie widgetu,który będzie wyświetlał nazwę pliku
        self.file_name.setText(QFileDialog.getOpenFileName()[0])

        with open(self.file_name.text(), 'r') as f:
            for idx_line, line in enumerate(f):
                for idx, item in enumerate(line.split(' ')):
                    self.table.setItem(idx_line, idx, QTableWidgetItem(str(item)))

    """Zapisywanie tabeli do pliku"""

    @Slot()
    def save_to_file(self):

        self.file_name.setText(QFileDialog.getSaveFileName()[0])

        with open(self.file_name.text(), 'w') as f:
            for i in range(self.table.columnCount()):
                f.write(self.table.item(0, i).text() + ' ')
            f.write('\n')
            for j in range(self.table.columnCount()):
                f.write(self.table.item(1, j).text() + ' ')

    """Konwertowanie obiektowej tabeli na listy p i w, na której będą dokonywane obliczenia"""

    def convert_to_lists(self):
        for i in range(self.table.columnCount()):
            self.p.append(int(self.table.item(0, i).text()))
        for j in range(self.table.columnCount()):
            self.w.append(int(self.table.item(1, j).text()))

    """Sortowanie-algorytm zachłanny"""

    def sort(self):
        n = int(self.n.text())
        w = self.w
        p = self.p
        for i in range(n - 1):
            for j in range(n - 1):
                if (p[j] / w[j]) <= p[j + 1] / w[j + 1]:
                    w[j], w[j + 1] = w[j + 1], w[j]
                    p[j], p[j + 1] = p[j + 1], p[j]

    """Algorytm zachłanny"""

    @Slot()
    def zapakuj_zachlannie(self):
        self.clear_result()
        self.convert_to_lists()
        self.sort()
        U = int(self.U.text())
        w = self.w
        p = self.p
        n = int(self.n.text())
        u = U
        for i in range(n):
            items = int(u / w[i])
            u -= items * w[i]
            self.W += items * p[i]

        self.solve1.setEnabled(False)
        self.result_text.show()
        self.result1.setText("*metodą programowania zachłannego: " + str(self.W))
        self.result1.show()

    """Algorytm dynamiczny"""

    @Slot()
    def zapakuj_dynamicznie(self):
        self.clear_result()
        self.convert_to_lists()
        P = [[0 for i in range(int(self.U.text()) + 1)] for i in range(int(self.n.text()) + 1)]
        Q = [[0 for i in range(int(self.U.text()) + 1)] for i in range(int(self.n.text()) + 1)]

        n = int(self.n.text())
        U = int(self.U.text())

        for i in range(1, n + 1):
            for j in range(1, U + 1):
                if j >= self.w[i - 1] and P[i - 1][j] < P[i][j - self.w[i - 1]] + self.p[i - 1]:
                    P[i][j] = P[i][j - self.w[i - 1]] + self.p[i - 1]
                    Q[i][j] = i
                else:
                    P[i][j] = P[i - 1][j]
                    Q[i][j] = Q[i - 1][j]

        self.W = P[i][j]

        u = U
        chosen = []
        print(P)
        while u != 0:
            value = Q[n][u]
            if value == 0:
                break
            chosen.append(value - 1)
            u = u - self.w[value - 1]

        for value in chosen:
            self.table.setRowCount(3)
            self.table.setVerticalHeaderLabels(["p[i]", "w[i]]", "Ilość wybranych\nprzedmiotów"])
            self.table.setItem(2, value, QTableWidgetItem(str(chosen.count(value))))
            for i in range(self.table.rowCount()):
                self.table.item(i, value).setBackground(QColor(255, 158, 163))

        self.solve2.setEnabled(False)
        self.result_text.show()

        self.result2.setText("*metodą programowania dynamicznego: " + str(self.W))
        self.result2.show()

    """Funkcja sprawdza czy są wpisane zarówno wartość n jak i P, 
        jeśli nie, niemożliwe jest wygenerowanie tabeli"""

    @Slot()
    def check_disable(self):
        actions = [self.from_keys, self.random, self.from_file]
        for action in actions:
            if not self.n.text() or not self.U.text():
                action.setEnabled(False)
            else:
                action.setEnabled(True)

    """Zamykanie aplikacji"""



    """Zerowanie zmiennej przechowującej wynik, oraz usuwanie wartości w tablciach p i w
    w celu wykonania drugiej metody do rozwiązania algorytmu plecakowego"""

    def clear_result(self):
        self.W = 0
        self.p = []
        self.w = []

    """Czyszczenie tabeli, czyli usuwanie kolumn, i ustawienie dwu wierszy, usuwanie wartosći tablic p,q,
         odblokawanie przycisków do rozwiązania problemu oraz ukrywanie pól z wynikami
         w celu możliwości pracy na innych danych"""

    @Slot()
    def clear_table(self):
        self.table.setColumnCount(0)
        self.table.setRowCount(2)
        self.p = []
        self.w = []
        self.solve1.setEnabled(True)
        self.solve2.setEnabled(True)

        self.result1.hide()
        self.result2.hide()
        self.result_text.hide()
    @Slot()
    def quit_application(self):
        QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.resize(1200, 300)
    widget.show()
    sys.exit(app.exec_())
