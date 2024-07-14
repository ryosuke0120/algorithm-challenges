import tkinter as tk
from tkinter import font as tkfont
from typing import Literal, Optional


class App:

    def __init__(self, title="App", w=800, h=600):
        root = tk.Tk()
        root.title(title)
        root.geometry(f"{w}x{h}")
        self.root = root

        self.w = w
        self.h = h

        self.canvases: dict[str, Canvas] = {}
        self.current_canvas_name = None

    def canvas(self, name: str):
        # 存在しない場合は新規作成
        if name not in self.canvases:
            c = Canvas(self.root, width=self.w, height=self.h)
            self.canvases[name] = c
        return self.canvases[name]

    def activate(self, name):
        if self.current_canvas_name:
            print(f"Deactivate: {self.current_canvas_name}")
            self.canvases[self.current_canvas_name].inner_canvas.pack_forget()
        print(f"Activate: {name}")
        self.canvases[name].inner_canvas.pack(fill=tk.BOTH, expand=True)
        self.canvases[name].paint()

        # 切り替え
        self.current_canvas_name = name

    def run(self, initial: str):
        self.current_canvas_name = initial
        self.activate(initial)
        self.root.mainloop()

    def quit(self):
        self.root.quit()


class Canvas:

    def __init__(self, root, width, height):
        self.inner_canvas = tk.Canvas(root, width=width, height=height)
        self.width = width
        self.height = height
        self.obj: Optional[GameObject] = None

    def body(self, obj):
        self.obj = obj

    def paint(self):
        if self.obj:
            # オブジェクトの関係性よりサイズを確定
            self.obj.resize(self)
            # ペイント
            self.obj.paint(self.inner_canvas, 0, 0)
        else:
            raise Exception("Bodyが設定されていません")


class GameObject:

    def __init__(self, name):
        self.name = name
        self.id = None
        self.width = 0
        self.height = 0
        self.parent: Optional["GameObject"] = None
        self.inner_anchor = "nw"

    def paint(self, canvas: tk.Canvas, x: int, y: int):
        raise NotImplementedError("Subclasses should implement this method")

    def resize(self, canvas: Canvas):
        raise NotImplementedError("Subclasses should implement this method")


class Box(GameObject):
    def __init__(self, *, w=100, h=30, name: str = "box"):
        super().__init__(name)
        self.width = w
        self.height = h
        self.fill = 'white'
        self.outline = 'black'
        self.line_width = 1
        self.active_fill = None
        self.active_outline = None
        self.active_line_width = None

    def paint(self, canvas: tk.Canvas, x: int, y: int):
        # アンカーによって位置を調整
        if self.inner_anchor == "nw":
            offset_x = 0
        elif self.inner_anchor == "n":
            offset_x = - self.width // 2
        elif self.inner_anchor == "ne":
            offset_x = -self.width
        else:
            raise ValueError(f"Invalid anchor type: {self.inner_anchor}")

        self.id = canvas.create_rectangle(
            x + offset_x, y, x + self.width + offset_x, y + self.height,
            fill=self.fill,
            outline=self.fill,
            width=self.line_width,
            activefill=self.active_fill,
            activeoutline=self.active_outline,
            activewidth=self.active_line_width,
        )

    def resize(self, canvas: Canvas):
        pass


class Text(GameObject):
    def __init__(self, text: str, *, name: str = "text", color: str = "black"):
        super().__init__(name)
        self.text = text
        self.font_family = "Helvetica"
        self.font_size = 12
        self.hover_color = color
        self.normal_color = color

    def paint(self, canvas: tk.Canvas, x: int, y: int):
        self.id = canvas.create_text(
            x, y, text=self.text, font=tkfont.Font(family=self.font_family, size=self.font_size),
            fill=self.normal_color, anchor=self.inner_anchor
        )
        # ホバーイベントのバインディング
        canvas.tag_bind(self.id, '<Enter>', self._on_enter)
        canvas.tag_bind(self.id, '<Leave>', self._on_leave)

    def font(self, *, family: Optional[str] = None, size: Optional[int] = None):
        if family:
            self.font_family = family
        if size:
            self.font_size = size
        return self

    def color(self, *, normal: Optional[str] = None, hover: Optional[str] = None):
        if normal:
            self.normal_color = normal
        if hover:
            self.hover_color = hover
        return self

    def resize(self, canvas: tk.Canvas):
        font = tkfont.Font(family=self.font_family, size=self.font_size)
        self.width = font.measure(self.text)
        self.height = font.metrics("linespace")

    def _on_enter(self, event):
        canvas = event.widget
        canvas.itemconfig(self.id, fill=self.hover_color)  # ホバー時に色を変更

    def _on_leave(self, event):
        canvas = event.widget
        canvas.itemconfig(self.id, fill=self.normal_color)  # 元の色に戻す


