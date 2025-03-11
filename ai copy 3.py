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
        # Display cards in a grid on the screen  
        card_width = 100  # Assuming width of 100  
        card_height = int(card_width * 7 / 5)  # Height to maintain 7:5 ratio  
        for index, card in enumerate(self.cards):  
            x = (index % 5) * (card_width + 10) + 10  
            y = self.y_offset + (index // 5) * (card_height + 10)  
            pygame.draw.rect(screen, (255, 255, 255), (x, y, card_width, card_height))  # Draw card rectangle  
  
            # Add card name at the top  
            font = pygame.font.Font(None, 24)  
            name_text = font.render(card.name, True, (0, 0, 0))  
            screen.blit(name_text, (x + 5, y + 5))  
  
            # Add health at the top right corner  
            health_text = font.render(f"HP: {card.health}", True, (0, 0, 0))  
            screen.blit(health_text, (x + card_width - 50, y + 5))  
  
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
player_hand = Hand(400)  # Player hand at the bottom  
enemy_hand = Hand(10)    # Enemy hand at the top  
  
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
    screen.fill((0, 0, 0))  # Black background  
  
    # Display the hands  
    enemy_hand.display(screen)  
    player_hand.display(screen)  
  
    # Update the display  
    pygame.display.flip()  
  
pygame.quit()  
