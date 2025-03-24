import random
import numpy as np

class PaintTerritoryGame:
    def __init__(self, board_height=9, board_width=10, max_turns=20):
        # Game board initialization
        self.board = np.zeros((board_height, board_width), dtype=int)
        
        # Teams: 0 for α team (α-チーム), 1 for β team (β-チーム)
        self.current_turn = 0
        
        # Game decks for movement cards
        self.alpha_deck = []
        self.beta_deck = []
        
        # Game parameters
        self.max_turns = max_turns
        self.current_game_turn = 0
        
        # Team scores and player positions
        self.alpha_score = 0
        self.beta_score = 0
        self.alpha_position = [0, 0]  # Starting position for α team
        self.beta_position = [board_height-1, board_width-1]  # Starting position for β team
        
        # Initialize decks with random movement cards
        self._generate_initial_decks()
    
    def _generate_initial_decks(self):
        """Generate initial movement cards for both teams"""
        movements = [
            (1, 0),   # Move down
            (-1, 0),  # Move up
            (0, 1),   # Move right
            (0, -1),  # Move left
            (1, 1),   # Diagonal down-right
            (1, -1),  # Diagonal down-left
            (-1, 1),  # Diagonal up-right
            (-1, -1)  # Diagonal up-left
        ]
        
        # Generate 10 random movement cards for each team
        for _ in range(10):
            self.alpha_deck.append(random.choice(movements))
            self.beta_deck.append(random.choice(movements))
    
    def is_valid_move(self, team, card):
        """Check if the proposed move is valid"""
        current_pos = self.alpha_position if team == 0 else self.beta_position
        new_pos = [current_pos[0] + card[0], current_pos[1] + card[1]]
        
        # Check board boundaries
        if (0 <= new_pos[0] < self.board.shape[0] and 
            0 <= new_pos[1] < self.board.shape[1]):
            return True
        return False
    
    def move(self, team, card_index):
        """Execute a move for the given team"""
        # Select the appropriate deck and position based on the team
        deck = self.alpha_deck if team == 0 else self.beta_deck
        current_pos = self.alpha_position if team == 0 else self.beta_position
        
        # Validate the move
        card = deck[card_index]
        if not self.is_valid_move(team, card):
            print(f"Invalid move for {'α' if team == 0 else 'β'} team!")
            return False
        
        # Move the player
        new_pos = [current_pos[0] + card[0], current_pos[1] + card[1]]
        
        # Paint the territory
        if self.board[new_pos[0], new_pos[1]] == 0 or \
           self.board[new_pos[0], new_pos[1]] != team + 1:
            self.board[new_pos[0], new_pos[1]] = team + 1
        
        # Update player position
        if team == 0:
            self.alpha_position = new_pos
        else:
            self.beta_position = new_pos
        
        # Remove the used card from the deck
        deck.pop(card_index)
        
        return True
    
    def calculate_scores(self):
        """Calculate territories for each team"""
        self.alpha_score = np.count_nonzero(self.board == 1)
        self.beta_score = np.count_nonzero(self.board == 2)
    
    def play_turn(self):
        """Play a single turn of the game"""
        if self.current_game_turn >= self.max_turns:
            print("Game Over!")
            self.calculate_scores()
            return False
        
        # Randomly select a card for the current team
        card_index = random.randint(0, len(self.alpha_deck if self.current_turn == 0 else self.beta_deck) - 1)
        
        # Attempt to move
        if self.move(self.current_turn, card_index):
            # Switch turns
            self.current_turn = 1 - self.current_turn
            self.current_game_turn += 1
        
        return True
    
    def play_game(self):
        """Play the entire game"""
        while self.play_turn():
            pass
        
        # Display final results
        print(f"α Team Score: {self.alpha_score}")
        print(f"β Team Score: {self.beta_score}")
        
        if self.alpha_score > self.beta_score:
            print("α Team Wins!")
        elif self.beta_score > self.alpha_score:
            print("β Team Wins!")
        else:
            print("It's a Draw!")
        
        return self.board
    
    def display_board(self):
        """Display the current game board"""
        for row in self.board:
            print(' '.join(['.' if x == 0 else ('α' if x == 1 else 'β') for x in row]))
        print("\n")

# Example of how to run the game
def main():
    game = PaintTerritoryGame(max_turns=20)
    final_board = game.play_game()

if __name__ == "__main__":
    main()
