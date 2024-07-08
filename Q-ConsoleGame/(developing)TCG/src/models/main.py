class Card:
    def __init__(self, name: str, attack: int, defense: int, detail: str):
        self.name: str = name
        self.attack: int = attack
        self.defense: int = defense
        self.detail: str = detail

    def __str__(self):
        return f"{self['name']} (ATK: {self['attack']}, DEF: {self['defense']})"

    def __repr__(self):
        return f"{self['name']} (ATK: {self['attack']}, DEF: {self['defense']})"


class Player:
    def __init__(self, name: str, deck: list[Card], hand: list[Card]):
        self.name: str = name
        self.deck: list[Card] = deck
        self.hand: list[Card] = hand


class Field:
    def __init__(self, player1: Player, player2: Player):
        self.player1: Player = player1
        self.player2: Player = player2
        self.current_player: Player = player1

    def next_turn(self):
        self.current_player = self.player1 if self.current_player == self.player2 else self.player2
