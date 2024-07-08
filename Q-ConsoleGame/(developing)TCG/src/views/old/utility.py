import tkinter as tk
from typing import Literal

Alignment = Literal[
    "top", "bottom", "left", "right", "center",
    "top-left", "top-right", "bottom-left", "bottom-right"]


class Component:
    def __init__(self):
        self.frame = tk.Frame()
        self.component = None

    def hide(self):
        self.frame.pack_forget()
        return self

    def show(self):
        self.frame.pack(fill=tk.BOTH, expand=True)
        return self

    def add(self, component):
        self.frame.pack(fill=tk.BOTH, expand=True)
        component.show()
        return self


class Text(Component):
    def __init__(self, text: str):
        self.parent = None
        self.component = None
        self.text = text

    def font(self, font: str):
        self.component.config(font=font)
        return self

    def color(self, color: str):
        self.component.config(fg=color)
        return self

    def wrap(self, length: int):
        self.component.config(wraplength=length)
        return self

    def align(self, alignment: Alignment):
        self.component.config(anchor=alignment)
        return self

    def show(self, parent):
        self.component = tk.Label(parent, text=self.text)



# デフォルトでfitするようになる。ただし大きさが指定されている場合はその大きさになる
# Spacer：これを追加すると、fitでなく途中でサイズが切られる
class Stack(Component):

    def __init__(self, stacks: list):
        super().__init__()
        self.stacks = stacks

    def border(self, color, width):
        """枠線の色と太さを設定"""
        self.frame.config(bd=width, relief="solid", bordercolor=color)
        return self

    def spacing(self, value):
        """上下の間隔を設定"""
        self.frame.pack(pady=value)
        return self

    def padding(self, value):
        """余白を設定"""
        self.frame.pack(padx=value)
        return self

    def background(self, color):
        """背景色を設定"""
        return self


class VStack(Stack):
    def __init__(self, stacks: list):
        super().__init__(stacks)

    def align(self, alignment: Literal["left", "right", "center"]):
        """水平方向の配置を設定"""
        return self

    def show(self):
        # 自分自身を表示
        super().show()

        # 各スタックを表示
        for stack in self.stacks:
            stack.show()
        return self


class HStack(Stack):
    def __init__(self, stacks: list):
        super().__init__(stacks)

    def align(self, alignment: Literal["top", "bottom", "center"]):
        """水平方向の配置を設定"""
        return self


class ZStack(Stack):
    def __init__(self, stacks: list):
        super().__init__(stacks)

    def align(self, alignment: Alignment):
        return self
