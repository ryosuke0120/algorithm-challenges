from abc import ABC, abstractmethod
import tkinter as tk
from typing import Optional, List


class GameObject(ABC):

    def __init__(self):
        self.frame = None
        self.background = None

    def instantiate(self, parent: tk.Widget):
        """オブジェクトを生成する"""
        if self.frame is None:
            self.frame = self.draw(parent)

    def destroy(self):
        """オブジェクトを破棄する"""
        if self.frame:
            self.frame.destroy()
            self.frame = None

    @abstractmethod
    def draw(self, parent: tk.Widget) -> tk.Widget:
        item = tk.Widget()
        item.pack()
        return item


class Text(GameObject):
    def __init__(self, text: str, *, bordercolor: str = "black", borderwidth: int = 0, background: Optional[str] = None):
        super().__init__()
        self.text = text
        self.bordercolor = bordercolor
        self.borderwidth = borderwidth
        self.background = background

    def draw(self, parent: tk.Widget):
        item = tk.Label(parent, text=self.text)
        item.pack()
        # 背景色を設定
        if self.background:
            item.config(bg=self.background)
        # 枠線を設定
        item.config(
            borderwidth=self.borderwidth,
            relief="solid",
            # highlightthickness=self.borderwidth
        )
        return item


class VStack(GameObject):
    def __init__(self, stacks: List[Text], *, spacing: int = 0, padding: int = 0,
                 bordercolor: str = "black", borderwidth: int = 1, background: Optional[str] = None):

        super().__init__()
        self.stacks = stacks
        self.spacing = spacing
        self.padding = padding
        self.bordercolor = bordercolor
        self.borderwidth = borderwidth
        self.background = background

    def draw(self, parent: tk.Widget):
        frame = tk.Frame(parent)
        frame.config(
            highlightbackground=self.bordercolor,
            highlightthickness=self.borderwidth
        )
        if self.background:
            frame.config(bg=self.background)
        frame.pack(padx=self.padding, fill=tk.X, expand=True, anchor=tk.NW)

        # 子要素も描画
        for i, stack in enumerate(self.stacks):
            if stack.background is None:
                stack.background = self.background
            stack.instantiate(frame)
            # stack.frameの下にだけスペースを入れる
            if i < len(self.stacks) - 1:
                stack.frame.pack(pady=(0, self.spacing))

        return frame


class App:
    def __init__(self, title: str, width: int, height: int):
        self.tk = tk.Tk()
        self.tk.title(title)
        self.tk.geometry(f"{width}x{height}")

    def mainloop(self):
        self.tk.mainloop()

    def add(self, child: GameObject):
        child.instantiate(self.tk)


if __name__ == "__main__":
    app = App("Sample", 800, 600)
    component = VStack([
        Text("Hello", borderwidth=1, background="green"),
        Text("World", borderwidth=2),
        Text("Everyone", borderwidth=2),
    ], spacing=10, padding=20, bordercolor="red", borderwidth=2, background="blue")
    # component = Text("Hello")
    app.add(component)
    app.mainloop()
