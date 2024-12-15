import pygame
from settings import *
from sprites import Player

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Unbeatable AI")
        self.clock = pygame.time.Clock()
        
        self.all_sprites = pygame.sprite.Group()
        self.player = Player(self.all_sprites)
        
        self.opponent = pygame.Rect(POS['opponent'], SIZE['paddle'])
        self.ball = pygame.Rect(WINDOW_WIDTH // 2 - SIZE['ball'][0] // 2, 
                                WINDOW_HEIGHT // 2 - SIZE['ball'][1] // 2, 
                                *SIZE['ball'])
        
        self.ball_speed_x = SPEED['ball']
        self.ball_speed_y = SPEED['ball']

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            dt = self.clock.tick(60) / 1000

            self.update(dt)
            self.draw()

    def update(self, dt):
        self.all_sprites.update(dt)
        
        # Move the opponent (AI)
        ai_speed = SPEED['opponent'] * 1.5  # Increase AI speed by 50%
        if self.opponent.centery < self.ball.centery:
            self.opponent.y += ai_speed * dt
        elif self.opponent.centery > self.ball.centery:
            self.opponent.y -= ai_speed * dt
        
        # Predict ball's y-position when it reaches the AI's x-position
        time_to_reach = (self.opponent.centerx - self.ball.centerx) / self.ball_speed_x
        predicted_y = self.ball.centery + self.ball_speed_y * time_to_reach
        
        # Move towards the predicted position
        if abs(self.opponent.centery - predicted_y) > 10:  # Add a small threshold
            if self.opponent.centery < predicted_y:
                self.opponent.y += ai_speed * dt
            else:
                self.opponent.y -= ai_speed * dt
        
        self.opponent.clamp_ip(self.screen.get_rect())

        # Move the ball
        self.ball.x += self.ball_speed_x * dt
        self.ball.y += self.ball_speed_y * dt

        # Ball collision with walls
        if self.ball.top <= 0 or self.ball.bottom >= WINDOW_HEIGHT:
            self.ball_speed_y *= -1

        # Ball collision with paddles
        if self.ball.colliderect(self.player.rect) or self.ball.colliderect(self.opponent):
            self.ball_speed_x *= -1

        # Reset ball if it goes out of bounds
        if self.ball.left <= 0 or self.ball.right >= WINDOW_WIDTH:
            self.ball.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
            self.ball_speed_x *= -1

    def draw(self):
        self.screen.fill(COLORS['bg'])
        self.all_sprites.draw(self.screen)
        pygame.draw.rect(self.screen, COLORS['paddle'], self.opponent)
        pygame.draw.ellipse(self.screen, COLORS['ball'], self.ball)
        pygame.display.flip()

if __name__ == '__main__':
    game = Game()
    game.run()
