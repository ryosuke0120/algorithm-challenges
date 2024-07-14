import tkinter as tk
from typing import Callable, Dict, List, Union, Optional


class GameObject:
    """Base class for all game objects."""
    def __init__(self):
        self.onclick: Optional[Callable] = None

    def draw(self, canvas: tk.Canvas, x: int, y: int):
        raise NotImplementedError("Must be implemented by subclass")

    def bind_click(self, canvas: tk.Canvas, item_id: int):
        if self.onclick:
            canvas.tag_bind(item_id, "<Button-1>", lambda event: self.onclick())


class Rect(GameObject):
    def __init__(self, items: List[GameObject], width: int, height: int):
        super().__init__()
        self.items = items
        self.width = width
        self.height = height

    def draw(self, canvas: tk.Canvas, x: int, y: int):
        rect_id = canvas.create_rectangle(x, y, x + self.width, y + self.height, fill="white")
        for item in self.items:
            item.draw(canvas, x, y)
        self.bind_click(canvas, rect_id)
        return rect_id


class Text(GameObject):
    def __init__(self, text: str):
        super().__init__()
        self.text = text
        self.x = 0
        self.y = 0

    def pos(self, x: int, y: int):
        self.x = x
        self.y = y
        return self

    def draw(self, canvas: tk.Canvas, offset_x: int, offset_y: int):
        text_id = canvas.create_text(self.x + offset_x, self.y + offset_y, text=self.text)
        self.bind_click(canvas, text_id)
        return text_id


class CanvasWrapper:
    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas
        self.objects: Dict[str, GameObject] = {}

    def add(self, name: str, obj: GameObject, x: int, y: int):
        self.objects[name] = obj
        obj_id = obj.draw(self.canvas, x, y)
        self.canvas.tag_bind(obj_id, "<Button-1>", lambda event, name=name: self.on_click(name))

    def on_click(self, name: str):
        obj = self.objects[name]
        if hasattr(obj, 'onclick') and callable(obj.onclick):
            obj.onclick()


class FrameWrapper:
    def __init__(self, root: tk.Tk, frame: tk.Frame):
        self.root = root
        self.frame = frame
        self.widgets: Dict[str, Union[tk.Widget, CanvasWrapper]] = {}

    def add_button(self, text: str, font: Optional[tuple] = None, action: Optional[Callable] = None):
        button = tk.Button(self.frame, text=text, font=font, command=action)
        button.pack()
        return button

    def add_canvas(self, name: str, width: int, height: int, bg: str):
        canvas = tk.Canvas(self.frame, width=width, height=height, bg=bg)
        canvas.pack()
        self.widgets[name] = CanvasWrapper(canvas)
        return self.widgets[name]

    def get_widget(self, name: str) -> Union[tk.Widget, CanvasWrapper]:
        return self.widgets[name]


class TkWrapper:
    def __init__(self, title: str = "Tkinter Wrapper", width: int = 800, height: int = 600):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(f"{width}x{height}")
        self.frames: Dict[str, FrameWrapper] = {}

    def add_frame(self, name: str):
        frame = tk.Frame(self.root)
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        frame_wrapper = FrameWrapper(self.root, frame)
        self.frames[name] = frame_wrapper
        return frame_wrapper

    def get_frame(self, name: str) -> FrameWrapper:
        return self.frames[name]

    def show_frame(self, name: str):
        for frame in self.frames.values():
            frame.frame.lower()
        frame_wrapper = self.frames.get(name)
        if frame_wrapper:
            frame_wrapper.frame.lift()

    def run(self, start_frame: str = "main"):
        self.show_frame(start_frame)
        self.root.mainloop()

    def quit(self):
        self.root.quit()


class Card(GameObject):
    def __init__(self, suit: str, number: str):
        super().__init__()
        self.suit = suit
        self.number = number

    def draw(self, canvas: tk.Canvas, x: int, y: int):
        item = Rect([
            Text(self.number).pos(5, 5),
            Text(self.suit).pos(5, 25)
        ], width=50, height=70)
        return item.draw(canvas, x, y)


if __name__ == "__main__":
    app = TkWrapper(title="Poker Game", width=800, height=600)

    # メイン画面
    main_frame = app.add_frame("main")
    main_frame.add_button("Poker Game", font=("Helvetica", 24), action=lambda: app.show_frame("game"))
    main_frame.add_button("Settings", action=lambda: app.show_frame("settings"))
    main_frame.add_button("Exit", action=app.quit)

    # ゲーム画面
    game_frame = app.add_frame("game")
    canvas = game_frame.add_canvas("card_canvas", width=600, height=400, bg="green")
    game_frame.add_button("Deal Cards", action=lambda: print("Deal Cards"))
    game_frame.add_button("Back to Main Menu", action=lambda: app.show_frame("main"))

    # 味方のカードを描画
    for i in range(5):
        card = Card(suit="♥", number="A")
        card.onclick = lambda i=i: print(f"Clicked card {i}")
        canvas.add(f"player_card_{i}", card, x=70*i, y=100)

    # 設定
    settings_frame = app.add_frame("settings")
    settings_frame.add_button("Back to Main Menu", action=lambda: app.show_frame("main"))

    app.run("main")