class Button(GameObject):

    def __init__(self, text: str, action: callable, *, width=200, height=30, name: str = "button"):
        super().__init__(name)
        self.width = width
        self.height = height
        self.action = action
        self.obj_text = Text(text=text, name="text")
        self.obj_box = VStack([self.obj_text], w=width, h=height, name="box")._anchor("center").justify("center")
        self.obj_box = self.obj_box.normal(
            fill='white', outline='#f0f0f0', width=0
        ).hover(fill="#f0f0f0", outline="#f0f0f0", width=0)
        self.font_size = 12
        self.font_family = "Helvetica"

    def font(self, *, family: Optional[str] = None, size: Optional[int] = None):
        if family:
            self.font_family = family
        if size:
            self.font_size = size
        self.obj_text.font(family=self.font_family, size=self.font_size)
        return self

    def normal(self, *, text_color: Optional[str], fill: Optional[str] = None, outline: Optional[str] = None, width: Optional[int] = None):
        self.obj_box.normal(fill=fill, outline=outline, width=width)
        if text_color:
            self.obj_text.color(normal=text_color)
        return self

    def hover(self, *, text_color: Optional[str], fill: Optional[str] = None, outline: Optional[str] = None, width: Optional[int] = None):
        self.obj_box.hover(fill=fill, outline=outline, width=width)
        if text_color:
            self.obj_text.color(hover=text_color)
        return self

    def paint(self, canvas: tk.Canvas, x: int, y: int):
        # ボタンのサイズを設定
        self.obj_box.width = self.width
        self.obj_box.height = self.height

        # アンカーによって位置を調整
        if self.inner_anchor == "nw":
            offset_x = 0
        elif self.inner_anchor == "n":
            offset_x = - self.width // 2
        elif self.inner_anchor == "ne":
            offset_x = -self.width
        else:
            raise ValueError(f"Invalid anchor type: {self.inner_anchor}")

        # ボタンの描画
        self.id = self.obj_box.id
        self.obj_box.paint(canvas, x + offset_x, y)

        # Bind text events to rectangle events
        for item in [self.obj_box, self.obj_text]:
            canvas.tag_bind(item.id, "<Enter>", lambda event: canvas.itemconfig(
                self.obj_box.id, fill=self.obj_box.active_fill, outline=self.obj_box.active_outline, width=self.obj_box.active_line_width))
            canvas.tag_bind(item.id, "<Leave>", lambda event: canvas.itemconfig(
                self.obj_box.id, fill=self.obj_box.fill, outline=self.obj_box.outline, width=self.obj_box.line_width))

        # アクションを登録
        canvas.tag_bind(self.obj_box.id, "<Button-1>", lambda event: self.action())
        canvas.tag_bind(self.obj_text.id, "<Button-1>", lambda event: self.action())

    def resize(self, canvas: Canvas):
        self.obj_box.resize(canvas)


