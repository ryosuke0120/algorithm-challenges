import tkinter as tk
from .. import models

from typing import Callable


def dialogView(parent: tk.Tk, message: str, on_yes: Callable[[], None], on_no: Callable[[], None]):
    # 背景を無効にするためのオーバーレイを作成
    overlay = tk.Canvas(parent, bg="black", highlightthickness=0)
    # overlay.place(relwidth=1, relheight=1)
    # parent.update_idletasks()  # Update the display to show the overlay

    # ダイアログフレームを作成
    dialog_frame = tk.Frame(parent, bg='lightgrey', borderwidth=2, relief="solid", padx=10, pady=10)
    dialog_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # フレームを中央に配置

    message_label = tk.Label(dialog_frame, text=message, bg='lightgrey')
    message_label.pack(pady=10)

    button_frame = tk.Frame(dialog_frame, bg='lightgrey')
    button_frame.pack(pady=10)

    def _on_yes():
        on_yes()
        dialog_frame.destroy()
        overlay.destroy()

    def _on_no():
        on_no()
        dialog_frame.destroy()
        overlay.destroy()

    tk.Button(button_frame, text="はい", command=_on_yes).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="いいえ", command=_on_no).pack(side=tk.RIGHT, padx=10)

    # ダイアログが表示されている間、オーバーレイで背景をカバー
    overlay.bind("<Button-1>", lambda event: None)  # クリックを無効にする

    return dialog_frame

def fieldCardView(parent: tk.Tk, card: models.Card):
    # カードフレームを作成
    card_frame = tk.Frame(parent, borderwidth=2, relief="solid", padx=10, pady=10)

    # カード名の表示
    tk.Label(card_frame, text=card.name).pack()

    # ダミーのカードイメージ（正方形）を描画するCanvas
    canvas = tk.Canvas(card_frame, width=100, height=100)
    canvas.pack()
    canvas.create_rectangle(10, 10, 90, 90, outline="black", fill="blue")  # 例として青い正方形を描画
    canvas.create_text(50, 50, text="カードイメージ")

    # カード効果テキストの表示
    tk.Label(card_frame, text=card.detail, wraplength=100).pack()

    # 攻撃力と守備力の表示
    text = f"攻撃力: {card.attack} / 守備力: {card.defense}"
    tk.Label(card_frame, text=text).pack()

    return card_frame

def fieldView(parent: tk.Tk, field: models.Field):
    # フィールドフレームを作成
    field_frame = tk.Frame(parent, borderwidth=2, relief="solid", padx=10, pady=10)

    # プレイヤー1の情報を表示
    player1_frame = tk.Frame(field_frame, borderwidth=2, relief="solid", padx=10, pady=10)
    player1_name_label = tk.Label(player1_frame, text=field.player1.name)
    player1_name_label.pack()
    player1_deck_label = tk.Label(player1_frame, text=f"デッキ枚数: {len(field.player1.deck)}")
    player1_deck_label.pack()
    player1_hand_label = tk.Label(player1_frame, text=f"手札枚数: {len(field.player1.hand)}")
    player1_hand_label.pack()
    player1_frame.grid(row=0, column=0, padx=5, pady=5)

    # プレイヤー2の情報を表示
    player2_frame = tk.Frame(field_frame, borderwidth=2, relief="solid", padx=10, pady=10)
    player2_name_label = tk.Label(player2_frame, text=field.player2.name)
    player2_name_label.pack()
    player2_deck_label = tk.Label(player2_frame, text=f"デッキ枚数: {len(field.player2.deck)}")
    player2_deck_label.pack()
    player2_hand_label = tk.Label(player2_frame, text=f"手札枚数: {len(field.player2.hand)}")
    player2_hand_label.pack()
    player2_frame.grid(row=0, column=1, padx=5, pady=5)

    # ボタンも作成する(押したらダイアログを表示)
    def show_dialog():
        dialogView(parent, "ダイアログです", lambda: print("Yes"), lambda: print("No"))

    button = tk.Button(field_frame, text="ダイアログを表示", command=show_dialog)
    button.grid(row=1, column=0, columnspan=2, pady=10)

    return field_frame
