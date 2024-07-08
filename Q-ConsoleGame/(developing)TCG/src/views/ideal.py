import TkWrapper as tk


class Card(tk.GameObject):
    def __init__(self, suit: str, number: str):
        super().__init__()
        self.suit = suit
        self.number = number

    def draw(self, x: int, y: int):
        item = tk.VStack([
            tk.Text(self.number).pos(5, 5),
            tk.Text(self.suit).pos(5, 25)
        ], width=50, height=70)
        return item.draw(canvas, x, y)

class CardField(tk.GameObject):
    def __init__(self):
        super().__init__()
        self.cards = []

    def draw(self, x: int, y: int):
        item = tk.HStack(self.cards, spacing=10)
        return item.draw(canvas, x, y)


if __name__ == "__main__":
    app = tk.App(title="Poker Game", width=800, height=600)

    # メイン画面
    canvas = app.get_canvas("main")
    canvas.add_button("play_game", text="Poker Game", font=("Helvetica", 24), action=lambda: app.show_window("game"))
    canvas.add_button("go_setting", text="Settings", action=lambda: app.show_window("settings"))
    canvas.add_button("quit_app", text="Exit", action=app.quit)

    # ゲーム画面
    canvas = app.get_canvas("game", bg="green")
    canvas.add_button("Deal Cards", action=lambda: print("Deal Cards"))
    canvas.add_button("Back to Main Menu", action=lambda: app.show_frame("main"))

    # 味方のカードを描画
    cards = [Card(f"card{i}", suit="♥", number="A", onclick=lambda i=i: print(f"Clicked card {i}")) for i in range(5)]
    card_set = tk.HStack("card_item", cards, spacing=10)
    canvas.add("player_card", card_set, x=70*i, y=100)

    # 設定
    settings_frame = app.get_frame("settings")
    settings_frame.add_button("Back to Main Menu", action=lambda: app.show_frame("main"))

    app.run("main")

# ボックスで選択できること
# - padding, margin,