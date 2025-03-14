import pygame
import random
from copy import deepcopy  
  
# Classes for Card, Firewall, and Virus  
class Card:  
    def __init__(self, name, health, damage):  
        self.name = name  
        self.health = health  
        self.damage = damage  
  
class Firewall(Card):  
    def __init__(self, name, health):  
        super().__init__(name, health, damage=0)  
  
class Virus(Card):  
    def __init__(self, name, damage):  
        super().__init__(name, health=0, damage=damage)  
 
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

class Game:  
    def __init__(self):  
        self.player_hand = Hand(400)  
        self.enemy_hand = Hand(10)  
        self.deck = Deck()  
        self.discard_pile = []  
        self.redraws_left = 3  
        self.available_hands = 3  
        self.selected_card = None  
        self.virus_pool = [Virus("Trojan Virus", 5), Virus("Worm Virus", 3), Virus("Spyware Virus", 4)]  
        self.firewall_pool = [  
            Firewall("Basic Firewall", 10),  
            Firewall("Advanced Firewall", 15),  
            Firewall("Shielded Firewall", 10),  
            Firewall("Fortified Firewall", 10)  
        ]  
        self.battle_won = False  
  
    def draw_hand(self):  
        self.player_hand.cards = []  
        while len(self.player_hand.cards) < 5 and (self.deck.cards or self.discard_pile):  
            if not self.deck.cards:  
                self.reshuffle_discard_into_deck()  
            if self.deck.cards:  
                self.player_hand.add_card(self.deck.cards.pop(0))  
  
    def reshuffle_discard_into_deck(self):  
        print("Reshuffling discard pile into deck...")  
        self.deck.cards.extend(self.discard_pile)  
        random.shuffle(self.deck.cards)  
        self.discard_pile.clear()  
  
    def attack(self, target_card):  
        if self.selected_card and isinstance(self.selected_card, Virus):  
            target_card.health -= self.selected_card.damage  
            self.discard_pile.append(self.selected_card)  
            self.player_hand.cards.remove(self.selected_card)  
            self.selected_card = None  
  
            # Check if the target card is defeated  
            if target_card.health <= 0:  
                self.enemy_hand.cards.remove(target_card)  
  
            # Check if the enemy has been defeated  
            if not self.enemy_hand.cards:  
                self.battle_won = True  
  
            # Check if the player's hand is empty  
            if not self.player_hand.cards and self.redraws_left > 0:  
                self.redraw_hand()  
  
    def redraw_hand(self):  
        if self.redraws_left > 0:  
            self.redraws_left -= 1  
            print(f"Redrawing hand... Redraws left: {self.redraws_left}")  
            self.draw_hand()  
  
    def game_loop(self):  
        running = True  
        while running:  
            for event in pygame.event.get():  
                if event.type == pygame.QUIT:  
                    running = False  
                elif event.type == pygame.MOUSEBUTTONDOWN:  
                    mouse_pos = pygame.mouse.get_pos()  
                    if self.battle_won:  
                        self.handle_virus_selection(mouse_pos)  
                    else:  
                        self.handle_click(mouse_pos)  
  
            # Fill the screen with a color  
            screen.fill((0, 0, 0))  
  
            if self.battle_won:  
                self.display_battle_win_screen(screen)  
            else:  
                # Display the hands  
                self.enemy_hand.display(screen, self.draw_card)  
                self.player_hand.display(screen, self.draw_card)  
                self.deck.display(screen, screen_width, screen_height)  
  
            # Update the display  
            pygame.display.flip()  
  
    def handle_click(self, mouse_pos):  
        for card in self.player_hand.cards:  
            if self.is_card_clicked(card, mouse_pos, self.player_hand):  
                self.selected_card = card  
        for card in self.enemy_hand.cards:  
            if self.is_card_clicked(card, mouse_pos, self.enemy_hand) and self.selected_card:  
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
        pygame.draw.rect(screen, (255, 255, 255), (x, y, card_width, card_height))  
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
        for i, virus in enumerate(self.virus_pool):  
            x = 150 * i + 100  
            y = screen_height // 2 - (int(125 * 7 / 5)) // 2  
            self.draw_card(screen, virus, x, y)  
  
    def handle_virus_selection(self, mouse_pos):  
        card_width = 125  
        card_height = int(card_width * 7 / 5)  
        for i, virus in enumerate(self.virus_pool):  
            x = 150 * i + 100  
            y = screen_height // 2 - card_height // 2  
            if x <= mouse_pos[0] <= x + card_width and y <= mouse_pos[1] <= y + card_height:  
                self.deck.add_card(virus)  
                self.battle_won = False  
                self.start_new_battle()  
                print(f"Added {virus.name} to your deck!")  
  
    def start_new_battle(self):  
        # Reset enemy hand with new random firewalls  
        self.enemy_hand = Hand(10)  
        num_firewalls = random.randint(2, 4)  # Randomize the number of firewalls  
        for _ in range(num_firewalls):  
            firewall = deepcopy(random.choice(self.firewall_pool))  # Use deepcopy to ensure distinct instances  
            self.enemy_hand.add_card(firewall)  
  
        # Reset player hand, redraws, and deck  
        self.redraws_left = 3  
        self.available_hands = 3  
        # Shuffle player's current hand back into the deck  
        self.deck.cards.extend(self.player_hand.cards)  
        self.player_hand.cards.clear()  
        # Shuffle the discard pile into the deck  
        self.deck.cards.extend(self.discard_pile)  
        random.shuffle(self.deck.cards)  
        self.discard_pile.clear()  
        self.draw_hand()  
  
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
