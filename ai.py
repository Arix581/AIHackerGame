import pygame  
  
# Initialize Pygame  
pygame.init()  
  
# Set up the game window  
screen_width = 800  
screen_height = 600  
screen = pygame.display.set_mode((screen_width, screen_height))  
pygame.display.set_caption("Roguelike Adventure")  

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
  
# Example cards  
firewall1 = Firewall("Basic Firewall", 10)  
virus1 = Virus("Trojan Virus", 5)  
  
# Example interaction  
def attack(firewall, virus):  
    firewall.health -= virus.damage  
    print(f"{virus.name} attacks {firewall.name}! Remaining health: {firewall.health}")  
  
attack(firewall1, virus1)  

# Run the game loop  
running = True  
while running:  
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            running = False  
  
    # Fill the screen with a color  
    screen.fill((0, 0, 0))  # Black background  
  
    # Update the display  
    pygame.display.flip()  
  
pygame.quit()  
