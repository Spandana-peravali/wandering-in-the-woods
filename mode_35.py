import random
import pygame
import statistics
import os

# Constants
CELL_SIZE = 80
PANEL_WIDTH = 140
GREEN = (34, 139, 34)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKIN = (255, 224, 189)
SHIRT_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]

def draw_person(surface, center_x, center_y, color):
    pygame.draw.circle(surface, SKIN, (center_x, center_y - 15), 12)
    pygame.draw.line(surface, color, (center_x, center_y - 3), (center_x, center_y + 20), 4)
    pygame.draw.line(surface, color, (center_x - 12, center_y + 2), (center_x + 12, center_y + 2), 4)
    pygame.draw.line(surface, BLACK, (center_x, center_y + 20), (center_x - 10, center_y + 40), 3)
    pygame.draw.line(surface, BLACK, (center_x, center_y + 20), (center_x + 10, center_y + 40), 3)

class Balloon:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vy = random.uniform(-2, -0.5)
        self.vx = random.uniform(-1, 1)
        self.size = random.randint(20, 35)
        self.color = (random.randint(200, 255), random.randint(100, 200), random.randint(100, 200))
        self.life = 120

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        self.vy *= 0.98

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, 
                          (self.x - self.size//2, self.y - self.size//2, self.size, self.size//2))
        pygame.draw.line(screen, BLACK, 
                        (self.x, self.y + self.size//4), 
                        (self.x, self.y + 30), 2)

def save_leaderboard(moves):
    try:
        with open("leaderboard.txt", "a") as f:
            f.write(f"{moves}\n")
    except:
        pass

def load_leaderboard():
    try:
        if os.path.exists("leaderboard.txt"):
            with open("leaderboard.txt", "r") as f:
                scores = [int(line.strip()) for line in f if line.strip().isdigit()]
                return sorted(scores)[:3]
    except:
        pass
    return []

class Button:
    def __init__(self, x, y, w, h, text, color=(100, 150, 255)):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = tuple(min(255, c + 50) for c in color)

    def draw(self, screen, font):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=15)
        pygame.draw.rect(screen, WHITE, self.rect, 3, border_radius=15)
        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def clicked(self):
        return self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]

