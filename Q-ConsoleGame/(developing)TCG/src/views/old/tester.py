import tkinter as tk
import random
from typing import Dict, List, Optional, Union


class FrameWrapper:
    """
    A wrapper class for a tkinter Frame to manage and add widgets.

    Attributes:
        root (tk.Tk): The root tkinter window.
        frame (tk.Frame): The tkinter frame managed by this wrapper.
        widgets (Dict[str, tk.Widget]): A dictionary to store widgets by name.
    """
    def __init__(self, root: tk.Tk, frame: tk.Frame) -> None:
        self.root = root
        self.frame = frame
        self.widgets: Dict[str, tk.Widget] = {}

    def add(self, widget_type: str, widget_name: str, pack_options: Optional[Dict[str, Union[int, str]]] = None, **widget_options: Union[int, str]) -> None:
        """
        Add a widget to the frame and pack it.

        Args:
            widget_type (str): The type of widget (e.g., 'Button', 'Label').
            widget_name (str): The name of the widget to store in the widgets dictionary.
            pack_options (Optional[Dict[str, Union[int, str]]], optional): Options for packing the widget.
            **widget_options: Additional options for creating the widget.
        """
        widget_class = getattr(tk, widget_type)
        widget = widget_class(self.frame, **widget_options)
        self.widgets[widget_name] = widget
        widget.pack(**(pack_options or {}))


class TkinterWrapper:
    """
    A wrapper class for a tkinter application to manage multiple frames.

    Attributes:
        root (tk.Tk): The root tkinter window.
        frames (Dict[str, FrameWrapper]): A dictionary to store frames by name.
        current_hand (List[Dict[str, Union[str, int]]]): The current hand of cards.
    """
    def __init__(self, title: str = "Tkinter Wrapper", width: int = 800, height: int = 600) -> None:
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(f"{width}x{height}")
        self.frames: Dict[str, FrameWrapper] = {}
        self.current_hand: List[Dict[str, Union[str, int]]] = []

    def add_frame(self, name: str) -> FrameWrapper:
        """
        Add a new frame to the application.

        Args:
            name (str): The name of the frame.

        Returns:
            FrameWrapper: The wrapped frame.
        """
        frame = tk.Frame(self.root)
        frame_wrapper = FrameWrapper(self.root, frame)
        self.frames[name] = frame_wrapper
        return frame_wrapper

    def show_frame(self, name: str) -> None:
        """
        Show the specified frame.

        Args:
            name (str): The name of the frame to show.
        """
        frame_wrapper = self.frames.get(name)
        if frame_wrapper:
            frame_wrapper.frame.tkraise()

    def run(self) -> None:
        """
        Run the tkinter main loop.
        """
        for frame_wrapper in self.frames.values():
            frame_wrapper.frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.show_frame("main")  # Default frame to show
        self.root.mainloop()

def setup_main_screen(app: TkinterWrapper) -> None:
    main = app.add_frame("main")
    main.add("Label", "main_label", pack_options={"pady": 20}, text="Main Menu", font=("Arial", 24))
    main.add("Button", "start_button", pack_options={"pady": 10}, text="Start Game", command=lambda: app.show_frame("game"))
    main.add("Button", "settings_button", pack_options={"pady": 10}, text="Settings", command=lambda: app.show_frame("settings"))
    main.add("Button", "exit_button", pack_options={"pady": 10}, text="Exit", command=app.root.quit)

def setup_game_screen(app: TkinterWrapper) -> None:
    game = app.add_frame("game")
    game.add("Label", "game_label", pack_options={"pady": 20}, text="Game Screen", font=("Arial", 24))
    game.add("Button", "back_button_game", pack_options={"pady": 10}, text="Back to Main Menu", command=lambda: app.show_frame("main"))
    game.add("Canvas", "card_canvas", width=600, height=400, bg="green")
    game.add("Button", "deal_button", pack_options={"pady": 10}, text="Deal Cards", command=lambda: deal_cards(app))
    game.add("Label", "hand_label", pack_options={"pady": 10}, text="", font=("Arial", 16))

def setup_settings_screen(app: TkinterWrapper) -> None:
    settings = app.add_frame("settings")
    settings.add("Label", "settings_label", pack_options={"pady": 20}, text="Settings", font=("Arial", 24))
    settings.add("Button", "back_button_settings", pack_options={"pady": 10}, text="Back to Main Menu", command=lambda: app.show_frame("main"))

