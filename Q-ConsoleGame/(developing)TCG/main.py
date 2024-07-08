import tkinter as tk

from src.models import Card, Player, Field
from src.views import fieldView, dialogView


def main():
    root = tk.Tk()
    root.title("Trading Card Game")
    root.geometry("800x600")

    dialog = dialogView(root)

    # ボタンを作成
    def show_dialog():
        print("Show Dialog")
    button = tk.Button(root, text="Show Dialog", command=show_dialog)
    button.pack()

    # --------------------------------------
    # データ作成
    # --------------------------------------
    # 仮のカードデータ
    card1 = Card(name="Dragon", detail="A powerful dragon.", attack=3000, defense=2500)
    card2 = Card(name="Warrior", detail="A brave warrior.", attack=1500, defense=1200)
    card3 = Card(name="Mage", detail="A wise mage.", attack=1200, defense=1500)
    card4 = Card(name="Goblin", detail="A weak goblin.", attack=800, defense=800)
    card5 = Card(name="Slime", detail="A slimy slime.", attack=500, defense=500)

    # 仮のプレイヤーとフィールドデータ
    player1 = Player(name="Player 1", deck=[card1, card2], hand=[card3, card4, card5])
    player2 = Player(name="Player 2", deck=[card2], hand=[card1])
    field = Field(player1=player1, player2=player2)

    # --------------------------------------
    # ビュー作成
    # --------------------------------------
    # フィールドビューを作成し表示
    field_frame = fieldView(root, field)
    field_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # それぞれのカードを表示するフレームを作成し表示
    # for card in player1.deck:
    #     card_frame = fieldCardView(root, card)
    #     card_frame.pack(side=tk.LEFT, padx=10, pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