class Stack(GameObject):
    def __init__(self, children: list[GameObject], *, w, h, s: int = 0, p: int = 0, name: str = "stack"):
        super().__init__(name)
        self.width = w
        self.height = h

        # 子要素の設定
        self.children = children
        for child in self.children:
            child.parent = self

        # スペース & 余白
        self.spacing = s
        self.padding = p

        # 通常
        self.fill = 'white'
        self.outline = 'black'
        self.line_width = 1

        # ホバー選択時
        self.active_fill = None
        self.active_outline = None
        self.active_line_width = None

        # アンカー
        self.anchor_type = "topLeft"
        self.justify_type = None

    # def _resize_self(self):
    #     raise NotImplementedError("Subclasses should implement this method")

    def resize(self, canvas: Canvas):
        # 自分のリサイズ
        # self._resize_self()

        # 子要素のリサイズ
        for child in self.children:
            child.resize(canvas)

    def _anchor(self, anchor: Literal[
            "topLeft", "top", "topRight",
            "left", "center", "right",
            "bottomLeft", "bottom", "bottomRight"]):
        self.anchor_type = anchor
        return self

    def anchor_top_left(self):
        return self._anchor("topLeft")

    def anchor_top(self):
        return self._anchor("top")

    def anchor_top_right(self):
        return self._anchor("topRight")

    def anchor_left(self):
        return self._anchor("left")

    def anchor_center(self):
        return self._anchor("center")

    def anchor_right(self):
        return self._anchor("right")

    def anchor_bottom_left(self):
        return self._anchor("bottomLeft")

    def anchor_bottom(self):
        return self._anchor("bottom")

    def anchor_bottom_right(self):
        return self._anchor("bottomRight")

    def anchor_padding_offset(self, x: int, y: int):

        # 中央揃えのための計算
        inner_width, inner_height = self.inner_size()
        p = self.padding
        wc = self.width // 2
        hc = self.height // 2 - inner_height // 2 - p
        wr = self.width - 2 * p
        s = self.height - inner_height - 4 * p

        # anchorによって位置を調整
        anchor_offsets = {
            "topLeft": (p, p), "top": (wc, p), "topRight": (wr, p),
            "left": (p, hc), "center": (wc, hc), "right": (wr, hc),
            "bottomLeft": (p, s), "bottom": (wc, s), "bottomRight": (wr, s)
        }

        if self.anchor_type in anchor_offsets:
            offset_x, offset_y = anchor_offsets[self.anchor_type]
        else:
            raise ValueError(f"Invalid anchor type: {self.anchor_type}")

        return offset_x, offset_y

    def inner_size(self):
        raise NotImplementedError("Subclasses should implement this method")

    def paint(self, canvas: tk.Canvas, x: int, y: int):
        # 自分を描画
        self.id = canvas.create_rectangle(
            x, y, x + self.width, y + self.height,
            fill=self.fill,
            outline=self.fill,
            width=self.line_width,
            activefill=self.active_fill,
            activeoutline=self.active_outline,
            activewidth=self.active_line_width,
        )

        # アンカーの計算
        offset_x, offset_y = self.anchor_padding_offset(x, y)

        self._paint_children(canvas, x + offset_x, y + offset_y)

    def _paint_children(self, canvas: tk.Canvas, x: int, y: int):
        raise NotImplementedError("Subclasses should implement this method")

    def hover(self, *, fill: Optional[str] = None, outline: Optional[str] = None, width: Optional[int] = None):
        if fill:
            self.active_fill = fill
        if outline:
            self.active_outline = outline
        if width:
            self.active_line_width = width
        return self

    def normal(self, *, fill: Optional[str] = None, outline: Optional[str] = None, width: Optional[int] = None):
        if fill:
            self.fill = fill
        if outline:
            self.outline = outline
        if width:
            self.line_width = width
        return self


class VStack(Stack):
    # def __init__(self, children: list[GameObject], *, w: int, h: int, s: int = 0, p: int = 0, name: str = "vstack"):
    #     super().__init__(children, spacing=s, padding=p, name=name)
    #     self._fixed_width = w
    #     self._fixed_height = h

    # def _resize_self(self):
    #     self.width = self._fixed_width
    #     self.height = self._fixed_height

    def inner_size(self):
        total_height = sum([child.height for child in self.children])
        total_hight_space = self.spacing * (len(self.children) - 1)
        total_padding = self.padding * 2
        return self.width - total_padding, total_height + total_hight_space - total_padding

    def justify(self, justify: Literal["left", "center", "right"]):
        self.justify_type = justify
        return self

    def _paint_children(self, canvas: tk.Canvas, x: int, y: int):
        # アンカーのデフォルト設定
        if self.justify_type is None:
            if self.anchor_type in ["topLeft", "left", "bottomLeft"]:
                self.justify_type = "left"
            elif self.anchor_type in ["topRight", "right", "bottomRight"]:
                self.justify_type = "right"
            elif self.anchor_type in ["top", "center", "bottom"]:
                self.justify_type = "center"

        # justifyの計算(width)
        max_item_width = max([child.width for child in self.children])
        if self.justify_type == "left":
            child_anchor = "nw"
            if self.anchor_type in ["topLeft", "left", "bottomLeft"]:
                x += 0
            elif self.anchor_type in ["top", "center", "bottom"]:
                x -= max_item_width // 2
            elif self.anchor_type in ["topRight", "right", "bottomRight"]:
                x -= max_item_width
        elif self.justify_type == "center":
            child_anchor = "n"
            if self.anchor_type in ["topLeft", "left", "bottomLeft"]:
                x += max_item_width // 2
            elif self.anchor_type in ["top", "center", "bottom"]:
                x += 0
            elif self.anchor_type in ["topRight", "right", "bottomRight"]:
                x -= max_item_width // 2
        elif self.justify_type == "right":
            child_anchor = "ne"
            if self.anchor_type in ["topLeft", "left", "bottomLeft"]:
                x += max_item_width
            elif self.anchor_type in ["top", "center", "bottom"]:
                x += max_item_width // 2
            elif self.anchor_type in ["topRight", "right", "bottomRight"]:
                x += 0
        else:
            raise ValueError(f"Invalid justify type: {self.justify_type}")

        for child in self.children:
            tmp_width = self.width - self.padding * 2
            child.width = tmp_width if child.width > tmp_width else child.width
            child.inner_anchor = child_anchor
            child.paint(canvas, x, y)
            y += child.height + self.spacing


