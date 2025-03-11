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
    def __init__(self):  
        self.cards = []  
  
    def add_card(self, card):  
        self.cards.append(card)  
  
    def display(self, screen):  
        # Display cards in a grid on the screen  
        for index, card in enumerate(self.cards):  
            # Simple grid placement  
            x = (index % 5) * 150 + 10  # 5 cards per row  
            y = (index // 5) * 100 + 10  
            pygame.draw.rect(screen, (255, 255, 255), (x, y, 140, 90))  # Draw card rectangle  
            # Add card text  
            font = pygame.font.Font(None, 36)  
            text = font.render(card.name, True, (0, 0, 0))  
            screen.blit(text, (x + 10, y + 30))  
  
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
  
# Create player and enemy hands  
player_hand = Hand()  
enemy_hand = Hand()  
  
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
    player_hand.display(screen)  
    enemy_hand.display(screen)  
  
    # Update the display  
    pygame.display.flip()  
  
pygame.quit()  
