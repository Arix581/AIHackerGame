import pygame
import random
  
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
  
class Hand:  
    def __init__(self, y_offset):  
        self.cards = []  
        self.y_offset = y_offset  
  
    def add_card(self, card):  
        self.cards.append(card)  
  
    def display(self, screen):  
        card_width = 125  
        card_height = int(card_width * 7 / 5)  
        font = pygame.font.Font(None, 24)  
          
        for index, card in enumerate(self.cards):  
            x = (index % 5) * (card_width + 10) + 10  
            y = self.y_offset + (index // 5) * (card_height + 10)  
            pygame.draw.rect(screen, (255, 255, 255), (x, y, card_width, card_height))  
  
            # Add health at the top right corner  
            health_text = font.render(f"HP: {card.health}", True, (0, 0, 0))  
            screen.blit(health_text, (x + card_width - 50, y + 5))  
  
            # Add and center card name  
            self.render_text_centered(screen, card.name, font, x, y, card_width, card_height)  
  
    def render_text_centered(self, screen, text, font, x, y, card_width, card_height):  
        words = text.split(' ')  
        lines = []  
        current_line = words[0]  
  
        for word in words[1:]:  
            if font.size(current_line + ' ' + word)[0] < card_width - 10:  
                current_line += ' ' + word  
            else:  
                lines.append(current_line)  
                current_line = word  
        lines.append(current_line)  
  
        for i, line in enumerate(lines):  
            text_surface = font.render(line, True, (0, 0, 0))  
            text_width, text_height = text_surface.get_size()  
            line_x = x + (card_width - text_width) // 2  
            line_y = y + (card_height // 2) - (len(lines) * text_height // 2) + (i * text_height)  
            screen.blit(text_surface, (line_x, line_y))  
  
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
        self.rounds = 3  
        self.current_round = 0  
        self.selected_card = None  
  
    def draw_hand(self):  
        self.player_hand.cards = []  
        for _ in range(min(5, len(self.deck.cards))):  
            self.player_hand.add_card(self.deck.cards.pop(0))  
  
    def attack(self, target_card):  
        if self.selected_card and isinstance(self.selected_card, Virus):  
            target_card.health -= self.selected_card.damage  
            self.player_hand.cards.remove(self.selected_card)  
            self.selected_card = None  
  
    def game_loop(self):  
        running = True  
        while running:  
            for event in pygame.event.get():  
                if event.type == pygame.QUIT:  
                    running = False  
                elif event.type == pygame.MOUSEBUTTONDOWN:  
                    mouse_pos = pygame.mouse.get_pos()  
                    self.handle_click(mouse_pos)  
  
            # Fill the screen with a color  
            screen.fill((0, 0, 0))  
  
            # Display the hands  
            self.enemy_hand.display(screen)  
            self.player_hand.display(screen)  
            self.deck.display(screen, screen_width, screen_height)  
  
            # Update the display  
            pygame.display.flip()  
  
    def handle_click(self, mouse_pos):  
        # Check for card selection and attack logic  
        for card in self.player_hand.cards:  
            if self.is_card_clicked(card, mouse_pos):  
                self.selected_card = card  
        for card in self.enemy_hand.cards:  
            if self.is_card_clicked(card, mouse_pos) and self.selected_card:  
                self.attack(card)  
                if card.health <= 0:  
                    self.enemy_hand.cards.remove(card)  
  
    def is_card_clicked(self, card, mouse_pos):  
        card_width = 125  
        card_height = int(card_width * 7 / 5)  
        index = self.player_hand.cards.index(card)  
        x = (index % 5) * (card_width + 10) + 10  
        y = self.player_hand.y_offset + (index // 5) * (card_height + 10)  
        return x <= mouse_pos[0] <= x + card_width and y <= mouse_pos[1] <= y + card_height  
  
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
  
# Add firewall cards to the enemy's hand  
game.enemy_hand.add_card(Firewall("Basic Firewall", 10))  
game.enemy_hand.add_card(Firewall("Advanced Firewall", 15))  
  
random.shuffle(game.deck.cards)  
game.draw_hand()  
  
# Run the game loop  
game.game_loop()  
  
pygame.quit()