def run_35():
    pygame.init()
    pygame.mixer.init()

    all_runs = []
    leaderboard = load_leaderboard()
    
    while True:
        # Input validation
        while True:
            try:
                rows = int(input("Enter rows (3-20): "))
                if 3 <= rows <= 20: break
                print("Please enter 3-20")
            except:
                print("Please enter a number")
        
        while True:
            try:
                cols = int(input("Enter columns (3-20): "))
                if 3 <= cols <= 20: break
                print("Please enter 3-20")
            except:
                print("Please enter a number")
        
        while True:
            try:
                num_people = int(input("Number of people (2-4): "))
                if 2 <= num_people <= 4: break
                print("Please enter 2, 3, or 4")
            except:
                print("Please enter a number")
        
        names = []
        for i in range(num_people):
            name = input(f"Name for person {i+1} : ").strip()
            names.append(name[:12] if name else f"Person {i+1}")

        grid_width = cols * CELL_SIZE
        grid_height = rows * CELL_SIZE
        total_width = grid_width + PANEL_WIDTH
        screen = pygame.display.set_mode((total_width, grid_height))
        pygame.display.set_caption("Wandering in the Woods - Grades 3-5")

        moves_font = pygame.font.SysFont(None, 30)
        name_font = pygame.font.SysFont(None, 24)
        button_font = pygame.font.SysFont(None, 28)
        clock = pygame.time.Clock()

        try:
            pygame.mixer.music.load("Game_music.mp3")
            pygame.mixer.music.play(-1)
        except:
            pass

        play_btn = Button(grid_width + 10, 15, 120, 50, "⏸️ PAUSE", (100, 200, 100))
        quit_btn = Button(grid_width + 10, 75, 120, 50, "❌ QUIT", (200, 100, 100))

        positions = [(random.randint(0, cols - 1), random.randint(0, rows - 1)) for _ in range(num_people)]
        move_count = 0
        paused = False
        game_over = False
        balloons = []
        running = True

        while running:
            mouse_clicked = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_clicked = True

            if play_btn.clicked() and mouse_clicked:
                paused = not paused
                play_btn.text = "▶️ PLAY" if paused else "⏸️ PAUSE"
            if quit_btn.clicked() and mouse_clicked:
                running = False

            if game_over:
                screen.fill((255, 255, 200))
                if len(balloons) == 0:
                    balloons = [Balloon(random.randint(0, grid_width), random.randint(grid_height//2, grid_height)) 
                               for _ in range(15)]
                
                for balloon in balloons[:]:
                    balloon.update()
                    if balloon.life > 0:
                        balloon.draw(screen)
                    else:
                        balloons.remove(balloon)

                big_font = pygame.font.SysFont(None, 72)
                vic_text = big_font.render(" THEY MET! ", True, GREEN)
                screen.blit(vic_text, (grid_width//2 - vic_text.get_width()//2, 100))

                if all_runs:
                    stats_font = pygame.font.SysFont(None, 36)
                    stats = [
                        f"Shortest: {min(all_runs)}",
                        f"Longest:  {max(all_runs)}", 
                        f"Average: {statistics.mean(all_runs):.1f}"
                    ]
                    for i, stat in enumerate(stats):
                        screen.blit(stats_font.render(stat, True, BLACK), (50, 250 + i*50))

                inst_font = pygame.font.SysFont(None, 28)
                screen.blit(inst_font.render("SPACE = PLAY AGAIN OR ESC = QUIT", True, BLACK), (50, grid_height - 80))
                
                # Panel during celebration
                pygame.draw.rect(screen, (50, 100, 50), (grid_width, 0, PANEL_WIDTH, grid_height))
                panel_title = pygame.font.SysFont(None, 24).render("CONTROLS", True, WHITE)
                screen.blit(panel_title, (grid_width + 20, 5))
                play_btn.draw(screen, button_font)
                quit_btn.draw(screen, button_font)
                
                pygame.display.flip()
                clock.tick(60)
                continue

            if not paused:
                new_positions = []
                for x, y in positions:
                    dx, dy = random.choice([(0,1),(0,-1),(1,0),(-1,0),(0,0)])
                    nx, ny = (x + dx) % cols, (y + dy) % rows
                    new_positions.append((nx, ny))
                positions = new_positions
                move_count += 1

                if len(set(positions)) == 1:
                    all_runs.append(move_count)
                    save_leaderboard(move_count)
                    game_over = True
                    pygame.mixer.music.fadeout(1000)

            # DRAW
            screen.fill(GREEN)
            
            # Side panel background
            pygame.draw.rect(screen, (50, 100, 50), (grid_width, 0, PANEL_WIDTH, grid_height))
            
            # Panel title
            panel_title = pygame.font.SysFont(None, 24).render("CONTROLS", True, WHITE)
            screen.blit(panel_title, (grid_width + 20, 5))
            
            # Grid (only left side)
            for c in range(cols + 1):
                pygame.draw.line(screen, WHITE, (c*CELL_SIZE, 0), (c*CELL_SIZE, grid_height), 2)
            for r in range(rows + 1):
                pygame.draw.line(screen, WHITE, (0, r*CELL_SIZE), (grid_width, r*CELL_SIZE), 2)

            for i, (x_cell, y_cell) in enumerate(positions):
                color = SHIRT_COLORS[i % 4]
                cx = x_cell * CELL_SIZE + CELL_SIZE // 2
                cy = y_cell * CELL_SIZE + CELL_SIZE // 2 + 5
                name_surf = name_font.render(names[i], True, BLACK)
                screen.blit(name_surf, (cx - name_surf.get_width()//2, y_cell*CELL_SIZE + 5))
                draw_person(screen, cx, cy, color)

            moves_surf = moves_font.render(f"Moves: {move_count}", True, WHITE)
            screen.blit(moves_surf, (10, 10))
            if leaderboard:
                lb_surf = moves_font.render(f"Best: {leaderboard[0]}", True, WHITE)
                screen.blit(lb_surf, (10, 45))

            play_btn.draw(screen, button_font)
            quit_btn.draw(screen, button_font)

            pygame.display.flip()
            clock.tick(8)

        if input("\nPlay again? (y/n): ").lower() != 'y':
            break

    pygame.quit()
