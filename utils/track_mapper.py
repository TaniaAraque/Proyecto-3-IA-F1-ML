"""
Herramienta para mapear waypoints del circuito haciendo clic en la imagen.
Ejecuta este script y haz clic en la imagen siguiendo la trayectoria del circuito.
"""
import pygame
import sys

def get_track_waypoints():
    pygame.init()
    
    track_img = pygame.image.load("assets/track.png")
    track_img = pygame.transform.scale(track_img, (900, 600))
    
    screen = pygame.display.set_mode((900, 600))
    pygame.display.set_caption("Click para marcar waypoints - ESC para terminar")
    
    waypoints = []
    font = pygame.font.SysFont("Arial", 16)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_u and waypoints:  
                    waypoints.pop()
            elif event.type == pygame.MOUSEBUTTONDOWN:

                pos = pygame.mouse.get_pos()
                waypoints.append(pos)
                print(f"Punto {len(waypoints)}: {pos}")
        

        screen.blit(track_img, (0, 0))
        

        if len(waypoints) > 0:
            for i, point in enumerate(waypoints):
                pygame.draw.circle(screen, (255, 0, 0), point, 5)

                text = font.render(str(i+1), True, (255, 255, 255))
                screen.blit(text, (point[0] + 8, point[1] - 8))
            

            if len(waypoints) > 1:
                pygame.draw.lines(screen, (0, 255, 0), False, waypoints, 2)
        

        instructions = [
            "Haz clic para agregar puntos siguiendo el circuito",
            f"Puntos marcados: {len(waypoints)}",
            "U = Deshacer último | ESC = Terminar"
        ]
        
        y_offset = 10
        for text in instructions:
            label = font.render(text, True, (255, 255, 0))
            pygame.draw.rect(screen, (0, 0, 0), (5, y_offset - 2, label.get_width() + 10, 20))
            screen.blit(label, (10, y_offset))
            y_offset += 25
        
        pygame.display.update()
    
    pygame.quit()
    

    if waypoints:
        print("\n" + "="*60)
        print("COPIA ESTE CÓDIGO EN create_track_path():")
        print("="*60)
        print("path = [")
        for point in waypoints:
            print(f"    {point},")
        print("]")
        print("="*60)
    
    return waypoints

if __name__ == "__main__":
    print("=== MAPEADOR DE CIRCUITO ===")
    print("Instrucciones:")
    print("1. Haz clic en la imagen siguiendo la línea del circuito")
    print("2. Coloca puntos cada cierta distancia (15-30 puntos es bueno)")
    print("3. Presiona ESC cuando termines")
    print("4. Copia el código generado\n")
    
    waypoints = get_track_waypoints()
