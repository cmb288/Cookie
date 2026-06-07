import pygame
import random
import math

pygame.init()

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 900
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cookie Game")
clock = pygame.time.Clock()

HELLBRAUN = (210, 180, 140)
DUNKELBRAUN = (101, 67, 33)
CREMEFARBIG = (240, 230, 210)
DUNKELBLAU = (30, 60, 120)
SCHWARZ = (0, 0, 0)
WEISS = (255, 255, 255)

font_large = pygame.font.Font(None, 100)
font_medium = pygame.font.Font(None, 50)
font_small = pygame.font.Font(None, 28)

# Load images
def load_image(filename, size=None):
    try:
        img = pygame.image.load(filename)
        if size:
            img = pygame.transform.scale(img, size)
        return img
    except:
        return None

class KrummelMonster:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.size = 60
        self.speed = 4
        self.max_size = 140
        self.min_size = 30
        self.base_image = load_image("kruemmelmonster.png", (self.size * 2, self.size * 2))
        self.current_image = self.base_image
    
    def handle_input(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed
        
        self.x = max(self.size, min(self.x, SCREEN_WIDTH - self.size))
        self.y = max(self.size, min(self.y, SCREEN_HEIGHT - self.size))
    
    def grow(self):
        if self.size < self.max_size:
            self.size += 3
            self.update_image()
    
    def shrink(self):
        if self.size > self.min_size:
            self.size -= 3
            self.update_image()
    
    def update_image(self):
        if self.base_image:
            self.current_image = pygame.transform.scale(self.base_image, (self.size * 2, self.size * 2))
    
    def draw(self, surface):
        if self.current_image:
            rect = self.current_image.get_rect(center=(int(self.x), int(self.y)))
            surface.blit(self.current_image, rect)
        else:
            pygame.draw.circle(surface, (100, 150, 200), (int(self.x), int(self.y)), self.size)

class Cookie:
    def __init__(self):
        self.x = random.randint(50, SCREEN_WIDTH - 50)
        self.y = random.randint(100, SCREEN_HEIGHT - 100)
        self.size = 35
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.angry = False
        self.angry_counter = 0
        self.angry_duration = 400
        self.chocolate_drops = []
        self.base_image = load_image("cookie.png", (self.size * 2, self.size * 2))
        self.current_image = self.base_image
    
    def update(self, monster):
        if not self.angry:
            self.x += self.vx
            self.y += self.vy
            
            if self.x - self.size < 0 or self.x + self.size > SCREEN_WIDTH:
                self.vx *= -1
            if self.y - self.size < 20 or self.y + self.size > SCREEN_HEIGHT:
                self.vy *= -1
            
            self.x = max(self.size, min(self.x, SCREEN_WIDTH - self.size))
            self.y = max(self.size, min(self.y, SCREEN_HEIGHT - self.size))
            
            if random.randint(1, 300) == 1:
                self.angry = True
                self.angry_counter = 0
        
        else:
            self.y = 50
            self.x += self.vx * 1.5
            
            if self.x - self.size < 0 or self.x + self.size > SCREEN_WIDTH:
                self.vx *= -1
            
            if self.angry_counter % 8 == 0:
                self.chocolate_drops.append({
                    'x': self.x,
                    'y': self.y,
                    'vy': random.uniform(2, 4),
                    'vx': random.uniform(-2, 2)
                })
            
            self.angry_counter += 1
            if self.angry_counter >= self.angry_duration:
                self.angry = False
                self.chocolate_drops.clear()
    
    def shrink(self):
        if self.size > 12:
            self.size -= 2
            self.update_image()
    
    def grow(self):
        if self.size < 55:
            self.size += 2
            self.update_image()
    
    def update_image(self):
        if self.base_image:
            self.current_image = pygame.transform.scale(self.base_image, (self.size * 2, self.size * 2))
    
    def respawn(self):
        self.x = random.randint(50, SCREEN_WIDTH - 50)
        self.y = random.randint(150, SCREEN_HEIGHT - 100)
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
    
    def draw(self, surface):
        if self.current_image:
            rect = self.current_image.get_rect(center=(int(self.x), int(self.y)))
            surface.blit(self.current_image, rect)
        else:
            pygame.draw.circle(surface, (210, 140, 50), (int(self.x), int(self.y)), self.size)
        
        if self.angry:
            pygame.draw.circle(surface, (255, 0, 0), (int(self.x), int(self.y)), self.size + 5, 3)

class GameState:
    MENU = 1
    PLAYING = 2
    WON = 3
    LOST = 4

def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def draw_cookie_background(surface):
    surface.fill(HELLBRAUN)
    random.seed(42)
    for i in range(30):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        size = random.randint(5, 20)
        pygame.draw.circle(surface, DUNKELBRAUN, (x, y), size)

def draw_menu(surface):
    draw_cookie_background(surface)
    title_text = font_large.render("Cookie", True, DUNKELBRAUN)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    surface.blit(title_text, title_rect)
    instruction_text = font_small.render("Spiel starten: C/c", True, DUNKELBRAUN)
    instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
    surface.blit(instruction_text, instruction_rect)

def draw_game(surface, monster, cookie):
    surface.fill(CREMEFARBIG)
    
    # Draw chocolate drops FIRST (so they don't cover text)
    for drop in cookie.chocolate_drops:
        pygame.draw.circle(surface, DUNKELBRAUN, (int(drop['x']), int(drop['y'])), 8)
    
    # Draw monsters and cookie on top
    monster.draw(surface)
    cookie.draw(surface)

def draw_won(surface):
    surface.fill(DUNKELBLAU)
    won_text = font_large.render("Cookie", True, WEISS)
    won_rect = won_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 - 20))
    surface.blit(won_text, won_rect)
    
    won_text2 = font_medium.render("aufgegessen!", True, WEISS)
    won_rect2 = won_text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 50))
    surface.blit(won_text2, won_rect2)
    
    instruction_text = font_small.render("Noch einmal Spielen: O/o", True, WEISS)
    instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))
    surface.blit(instruction_text, instruction_rect)

