from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QIcon
from PyQt6.uic import loadUi
import sys


########################################
# Объявление базовых методов #
########################################


def initialize_board():
    board = {}
    # Пешки
    for col in 'abcdefgh':
        board[f"{col}2"] = ChessPiece("pawn", "white", f"{col}2")
        board[f"{col}7"] = ChessPiece("pawn", "black", f"{col}7")
    # Белые фигуры
    board.update({
        "a1": ChessPiece("rook", "white", "a1"),
        "h1": ChessPiece("rook", "white", "h1"),
        "b1": ChessPiece("knight", "white", "b1"),
        "g1": ChessPiece("knight", "white", "g1"),
        "c1": ChessPiece("bishop", "white", "c1"),
        "f1": ChessPiece("bishop", "white", "f1"),
        "d1": ChessPiece("queen", "white", "d1"),
        "e1": ChessPiece("king", "white", "e1"),
    })
    # Чёрные фигуры
    board.update({
        "a8": ChessPiece("rook", "black", "a8"),
        "h8": ChessPiece("rook", "black", "h8"),
        "b8": ChessPiece("knight", "black", "b8"),
        "g8": ChessPiece("knight", "black", "g8"),
        "c8": ChessPiece("bishop", "black", "c8"),
        "f8": ChessPiece("bishop", "black", "f8"),
        "d8": ChessPiece("queen", "black", "d8"),
        "e8": ChessPiece("king", "black", "e8"),
    })
    return board


########################################
# Класс фигуры, нужен для создания шаблона фигуры #
########################################


class ChessPiece:
    def __init__(self, piece_type, color, position):
        self.piece_type = piece_type  # Тип фигуры ('pawn', 'rook', 'knight', 'bishop', 'queen', 'king')
        self.color = color  # Цвет ('white' или 'black')
        self.position = position  # Текущая позиция (например, 'a2')

    def __repr__(self):
        return f"{self.color} {self.piece_type} at {self.position}"

########################################
# Класс приложения, наш капот #
########################################

class ChessApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("gui/board.ui", self)
        self.board_state = initialize_board()  # Начальная расстановка фигур
        self.selected_piece = None  # Хранит выбранную фигуру
        self.current_turn = "white"  # Белые начинают
        self.setup_buttons()
        self.update_board_display()

    def move_piece(self, from_pos, to_pos):
        if from_pos in self.board_state:
            piece = self.board_state.pop(from_pos)  # Удаляем фигуру с текущей позиции
            piece.position = to_pos  # Обновляем её позицию
            self.board_state[to_pos] = piece  # Ставим фигуру на новую позицию
            self.update_board_display()  # Обновляем отображение на доске
        else:
            print("Невозможно выполнить ход")

    def setup_buttons(self):
        self.buttons = {}
        for row in 'abcdefgh':
            for col in range(1, 9):
                cell_name = f"cell_{row}_{col}"
                cell = getattr(self, cell_name)
                self.buttons[f"{row}{col}"] = cell
                cell.clicked.connect(lambda _, r=row, c=col: self.on_cell_clicked(f"{r}{c}"))

    def on_cell_clicked(self, position):
        piece = self.board_state.get(position)

        if self.selected_piece:  # Уже выбрана фигура
            if position != self.selected_piece:  # Кликнули на новую клетку
                if self.validate_move(self.selected_piece, position):  # Проверка допустимости хода
                    self.move_piece(self.selected_piece, position)  # Переместить фигуру
                    self.switch_turn()  # Сменить ход
                else:
                    print("Недопустимый ход!")
            self.selected_piece = None  # Сбрасываем выбор
        else:  # Выбор новой фигуры
            if piece and piece.color == self.current_turn:  # Проверяем, что фигура текущего игрока
                self.selected_piece = position  # Сохраняем текущую клетку как выбранную
                print(f"Вы выбрали {piece}")
            elif piece:
                print(f"Сейчас ход {self.current_turn}, нельзя выбрать {piece.color}")
            else:
                print(f"Клетка {position} пуста")

    def update_board_display(self):
        for position, button in self.buttons.items():
            piece = self.board_state.get(position)
            if piece:
                icon_path = f"assets/{piece.color}_{piece.piece_type}.svg"  # Убедитесь, что такие иконки есть
                button.setIcon(QIcon(icon_path))
                button.setIconSize(button.size())
            else:
                button.setIcon(QIcon())

    def switch_turn(self):
        self.current_turn = "white" if self.current_turn == "black" else "black"
        print(f"Сейчас ход {self.current_turn}")

    def validate_move(self, from_pos, to_pos):
        piece = self.board_state.get(from_pos)
        target = self.board_state.get(to_pos)

        # Нельзя ходить на клетку, где уже есть своя фигура
        if target and target.color == piece.color:
            return False

        # Пример проверки для пешки
        if piece.piece_type == "pawn":
            direction = 1 if piece.color == "white" else -1
            from_row, from_col = int(from_pos[1]), from_pos[0]
            to_row, to_col = int(to_pos[1]), to_pos[0]

            # Пешка ходит вперёд на одну клетку
            if to_col == from_col and to_row == from_row + direction and not target:
                return True

            # Пешка бьёт по диагонали
            if abs(ord(to_col) - ord(from_col)) == 1 and to_row == from_row + direction and target:
                return True

            return False

        # Пока разрешаем ходы для остальных фигур
        return True


########################################
# Точка входа и инициализация #
########################################


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChessApp()
    window.show()
    sys.exit(app.exec())
