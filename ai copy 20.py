import pygame  
import random  
from copy import deepcopy  
  
# Card class to define general card attributes  
class Card:  
    def __init__(self, name, health, damage):  
        self.name = name  
        self.health = health  
        self.damage = damage  
  
# Specific card types: Firewall and Virus  
class Firewall(Card):  
    def __init__(self, name, health):  
        super().__init__(name, health, damage=0)  
  
class Virus(Card):  
    def __init__(self, name, damage):  
        super().__init__(name, health=0, damage=damage)  
  
# Hand class to manage player's and enemy's cards  
class Hand:  
    def __init__(self, y_offset):  
        self.cards = []  
        self.y_offset = y_offset  
  
    def add_card(self, card):  
        self.cards.append(card)  
  
    def display(self, screen, draw_card_func):  
        card_width = 125  
        card_height = int(card_width * 7 / 5)  
          
        for index, card in enumerate(self.cards):  
            x = (index % 5) * (card_width + 10) + 10  
            y = self.y_offset + (index // 5) * (card_height + 10)  
            draw_card_func(screen, card, x, y)   
  
# Deck class to manage the collection of cards  
class Deck:  
    def __init__(self):  
        self.cards = [] 
    
    def add_card(self, card):  
        self.cards.append(card)  
  
    def display(self, screen, screen_width, screen_height):  
        card_width = 125  
        card_height = int(card_width * 7 / 5)  
        x = screen_width - card_width - 40  
        y = screen_height - card_height - 60  
        overlap = 10  
  
        for _ in range(min(3, len(self.cards))):  # Display top 3 cards  
            pygame.draw.rect(screen, (200, 200, 200), (x, y, card_width, card_height))  
            y -= overlap  # Overlap cards slightly  
  
# Main game class  
class Game:  
    def __init__(self):  
        self.player_hand = Hand(400)  
        self.enemy_hand = Hand(10)  
        self.deck = Deck()  
        self.discard_pile = []  
        self.redraws_left = 3  
        self.available_hands = 3  
        self.selected_cards = []  # List for multiple selections  
        self.battle_won = False  
        self.current_round = 1  
        self.game_over = False  
          
        # Virus pool with various viruses  
        self.virus_pool = [  
            Virus("Trojan Virus", 5),  
            Virus("Worm Virus", 3),  
            Virus("Spyware Virus", 4),  
            Virus("Rootkit Virus", 6),  
            Virus("Ransomware Virus", 8),  
            Virus("Adware Virus", 2),  
            Virus("Malware Virus", 7),  
            Virus("Backdoor Virus", 5),  
            Virus("Keylogger Virus", 4),  
            Virus("Phishing Virus", 3)  
        ]  
        self.selected_viruses = []  
  
    def draw_hand(self):  
        self.player_hand.cards = []  
        while len(self.player_hand.cards) < 5 and (self.deck.cards or self.discard_pile):  
            if not self.deck.cards:  
                self.reshuffle_discard_into_deck()  
            if self.deck.cards:  
                self.player_hand.add_card(self.deck.cards.pop(0))  
  
        # Check for failure state right after drawing  
        if not self.deck.cards and not self.player_hand.cards and self.available_hands == 0:  
            self.game_over = True  
  
    def reshuffle_discard_into_deck(self):  
        print("Reshuffling discard pile into deck...")  
        self.deck.cards.extend(self.discard_pile)  
        random.shuffle(self.deck.cards)  
        self.discard_pile.clear()  
  
    def attack(self, target_card):  
        for selected_card in self.selected_cards:  
            if isinstance(selected_card, Virus):  
                target_card.health -= selected_card.damage  
                self.discard_pile.append(selected_card)  
                self.player_hand.cards.remove(selected_card)  
  
        # Clear selected cards after attack  
        self.selected_cards.clear()  
  
        # Check if the target card is defeated  
        if target_card.health <= 0:  
            self.enemy_hand.cards.remove(target_card)  
  
        # Check if the enemy has been defeated  
        if not self.enemy_hand.cards:  
            self.battle_won = True  
  
        # Check if the player's hand is empty  
        if not self.player_hand.cards and self.redraws_left > 0:  
            self.redraw_hand() 
        elif not self.battle_won and not self.player_hand.cards and self.redraws_left <= 0:
            self.game_over = True 
  
    def redraw_hand(self):  
        if self.redraws_left > 0:  
            self.redraws_left -= 1  
            self.draw_hand()  
        elif self.available_hands > 0:  
            self.available_hands -= 1  
            self.draw_hand()  
  
        # Check for failure state  
        if self.redraws_left == 0 and not self.player_hand.cards:  
            self.game_over = True  
  
    def game_loop(self):  
        running = True  
        while running:  
            for event in pygame.event.get():  
                if event.type == pygame.QUIT:  
                    running = False  
                elif event.type == pygame.MOUSEBUTTONDOWN:  
                    if self.game_over:  
                        self.reset_game()  
                    else:  
                        mouse_pos = pygame.mouse.get_pos()  
                        if self.battle_won:  
                            self.handle_virus_selection(mouse_pos)  
                        else:  
                            self.handle_click(mouse_pos)  
  
            screen.fill((0, 0, 0))  
  
            if self.game_over:  
                self.display_failure_message(screen)  
            elif self.battle_won:  
                self.display_battle_win_screen(screen)  
            else:  
                self.enemy_hand.display(screen, self.draw_card)  
                self.player_hand.display(screen, self.draw_card)  
                self.deck.display(screen, screen_width, screen_height)  
                self.display_card_counts(screen)  
  
            pygame.display.flip() 
  
    def handle_click(self, mouse_pos):  
        for card in self.player_hand.cards:  
            if self.is_card_clicked(card, mouse_pos, self.player_hand):  
                # Toggle selection  
                if card in self.selected_cards:  
                    self.selected_cards.remove(card)  
                else:  
                    self.selected_cards.append(card)  
        for card in self.enemy_hand.cards:  
            if self.is_card_clicked(card, mouse_pos, self.enemy_hand) and self.selected_cards:  
                self.attack(card)  
  
    def is_card_clicked(self, card, mouse_pos, hand):  
        card_width = 125  
        card_height = int(card_width * 7 / 5)  
        index = hand.cards.index(card)  
        x = (index % 5) * (card_width + 10) + 10  
        y = hand.y_offset + (index // 5) * (card_height + 10)  
        return x <= mouse_pos[0] <= x + card_width and y <= mouse_pos[1] <= y + card_height  
  
    def draw_card(self, screen, card, x, y):  
        card_width = 125  
        card_height = int(card_width * 7 / 5)  
          
        # Change color for selected cards  
        color = (68, 133, 68) if card in self.selected_cards else (255, 255, 255)  
        pygame.draw.rect(screen, color, (x, y, card_width, card_height))  
          
        font = pygame.font.Font(None, 24)  
  
        # Center card name vertically  
        name_text = font.render(card.name, True, (0, 0, 0))  
        name_text_height = name_text.get_height()  
        screen.blit(name_text, (x + (card_width - name_text.get_width()) // 2, y + (card_height - name_text_height) // 2))  
  
        # Draw health if applicable  
        if card.health:  
            health_text = font.render(f"HP: {card.health}", True, (0, 0, 0))  
            screen.blit(health_text, (x + card_width - 50, y + 5))  
  
        # Draw damage  
        damage_text = font.render(f"DMG: {card.damage}", True, (0, 0, 0))  
        screen.blit(damage_text, (x + (card_width - damage_text.get_width()) // 2, y + card_height - 25))  
  
    def display_battle_win_screen(self, screen):  
        font = pygame.font.Font(None, 36)  
        text = font.render("Choose a Virus to Add to Your Deck", True, (255, 255, 255))  
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, 50))  
        for i, virus in enumerate(self.selected_viruses):  
            x = 150 * i + 100  
            y = screen_height // 2 - (int(125 * 7 / 5)) // 2  
            self.draw_card(screen, virus, x, y)  
  
    def handle_virus_selection(self, mouse_pos):  
        card_width = 125  
        card_height = int(card_width * 7 / 5)  
        for i, virus in enumerate(self.selected_viruses):  
            x = 150 * i + 100  
            y = screen_height // 2 - card_height // 2  
            if x <= mouse_pos[0] <= x + card_width and y <= mouse_pos[1] <= y + card_height:  
                self.deck.add_card(virus)  
                self.battle_won = False  
                self.start_new_battle()  
                print(f"Added {virus.name} to your deck!")  
  
    def start_new_battle(self):  
        self.enemy_hand = Hand(10)  
          
        # Define difficulty levels  
        easy_firewalls = [Firewall("Basic Firewall", 10)]  
        medium_firewalls = [Firewall("Advanced Firewall", 15)]  
        hard_firewalls = [Firewall("Shielded Firewall", 20), Firewall("Fortified Firewall", 25)]  
  
        # Adjust difficulty based on the round  
        if self.current_round <= 2:  
            chosen_firewalls = easy_firewalls  
        elif self.current_round <= 4:  
            chosen_firewalls = medium_firewalls  
        else:  
            chosen_firewalls = hard_firewalls  
  
        # Randomize the number of firewalls and select from chosen difficulty  
        num_firewalls = random.randint(2, 4)  
        for _ in range(num_firewalls):  
            firewall = deepcopy(random.choice(chosen_firewalls))  
            self.enemy_hand.add_card(firewall)  
  
        # Reset player hand, redraws, and deck  
        self.redraws_left = 3  
        self.available_hands = 3  
        self.deck.cards.extend(self.player_hand.cards)  
        self.player_hand.cards.clear()  
        self.deck.cards.extend(self.discard_pile)  
        random.shuffle(self.deck.cards)  
        self.discard_pile.clear()  
        self.draw_hand()  
          
        # Select three random viruses for reward  
        self.selected_viruses = random.sample(self.virus_pool, 3)  
          
        # Increase round count for next battle  
        self.current_round += 1  
  
    def display_card_counts(self, screen):  
        font = pygame.font.Font(None, 24)  
        discard_count = len(self.discard_pile)  
        deck_count = len(self.deck.cards)  
        hand_count = len(self.player_hand.cards)  
        redraws_text = f"Redraws: {self.redraws_left}"  
  
        discard_text = font.render(f"Discard: {discard_count}", True, (255, 255, 255))  
        deck_text = font.render(f"Deck: {deck_count}/{deck_count + discard_count + hand_count}", True, (255, 255, 255))  
        hand_text = font.render(f"Hand: {hand_count}/5", True, (255, 255, 255))  
        redraws_text = font.render(redraws_text, True, (255, 255, 255))  
  
        # Positioning in the top right corner  
        screen.blit(discard_text, (screen_width - discard_text.get_width() - 10, 10))  
        screen.blit(deck_text, (screen_width - deck_text.get_width() - 10, 40))  
        screen.blit(hand_text, (screen_width - hand_text.get_width() - 10, 70))  
        screen.blit(redraws_text, (screen_width - redraws_text.get_width() - 10, 100))  
  
    def display_failure_message(self, screen):  
        font_large = pygame.font.Font(None, 72)  
        font_small = pygame.font.Font(None, 36)  
  
        access_denied_text = font_large.render("[ACCESS DENIED]", True, (255, 0, 0))  
        retry_text = font_small.render("You lose. Try again?", True, (255, 255, 255))  
  
        screen.blit(access_denied_text, (screen_width // 2 - access_denied_text.get_width() // 2, screen_height // 2 - 40))  
        screen.blit(retry_text, (screen_width // 2 - retry_text.get_width() // 2, screen_height // 2 + 40))   
  
    def reset_game(self):  
        # Reset the game state to start over  
        self.__init__()  
        self.start_new_battle()  
  
# Initialize Pygame  
pygame.init()  
  
# Set up the game window  
screen_width = 800  
screen_height = 600  
screen = pygame.display.set_mode((screen_width, screen_height))  
pygame.display.set_caption("Roguelike Adventure")  
  
# Initialize the game  
game = Game()  
# Only add virus cards to the player's deck  
game.deck.add_card(Virus("Trojan Virus", 5))  
game.deck.add_card(Virus("Worm Virus", 3))  
game.deck.add_card(Virus("Spyware Virus", 4))  
  
# Add initial firewall cards to the enemy's hand  
game.start_new_battle()  
  
# Run the game loop  
game.game_loop()  
  
pygame.quit()  