class HStack(Stack):
    # def __init__(self, children: list[GameObject], *, h: int, s: int = 0, p: int = 0, name: str = "hstack"):
    #     super().__init__(children, spacing=s, padding=p, name=name)
    #     self._fixed_height = h
    #     self._fixed_height = h

    # def _resize_self(self):
    #     self.width = self.parent.width if self.parent else canvas.width
    #     self.height = self._fixed_height

    def inner_size(self):
        total_width = sum([child.width for child in self.children])
        total_width_space = self.spacing * (len(self.children) - 1)
        total_padding = self.padding * 2
        return total_width + total_width_space - total_padding, self.height - total_padding

    def _paint_children(self, canvas: tk.Canvas, x: int, y: int):
        for child in self.children:
            tmp_height = self.height - self.padding * 2
            child.height = tmp_height if child.height > tmp_height else child.height
            child.paint(canvas, x, y)
            x += child.width + self.spacing


def BlackButton(text, action):
    return Button(text, action=action).font(size=18).normal(
        text_color="white", fill="#333333", outline="#333333", width=0).hover(
        text_color="white", fill="#444444", outline="#444444", width=0)


SUIT = Literal["♠", "♥", "♦", "♣"]
NUMBER = Literal["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]


def Card(number: NUMBER, suit: SUIT):
    color = "black" if suit in ["♠", "♣"] else "red"
    return VStack([
        Text(str(number)).font(size=16).color(normal=color, hover=color),
        Text(suit).font(size=16).color(normal=color, hover=color),
    ], w=50, h=70, s=10, p=10).normal(fill="white", outline=color, width=1).anchor_center().justify("center")


def CardField():
    return HStack([
        Card("A", "♠"),
        Card("2", "♥"),
        Card("3", "♦"),
        Card("4", "♣"),
        Card("5", "♠"),
    ], w=300, h=80, s=10).normal(fill="#a6b724")


if __name__ == "__main__":
    app = App(title="Poker Game", w=800, h=600)
    canvas = app.canvas("main")
    canvas.body(
        VStack([
            Text("Poker Game").font(size=46).color(normal="black"),
            BlackButton("Start", lambda: app.activate("game")),
            BlackButton("Quit", lambda: app.quit())
        ], w=app.w, h=app.h, s=30).normal(fill="#348699").anchor_center()
    )
    canvas = app.canvas("game")
    canvas.body(
        HStack([
            VStack([
                CardField(),
                BlackButton("Deal", lambda: print("Deal")),
                BlackButton("Fold", lambda: print("Fold")),
                Text("Poker Game").font(size=24).color(normal="black", hover="red"),
                Text("This is a poker game.").font(size=12),
            ], w=400, h=app.h, p=10, s=10).normal(fill="#a6b724").anchor_top_left(),
            VStack([
                Text("Player: 1000"),
                Text("CPU: 1000"),
                Button("Back to menu", lambda: app.activate("main")),
            ], w=400, h=app.h, s=0, p=10).normal(fill="#348699"),
        ], h=app.h, w=app.w, s=20, p=10)
    )
    app.run("main")
