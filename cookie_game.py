import pygame
import random
import math

# ==================== INITIALISIERUNG ====================
pygame.init()

# Bildschirm-Einstellungen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cookie Game - Krümmelmonster")
clock = pygame.time.Clock()

# ==================== FARBEN ====================
HELLBRAUN = (210, 180, 140)  # Start & Game Over Hintergrund
DUNKELBRAUN = (101, 67, 33)  # Punkte auf Cookie
CREMEFARBIG = (240, 230, 210)  # Spielfeld
BLAU = (100, 150, 255)  # Gewonnen Hintergrund
SCHWARZ = (0, 0, 0)
WEISS = (255, 255, 255)

# ==================== SCHRIFTARTEN ====================
font_large = pygame.font.Font(None, 80)
font_medium = pygame.font.Font(None, 40)
font_small = pygame.font.Font(None, 25)

# ==================== KLASSE: KRÜMMELMONSTER ====================
class KrummelMonster:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.size = 30  # Radius in Pixeln
        self.speed = 5
        self.max_size = 80
        self.min_size = 10
    
    def handle_input(self, keys):
        """Krümmelmonster mit Pfeiltasten steuern"""
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed
        
        # Grenzen des Spielfelds
        self.x = max(self.size, min(self.x, SCREEN_WIDTH - self.size))
        self.y = max(self.size, min(self.y, SCREEN_HEIGHT - self.size))
    
    def grow(self):
        """Monster wächst, wenn es den Cookie isst"""
        if self.size < self.max_size:
            self.size += 5
    
    def shrink(self):
        """Monster schrumpft, wenn es Schokolade berührt"""
        if self.size > self.min_size:
            self.size -= 5
    
    def draw(self, surface):
        """Zeichnet das Krümmelmonster als blauen Kreis mit Augen"""
        # Körper (Kreis)
        pygame.draw.circle(surface, (100, 150, 200), (int(self.x), int(self.y)), self.size)
        
        # Augen
        eye_offset = self.size // 3
        eye_size = max(3, self.size // 6)
        pygame.draw.circle(surface, WEISS, (int(self.x - eye_offset), int(self.y - eye_offset // 2)), eye_size)
        pygame.draw.circle(surface, WEISS, (int(self.x + eye_offset), int(self.y - eye_offset // 2)), eye_size)
        
        # Pupillen
        pygame.draw.circle(surface, SCHWARZ, (int(self.x - eye_offset), int(self.y - eye_offset // 2)), eye_size // 2)
        pygame.draw.circle(surface, SCHWARZ, (int(self.x + eye_offset), int(self.y - eye_offset // 2)), eye_size // 2)

# ==================== KLASSE: COOKIE ====================
class Cookie:
    def __init__(self):
        self.x = random.randint(50, SCREEN_WIDTH - 50)
        self.y = random.randint(50, SCREEN_HEIGHT - 50)
        self.size = 15
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.angry = False
        self.angry_counter = 0
        self.angry_duration = 300  # 300 Frames = ~5 Sekunden
        self.chocolate_drops = []
    
    def update(self, monster):
        """Aktualisiert Cookie-Position und Zustände"""
        
        # Normaler Modus: Cookie bewegt sich zufällig
        if not self.angry:
            self.x += self.vx
            self.y += self.vy
            
            # Bouncing an den Rändern
            if self.x - self.size < 0 or self.x + self.size > SCREEN_WIDTH:
                self.vx *= -1
            if self.y - self.size < 0 or self.y + self.size > SCREEN_HEIGHT:
                self.vy *= -1
            
            self.x = max(self.size, min(self.x, SCREEN_WIDTH - self.size))
            self.y = max(self.size, min(self.y, SCREEN_HEIGHT - self.size))
            
            # Zufällig wütend werden
            if random.randint(1, 300) == 1:
                self.angry = True
                self.angry_counter = 0
        
        else:
            # Wütender Modus: Cookie oben, bewegt sich hin und her
            self.y = 40
            self.x += self.vx
            
            if self.x - self.size < 0 or self.x + self.size > SCREEN_WIDTH:
                self.vx *= -1
            
            # Schokoladenstückchen fallen lassen
            if self.angry_counter % 10 == 0:
                self.chocolate_drops.append({
                    'x': self.x,
                    'y': self.y,
                    'vy': random.uniform(1, 3),
                    'vx': random.uniform(-1, 1)
                })
            
            self.angry_counter += 1
            if self.angry_counter >= self.angry_duration:
                self.angry = False
                self.chocolate_drops.clear()
    
    def shrink(self):
        """Cookie schrumpft, wenn Monster ihn isst"""
        if self.size > 5:
            self.size -= 3
    
    def grow(self):
        """Cookie wächst, wenn Monster die Schokolade isst"""
        if self.size < 25:
            self.size += 3
    
    def respawn(self):
        """Cookie erscheint an neuer zufälliger Position"""
        self.x = random.randint(50, SCREEN_WIDTH - 50)
        self.y = random.randint(100, SCREEN_HEIGHT - 100)
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
    
    def draw(self, surface):
        """Zeichnet den Cookie als braunen Kreis mit Punkten (Schokoladenstückchen)"""
        # Cookie-Körper (Kreis)
        pygame.draw.circle(surface, (210, 140, 50), (int(self.x), int(self.y)), self.size)
        
        # Schokoladenstückchen auf dem Cookie
        random.seed(int(self.x) + int(self.y))  # Konsistente Punkte
        for i in range(8):
            angle = (i / 8) * 2 * math.pi
            dot_x = int(self.x + math.cos(angle) * (self.size * 0.7))
            dot_y = int(self.y + math.sin(angle) * (self.size * 0.7))
            pygame.draw.circle(surface, DUNKELBRAUN, (dot_x, dot_y), self.size // 4)
        
        # Wütender Modus: Rote Färbung
        if self.angry:
            pygame.draw.circle(surface, (255, 0, 0), (int(self.x), int(self.y)), self.size, 3)

# ==================== SPIEL-ZUSTÄNDE ====================
class GameState:
    MENU = 1
    PLAYING = 2
    WON = 3
    LOST = 4

# ==================== HILFSFUNKTIONEN ====================
def distance(x1, y1, x2, y2):
    """Berechnet Abstand zwischen zwei Punkten"""
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def draw_cookie_background(surface):
    """Zeichnet hellbrauen Hintergrund mit dunkelbraunen Punkten (Cookie-Muster)"""
    surface.fill(HELLBRAUN)
    
    # Zufällige Punkte zeichnen (wie Schokoladenstückchen auf einem Cookie)
    random.seed(42)  # Konsistente Punkte
    for i in range(30):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        size = random.randint(5, 20)
        pygame.draw.circle(surface, DUNKELBRAUN, (x, y), size)

def draw_menu(surface):
    """Zeichnet den Startbildschirm"""
    draw_cookie_background(surface)
    
    # Titel
    title_text = font_large.render("Cookie", True, DUNKELBRAUN)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    surface.blit(title_text, title_rect)
    
    # Anleitung
    instruction_text = font_small.render("Spiel starten: C/c", True, DUNKELBRAUN)
    instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    surface.blit(instruction_text, instruction_rect)

def draw_game(surface, monster, cookie):
    """Zeichnet das Spielfeld während des Spiels"""
    surface.fill(CREMEFARBIG)
    
    # Krümmelmonster zeichnen
    monster.draw(surface)
    
    # Cookie zeichnen
    cookie.draw(surface)
    
    # Schokoladenstückchen zeichnen
    for drop in cookie.chocolate_drops:
        pygame.draw.circle(surface, DUNKELBRAUN, (int(drop['x']), int(drop['y'])), 5)

def draw_won(surface):
    """Zeichnet den Gewonnen-Bildschirm"""
    surface.fill(BLAU)
    
    # Text
    won_text = font_large.render("Cookie aufgegessen!", True, WEISS)
    won_rect = won_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    surface.blit(won_text, won_rect)
    
    # Anleitung
    instruction_text = font_small.render("Noch einmal Spielen: O/o", True, WEISS)
    instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    surface.blit(instruction_text, instruction_rect)

def draw_lost(surface):
    """Zeichnet den Verloren-Bildschirm"""
    draw_cookie_background(surface)
    
    # Text
    lost_text = font_large.render("Game Over", True, DUNKELBRAUN)
    lost_rect = lost_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    surface.blit(lost_text, lost_rect)
    
    # Anleitung
    instruction_text = font_small.render("Noch einmal Spielen: O/o", True, DUNKELBRAUN)
    instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    surface.blit(instruction_text, instruction_rect)

# ==================== HAUPTSPIEL ====================
def main():
    state = GameState.MENU
    monster = KrummelMonster()
    cookie = Cookie()
    running = True
    
    while running:
        clock.tick(60)  # 60 FPS
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                # Menü-Eingaben
                if state == GameState.MENU:
                    if event.key in [pygame.K_c]:
                        state = GameState.PLAYING
                        monster = KrummelMonster()
                        cookie = Cookie()
                
                # Nach Spiel beendet
                if state in [GameState.WON, GameState.LOST]:
                    if event.key in [pygame.K_o]:
                        state = GameState.MENU
        
        # Spiellogik
        if state == GameState.PLAYING:
            keys = pygame.key.get_pressed()
            monster.handle_input(keys)
            cookie.update(monster)
            
            # Kollision: Monster isst Cookie
            dist = distance(monster.x, monster.y, cookie.x, cookie.y)
            if dist < monster.size + cookie.size:
                monster.grow()
                cookie.shrink()
                cookie.respawn()
                
                # Gewonnen: Cookie komplett aufgegessen
                if cookie.size <= 5:
                    state = GameState.WON
            
            # Kollision: Monster berührt Schokolade
            for drop in cookie.chocolate_drops[:]:
                dist = distance(monster.x, monster.y, drop['x'], drop['y'])
                if dist < monster.size + 5:
                    monster.shrink()
                    cookie.grow()
                    cookie.chocolate_drops.remove(drop)
                
                # Verloren: Monster komplett aufgegessen
                if monster.size <= 10:
                    state = GameState.LOST
                
                # Schokolade fällt nach unten
                drop['y'] += drop['vy']
                drop['x'] += drop['vx']
                
                # Entfernen wenn aus dem Bildschirm
                if drop['y'] > SCREEN_HEIGHT:
                    cookie.chocolate_drops.remove(drop)
        
        # Zeichnen
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

# ==================== SPIEL STARTEN ====================
if __name__ == "__main__":
    main()
