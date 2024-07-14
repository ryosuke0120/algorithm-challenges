import tkinter as tk

class App:
    def __init__(self, title="App", width=800, height=600):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(f"{width}x{height}")
        self.canvases = {}
        self.current_canvas = None
        self.width = width
        self.height = height

    def register_canvas(self, name, spacing=0, stack='v'):
        canvas = CustomCanvas(self.root, self.width, self.height, spacing, stack)
        self.canvases[name] = canvas
        return canvas

    def switch_to(self, name):
        if self.current_canvas:
            self.current_canvas.pack_forget()
        self.current_canvas = self.canvases[name]
        self.current_canvas.pack(fill=tk.BOTH, expand=True)

    def run(self, initial_canvas):
        self.switch_to(initial_canvas)
        self.root.mainloop()

    def quit(self):
        self.root.quit()


class CustomCanvas(tk.Canvas):
    def __init__(self, parent, width, height, spacing, stack):
        super().__init__(parent, width=width, height=height, bg='white')
        self.pack_propagate(0)
        self.spacing = spacing
        self.stack = stack
        self.items = []

    def add(self, name, text="", action=None, font=("Helvetica", 12), fg="black", bg="white", **kwargs):
        item = CustomItem(self, name, text, action, font, fg, bg, **kwargs)
        self.items.append(item)
        self._rearrange()
        return item

    def _rearrange(self):
        x, y = 10, 10
        for item in self.items:
            if self.stack == 'v':
                item.place(x, y)
                y += item.height + self.spacing
            else:
                item.place(x, y)
                x += item.width + self.spacing

class CustomItem:
    def __init__(self, canvas, name, text, action, font, fg, bg, **kwargs):
        self.canvas = canvas
        self.name = name
        self.text = text
        self.action = action
        self.font = font
        self.fg = fg
        self.bg = bg
        self.kwargs = kwargs
        self.width = kwargs.get('width', 100)
        self.height = kwargs.get('height', 50)

        self.rect = self.canvas.create_rectangle(0, 0, self.width, self.height, fill=self.bg, outline='')
        self.text_id = self.canvas.create_text(self.width//2, self.height//2, text=self.text, font=self.font, fill=self.fg)
        if self.action:
            self.canvas.tag_bind(self.rect, "<Button-1>", lambda e: self.action())
            self.canvas.tag_bind(self.text_id, "<Button-1>", lambda e: self.action())

    def place(self, x, y):
        self.canvas.coords(self.rect, x, y, x+self.width, y+self.height)
        self.canvas.coords(self.text_id, x+self.width//2, y+self.height//2)


if __name__ == "__main__":
    app = App(title="Poker Game", width=800, height=600)

    # -------------------------
    # メイン画面
    # -------------------------
    canvas = app.register_canvas("main", spacing=10)

    # ボタンを設定(actionが設定されていると、自動的にボタンになる)
    canvas.add("play", text="Poker Game", action=lambda: app.switch_to("game"), font=("Helvetica", 24))
    canvas.add("go", text="Settings", action=lambda: app.switch_to("settings"))
    canvas.add("quit", text="Exit", action=app.quit)

    # -------------------------
    # ゲーム画面
    # -------------------------
    canvas = app.register_canvas("game", stack="h")

    # 1. インフォメーション(textやfontのみだと、自動的にLabelになる)
    info = canvas.add("info", stack="v", spacing=10, width=int(app.width * 0.3))
    info.add("player1", text="Player 1")
    info.add("player2", text="Player 2")
    info.add("turn", text="Turn: 1")
    info.add("phase", text="Phase: Draw")

    # 2. ゲームフィールド
    field = canvas.add("field", stack="v", width=int(app.width * 0.7))
    field.add("field_title", text="ポーカーゲーム", font=("Helvetica", 24), fg="white", bg="black", height=50)

    # 2-A. ボードの詳細
    board = field.add("board", stack="h", bg="green", height=400, spacing=10)

    # 2-B. ボタンの配置
    panel = field.add("panel", stack="v", bg="blue", height=100)
    panel.add("deal", text="Deal Cards", action=lambda: print("Deal Cards"))
    panel.add("back", text="Back to Main Menu", action=lambda: app.switch_to("main"))

    # -------------------------
    # セッティング画面
    # -------------------------
    canvas = app.register_canvas("settings")
    canvas.add("back_to_main", text="Return Main", action=lambda: app.switch_to("main"))

    # 実行
    app.run("main")  # メイン画面を表示
