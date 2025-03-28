import pygame  
  
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
        card_width = 100  
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
  
        # Render lines centered  
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
        card_width = 60  
        card_height = int(card_width * 7 / 5)  
        x = screen_width - card_width - 10  
        y = screen_height - card_height - 10  
        overlap = 10  
  
        for _ in range(min(3, len(self.cards))):  # Display top 3 cards  
            pygame.draw.rect(screen, (200, 200, 200), (x, y, card_width, card_height))  
            y -= overlap  # Overlap cards slightly  
  
# Initialize Pygame  
pygame.init()  
  
# Set up the game window  
screen_width = 800  
screen_height = 600  
screen = pygame.display.set_mode((screen_width, screen_height))  
pygame.display.set_caption("Roguelike Adventure")  
  
# Example cards  
firewall1 = Firewall("Basic Firewall", 10)  
virus1 = Virus("Trojan Virus", 5)  
  
# Create player and enemy hands with different y offsets  
player_hand = Hand(400)  
enemy_hand = Hand(10)  
  
# Create a deck  
deck = Deck()  
deck.add_card(firewall1)  
deck.add_card(virus1)  
deck.add_card(Firewall("Advanced Firewall", 15))  
  
# Add cards to hands  
player_hand.add_card(virus1)  
enemy_hand.add_card(firewall1)  
  
# Run the game loop  
running = True  
while running:  
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            running = False  
  
    # Fill the screen with a color  
    screen.fill((0, 0, 0))  
  
    # Display the hands  
    enemy_hand.display(screen)  
    player_hand.display(screen)  
    deck.display(screen, screen_width, screen_height)  
  
    # Update the display  
    pygame.display.flip()  
  
pygame.quit()  
