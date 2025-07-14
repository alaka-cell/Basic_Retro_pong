class GameStateManager:
    def __init__(self):
        self.state = "menu" 
    def is_menu(self):
        return self.state == "menu"

    def is_playing(self):
        return self.state == "playing"

    def is_exploding(self):
        return self.state == "exploding"

    def is_game_over(self):
        return self.state == "game_over"

    def start_game(self):
        self.state = "playing"

    def go_to_menu(self):
        self.state = "menu"

    def explode(self):
        self.state = "exploding"

    def finish_explode(self):
        self.go_to_game_over()  

    def go_to_game_over(self):
        self.state = "game_over"
