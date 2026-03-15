import pygame
from mode_35 import run_35

def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 650))
    pygame.display.set_caption("Wandering in the Woods")
    clock = pygame.time.Clock()
    
    while True:
        print("\n=== Wandering in the Woods ===")
        print("2. Grades 3–5")
        print("4. Exit")
        print("Press ESC in game to return to menu")
        
        choice = input("Select level (2-4): ")
        
        if choice == "2":
            try:
                run_35(screen)
            except:
                pygame.event.pump()  # Keep window responsive
            print("Game ended. Select option again.")
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again!")
    
    pygame.quit()

if __name__ == "__main__":
    main()