def draw_lost(surface):
    draw_cookie_background(surface)
    lost_text = font_large.render("Game", True, DUNKELBRAUN)
    lost_rect = lost_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 - 20))
    surface.blit(lost_text, lost_rect)
    
    lost_text2 = font_medium.render("Over", True, DUNKELBRAUN)
    lost_rect2 = lost_text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 50))
    surface.blit(lost_text2, lost_rect2)
    
    instruction_text = font_small.render("Noch einmal Spielen: O/o", True, DUNKELBRAUN)
    instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))
    surface.blit(instruction_text, instruction_rect)

def main():
    state = GameState.MENU
    monster = KrummelMonster()
    cookie = Cookie()
    running = True
    
    while running:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if state == GameState.MENU:
                    if event.key in [pygame.K_c]:
                        state = GameState.PLAYING
                        monster = KrummelMonster()
                        cookie = Cookie()
                
                if state in [GameState.WON, GameState.LOST]:
                    if event.key in [pygame.K_o]:
                        state = GameState.MENU
        
        if state == GameState.PLAYING:
            keys = pygame.key.get_pressed()
            monster.handle_input(keys)
            cookie.update(monster)
            
            dist = distance(monster.x, monster.y, cookie.x, cookie.y)
            if dist < monster.size + cookie.size:
                monster.grow()
                cookie.shrink()
                cookie.respawn()
                
                if cookie.size <= 12:
                    state = GameState.WON
            
            for drop in cookie.chocolate_drops[:]:
                dist = distance(monster.x, monster.y, drop['x'], drop['y'])
                if dist < monster.size + 8:
                    monster.shrink()
                    cookie.grow()
                    cookie.chocolate_drops.remove(drop)
                
                if monster.size <= 30:
                    state = GameState.LOST
                
                drop['y'] += drop['vy']
                drop['x'] += drop['vx']
                
                if drop['y'] > SCREEN_HEIGHT:
                    cookie.chocolate_drops.remove(drop)
        
        if state == GameState.MENU:
            draw_menu(screen)
        elif state == GameState.PLAYING:
            draw_game(screen, monster, cookie)
        elif state == GameState.WON:
            draw_won(screen)
        elif state == GameState.LOST:
            draw_lost(screen)
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()
