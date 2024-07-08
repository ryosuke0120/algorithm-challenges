import tkinter as tk
from tkinter import Canvas, Scrollbar, Frame


class CardGameUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TGC Game UI")
        self.geometry("1024x768")
        self.configure(bg="#282c34")

        # Create main frames
        left_frame = Frame(self, bg="#282c34")
        right_frame = Frame(self, bg="#282c34")

        left_frame.place(relx=0, rely=0, relwidth=0.2, relheight=1)
        right_frame.place(relx=0.2, rely=0, relwidth=0.8, relheight=1)

        # Left Frame Layout
        self.create_left_frame(left_frame)

        # Right Frame Layout
        self.create_right_frame(right_frame)

    def card_frame(self, parent):
        # フレーム(横幅と縦幅は固定値で指定)
        card_frame = tk.Frame(parent, width=200, height=300, bg="#485792", borderwidth=1, relief="solid")
        card_frame.pack()

        # カードの内側
        # inner_frame = tk.Frame(card_frame, width=160, height=200, bg="#123432")
        # inner_frame.pack(pady=10, padx=10)

        # # カード名の表示(横幅はいっぱいに広げる)
        # title = tk.Label(card_frame, text="カード名", border=1, relief="solid")
        # title.pack(fill="x")

        # # ダミーのカードイメージ（正方形）を描画するCanvas
        # canvas = tk.Canvas(card_frame, width=160, height=100, border=1, relief="solid")
        # # 背景色を白色にする(中心に配置)
        # # canvas.create_rectangle(0, 0, 110, 110, outline="black", fill="white")
        # canvas.pack()

        # # カード効果テキストの表示
        # detail = tk.Label(card_frame, text="このカードが召喚に成功したとき、相手の手札を一枚捨てる", wraplength=100)
        # detail.pack(fill="x")

        # # 攻撃力と守備力の表示
        # text = "攻撃力: 1000 / 守備力: 1000"
        # tk.Label(card_frame, text=text).pack()

        return card_frame

    def create_left_frame(self, parent):
        # Top Frame for Game State Information
        top_frame = Frame(parent, bg="#383c44")
        top_frame.place(relx=0, rely=0, relwidth=1, relheight=0.3)

        turn_label = tk.Label(top_frame, text="Turn: 1", fg="white", bg="#383c44", font=("Helvetica", 14))
        turn_label.pack(pady=10)

        player_label = tk.Label(top_frame, text="Player: HP 20", fg="white", bg="#383c44", font=("Helvetica", 14))
        player_label.pack(pady=10)

        enemy_label = tk.Label(top_frame, text="Enemy: HP 20", fg="white", bg="#383c44", font=("Helvetica", 14))
        enemy_label.pack(pady=10)

        # Bottom Frame for Card Details
        bottom_frame = Frame(parent, bg="#3e434c")
        bottom_frame.place(relx=0, rely=0.3, relwidth=1, relheight=0.7)

        card_name = tk.Label(bottom_frame, text="Card Name", fg="white", bg="#3e434c", font=("Helvetica", 18))
        card_name.pack(pady=10)

        card_image = Canvas(bottom_frame, width=100, height=150, bg="white")
        card_image.pack(pady=10)

        card_text = tk.Label(bottom_frame, text="Card Text", fg="white", bg="#3e434c", font=("Helvetica", 14))
        card_text.pack(pady=10)

        card_stats = tk.Label(bottom_frame, text="Attack: 10, Defense: 10", fg="white", bg="#3e434c", font=("Helvetica", 14))
        card_stats.pack(pady=10)

    def create_right_frame(self, parent):
        self.card_frame(parent)
        # # Top Frame for Enemy Field
        # top_frame = Frame(parent, bg="#383c44")
        # top_frame.place(relx=0, rely=0, relwidth=1, relheight=0.4)
        # self.create_field_grid(top_frame, "Enemy")

        # # Middle Frame for Player Field
        # middle_frame = Frame(parent, bg="#3e434c")
        # middle_frame.place(relx=0, rely=0.4, relwidth=1, relheight=0.4)
        # self.create_field_grid(middle_frame, "Player")

        # # Bottom Frame for Hand Zone
        # bottom_frame = Frame(parent, bg="#282c34")
        # bottom_frame.place(relx=0, rely=0.8, relwidth=1, relheight=0.2)

        # hand_canvas = Canvas(bottom_frame, bg="#282c34")
        # hand_canvas.pack(side="left", fill="both", expand=True)

        # scrollbar = Scrollbar(bottom_frame, orient="horizontal", command=hand_canvas.xview)
        # scrollbar.pack(side="bottom", fill="x")

        # hand_canvas.configure(xscrollcommand=scrollbar.set)
        # hand_canvas.bind('<Configure>', lambda e: hand_canvas.configure(scrollregion=hand_canvas.bbox("all")))

        # hand_frame = Frame(hand_canvas, bg="#282c34")
        # hand_canvas.create_window((0, 0), window=hand_frame, anchor="nw")

        # # Add cards to hand frame for demo purposes
        # for i in range(7):
        #     card = Canvas(hand_frame, width=100, height=150, bg="white")
        #     card.grid(row=0, column=i, padx=10, pady=10)

    def create_field_grid(self, parent, label_text):
        for row in range(2):
            for col in range(3):
                frame = Frame(parent, width=100, height=100, bg="#4e555e", highlightbackground="white", highlightthickness=1)
                frame.grid(row=row, column=col, padx=10, pady=10)
                frame.grid_propagate(False)

                label = tk.Label(frame, text=label_text, fg="white", bg="#4e555e", font=("Helvetica", 10))
                label.pack(expand=True)


if __name__ == "__main__":
    app = CardGameUI()
    app.mainloop()


# 描画メモ
# スタック構造で描画するのが一番楽かもしれない
# なので、ラッパークラスを記載した方がわかりやすいかも...
card = ZStack(
    VStack(
        Text("Card Name", size=24),
        Box(w=200, h=200, bg="white"),
        Text("Card Text", size=18),
        Text("Attack: 10, Defense: 10", size=18)
    ).Alien("center")
).size(200, 300).border(1, "black").bg("blue")