def deal_cards(app: TkinterWrapper) -> None:
    game = app.frames["game"]
    card_canvas = game.widgets["card_canvas"]
    card_canvas.delete("all")

    # カード情報
    suits = ["♠", "♥", "♦", "♣"]
    numbers = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    colors = {"♠": "black", "♣": "black", "♥": "red", "♦": "red"}

    deck = [{"number": number, "suit": suit, "color": colors[suit]} for suit in suits for number in numbers]
    random.shuffle(deck)
    app.current_hand = deck[:5]

    # カードを配置
    card_width, card_height = 50, 70
    x_offset, y_offset = 20, 20

    for i, card in enumerate(app.current_hand):
        x = x_offset + i * (card_width + 10)
        y = y_offset
        rect = card_canvas.create_rectangle(x, y, x + card_width, y + card_height, fill="white")
        text1 = card_canvas.create_text(x + card_width / 2, y + 20, text=card["number"], fill=card["color"], font=("Arial", 16))
        text2 = card_canvas.create_text(x + card_width / 2, y + 50, text=card["suit"], fill=card["color"], font=("Arial", 16))

        # カードクリックイベントをバインド
        card_canvas.tag_bind(rect, "<Button-1>", lambda event, index=i: swap_card(app, index))
        card_canvas.tag_bind(text1, "<Button-1>", lambda event, index=i: swap_card(app, index))
        card_canvas.tag_bind(text2, "<Button-1>", lambda event, index=i: swap_card(app, index))

    hand_label = game.widgets["hand_label"]
    hand_label.config(text=check_hand(app.current_hand))

def swap_card(app: TkinterWrapper, index: int) -> None:
    """
    Swap the clicked card with a new one from the deck and re-evaluate the hand.

    Args:
        app (TkinterWrapper): The tkinter application wrapper.
        index (int): The index of the card to swap.
    """
    game = app.frames["game"]
    card_canvas = game.widgets["card_canvas"]

    # カード情報
    suits = ["♠", "♥", "♦", "♣"]
    numbers = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    colors = {"♠": "black", "♣": "black", "♥": "red", "♦": "red"}

    deck = [{"number": number, "suit": suit, "color": colors[suit]} for suit in suits for number in numbers]
    random.shuffle(deck)

    # 新しいカードに交換
    new_card = deck.pop()
    app.current_hand[index] = new_card

    # 再描画
    card_canvas.delete("all")
    card_width, card_height = 50, 70
    x_offset, y_offset = 20, 20

    for i, card in enumerate(app.current_hand):
        x = x_offset + i * (card_width + 10)
        y = y_offset
        rect = card_canvas.create_rectangle(x, y, x + card_width, y + card_height, fill="white")
        text1 = card_canvas.create_text(x + card_width / 2, y + 20, text=card["number"], fill=card["color"], font=("Arial", 16))
        text2 = card_canvas.create_text(x + card_width / 2, y + 50, text=card["suit"], fill=card["color"], font=("Arial", 16))

        # カードクリックイベントをバインド
        card_canvas.tag_bind(rect, "<Button-1>", lambda event, index=i: swap_card(app, index))
        card_canvas.tag_bind(text1, "<Button-1>", lambda event, index=i: swap_card(app, index))
        card_canvas.tag_bind(text2, "<Button-1>", lambda event, index=i: swap_card(app, index))

    hand_label = game.widgets["hand_label"]
    hand_label.config(text=check_hand(app.current_hand))

def check_hand(hand: List[Dict[str, Union[str, int]]]) -> str:
    """
    Check the hand and return the name of the poker hand.

    Args:
        hand (List[Dict[str, Union[str, int]]]): The list of cards in the hand.

    Returns:
        str: The name of the poker hand.
    """
    numbers = [card["number"] for card in hand]
    suits = [card["suit"] for card in hand]

    number_counts = {number: numbers.count(number) for number in set(numbers)}
    suit_counts = {suit: suits.count(suit) for suit in set(suits)}

    is_flush = len(suit_counts) == 1
    number_values = sorted([number_value(n) for n in numbers])
    is_straight = all(number_values[i] + 1 == number_values[i + 1] for i in range(len(number_values) - 1))

    if is_straight and is_flush:
        if number_values == [10, 11, 12, 13, 14]:
            return "ロイヤルストレートフラッシュ"
        return "ストレートフラッシュ"

    if 4 in number_counts.values():
        return "フォーカード"

    if sorted(number_counts.values()) == [2, 3]:
        return "フルハウス"

    if is_flush:
        return "フラッシュ"

    if is_straight:
        return "ストレート"

    if 3 in number_counts.values():
        return "スリーカード"

    pairs = list(number_counts.values()).count(2)
    if pairs == 2:
        return "ツーペア"

    if pairs == 1:
        return "ワンペア"

    return "ノーペア"

def number_value(number: str) -> int:
    """
    Convert card number to its respective value for hand evaluation.

    Args:
        number (str): The card number.

    Returns:
        int: The numerical value of the card.
    """
    if number == "A":
        return 14
    if number == "K":
        return 13
    if number == "Q":
        return 12
    if number == "J":
        return 11
    return int(number)

if __name__ == "__main__":
    app = TkinterWrapper(title="Poker Game", width=800, height=600)

    # 各画面をセットアップ
    setup_main_screen(app)
    setup_game_screen(app)
    setup_settings_screen(app)

    # アプリケーションの実行
    app.run()
