import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QKeyEvent
from PyQt5.QtCore import Qt, QTimer

# Game settings
WIDTH = 600
HEIGHT = 400
PADDLE_WIDTH = 50
BALL_SPEED = 2
SCORE_LIMIT = 10

# ASCII characters for visual representation
WALL = "#"
PADDLE = "@"
BALL = "o"
SPACE = " "

# Game state variables
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = random.choice([-1, 1]) * BALL_SPEED
ball_dy = random.choice([-1, 1]) * BALL_SPEED
player_paddle_y = HEIGHT // 2
computer_paddle_y = HEIGHT // 2
player_score = 0
computer_score = 0

class PongGame(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Pong")
        self.setGeometry(100, 100, WIDTH, HEIGHT)
        self.show()

        # Initialize timer for animation
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000 // 60)  # Update 60 times per second

        # Set keyboard event handling
        self.setFocus()
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QKeyEvent.KeyPress:
            if event.key() == Qt.Key_W and player_paddle_y > 0:
                player_paddle_y -= 10
            elif event.key() == Qt.Key_S and player_paddle_y < HEIGHT - PADDLE_WIDTH:
                player_paddle_y += 10
            self.repaint()
        return super().eventFilter(obj, event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.white)
        painter.setFont(QFont("Monospace", 12))

        # Draw game elements
        painter.drawText(20, 20, f"Player: {player_score}")
        painter.drawText(WIDTH - 100, 20, f"Computer: {computer_score}")

        for y in range(HEIGHT):
            for x in range(WIDTH):
                if x == 0 or x == WIDTH - 1:
                    painter.drawText(x * 10, y * 10, WALL)
                elif x == WIDTH // 2 - PADDLE_WIDTH // 2:
                    painter.drawText(x * 10, player_paddle_y * 10, PADDLE)
                elif x == WIDTH // 2 + PADDLE_WIDTH // 2:
                    painter.drawText(x * 10, computer_paddle_y * 10, PADDLE)
                elif x == ball_x // 10 and y == ball_y // 10:
                    painter.drawText(x * 10, y * 10, BALL)
                else:
                    painter.drawText(x * 10, y * 10, SPACE)

    def update(self):
        global ball_x, ball_y, ball_dx, ball_dy, player_score, computer_score

        # Move computer paddle with AI
        computer_paddle_y_next = ball_y
        if computer_paddle_y_next != computer_paddle_y:
            if computer_paddle_y_next < 0:
                computer_paddle_y_next = 0
            elif computer_paddle_y_next > HEIGHT - PADDLE_WIDTH:
                computer_paddle_y_next = HEIGHT - PADDLE_WIDTH
        computer_paddle_y = computer_paddle_y_next

        # Update ball position
        ball_x += ball_dx
        ball_y += ball_dy

    # Handle collisions
    handle_collisions()

    # Check for game end
    if player_score == SCORE_LIMIT or computer_score == SCORE_LIMIT:
        self.timer.stop()
        painter = QPainter(self)
        painter.setPen(Qt.white)
        painter.setFont(QFont("Monospace", 24))

        if player_score == SCORE_LIMIT:
            text = "Player wins!"
        else:
            text = "Computer wins!"

        painter.drawText(WIDTH // 2 - painter.fontMetrics().width(text) // 2, HEIGHT // 2, text)

        # Add option to play again or quit
        restart_button = QPushButton("Play Again", self)
        restart_button.setGeometry(WIDTH // 2 - 50, HEIGHT // 2 + 50, 100, 30)
        restart_button.clicked.connect(self.restart_game)

        quit_button = QPushButton("Quit", self)
        quit_button.setGeometry(WIDTH // 2 - 50, HEIGHT // 2 + 80, 100, 30)
        quit_button.clicked.connect(self.close)

        self.show()
    else:
        self.repaint()  # Update display


def restart_game(self):
    global ball_x, ball_y, ball_dx, ball_dy, player_score, computer_score

    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    ball_dx = random.choice([-1, 1]) * BALL_SPEED
    ball_dy = random.choice([-1, 1]) * BALL_SPEED
    player_score = 0
    computer_score = 0

    self.timer.start()
    self.repaint()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = PongGame()
    sys.exit(app.exec_())
