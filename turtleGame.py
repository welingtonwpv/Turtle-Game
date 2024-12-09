import pygame
import sys
import random
import os

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
pygame.display.set_caption("Atividade Prática - Welington Pereira RU: 4471040")

# Função para garantir o caminho correto dos recursos no ambiente de execução
def resource_path(relative_path):
    """Obtém o caminho correto para os arquivos de recursos no ambiente de execução"""
    try:
        # Se estiver executando a partir do arquivo .exe
        base_path = sys._MEIPASS
    except Exception:
        # Se estiver executando a partir do código fonte diretamente
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

credits_font = pygame.font.Font(resource_path("assets/PressStart2P-Regular.ttf"), 18)

# Defina o ícone da janela
icon = pygame.image.load(resource_path('assets/icon.png'))  # Certifique-se de que o ícone está na pasta 'assets'
pygame.display.set_icon(icon)

# Usando resource_path para carregar a fonte
game_font = pygame.font.Font(resource_path("assets/PressStart2P-Regular.ttf"), 24)

# Classes

class Cloud(pygame.sprite.Sprite):
    def __init__(self, image, x_pos, y_pos):
        super().__init__()
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.rect.x -= 1


class Turtle(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.running_sprites = []
        self.ducking_sprites = []
        self.jumping_sprite = pygame.transform.scale(
            pygame.image.load(resource_path("assets/TurtleJumping.png")), (80, 100))  # Imagem de pulo

        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load(resource_path("assets/Turtle1.png")), (80, 100)))
        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load(resource_path("assets/Turtle2.png")), (80, 100)))

        self.ducking_sprites.append(pygame.transform.scale(
            pygame.image.load(resource_path(f"assets/TurtleDucking1.png")), (110, 60)))
        self.ducking_sprites.append(pygame.transform.scale(
            pygame.image.load(resource_path(f"assets/TurtleDucking2.png")), (110, 60)))

        self.x_pos = x_pos
        self.y_pos = y_pos
        self.current_image = 0
        self.image = self.running_sprites[self.current_image]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.velocity = 12  # Aumente a velocidade inicial do pulo para maior altura
        self.gravity = 0.5
        self.ducking = False
        self.jumping = False  # Flag de pulo
        self.jump_height = 0  # Para controlar a altura do pulo

    def jump(self):
        if not self.jumping:  # Verifica se o dinossauro não está já pulando
            jump_sfx.play()
            self.jumping = True
            self.velocity = 15  # Aumente o valor de velocity para um pulo mais alto
            self.jump_height = 0  # Reseta a altura do pulo

    def apply_gravity(self):
        if self.jumping:  # Aplica a gravidade apenas quando estiver pulando
            self.rect.centery -= self.velocity  # Movimento para cima no início do pulo
            self.velocity -= self.gravity  # Reduz a velocidade para simular a gravidade

            if self.rect.centery <= 100:  # Aumente esse valor para fazer o pulo mais alto
                self.velocity = -self.velocity  # Inverte a velocidade para cair

        if self.rect.centery >= 360:  # Quando atinge o solo
            self.rect.centery = 360  # Garante que o dinossauro não ultrapasse o solo
            self.jumping = False  # O pulo termina
            self.velocity = 12  # Restabelece a velocidade de pulo

    def update(self):
        self.animate()
        self.apply_gravity()

    def animate(self):
        if self.jumping:
            self.image = self.jumping_sprite  # Imagem de pulo
        elif self.ducking:
            self.image = self.ducking_sprites[int(self.current_image)]
        else:
            self.current_image += 0.05
            if self.current_image >= 2:
                self.current_image = 0
            self.image = self.running_sprites[int(self.current_image)]  # Imagem de corrida

    def duck(self):
        self.ducking = True
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos + 25))  # Ajusta a posição quando agachado

    def unduck(self):
        self.ducking = False
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))  # Restaura a posição normal


class PalmTree(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.sprites = []
        for i in range(1, 7):
            current_sprite = pygame.transform.scale(
                pygame.image.load(resource_path(f"assets/palmeiras/palmeira{i}.png")), (100, 100))
            self.sprites.append(current_sprite)
        self.image = random.choice(self.sprites)
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.x_pos -= game_speed
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))


class Ptero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x_pos = 1300
        self.y_pos = random.choice([280, 295, 350])
        self.sprites = []
        self.sprites.append(
            pygame.transform.scale(
                pygame.image.load(resource_path("assets/Ptero1.png")), (84, 62)))
        self.sprites.append(
            pygame.transform.scale(
                pygame.image.load(resource_path("assets/Ptero2.png")), (84, 62)))
        self.current_image = 0
        self.image = self.sprites[self.current_image]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.animate()
        self.x_pos -= game_speed
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def animate(self):
        self.current_image += 0.025
        if self.current_image >= 2:
            self.current_image = 0
        self.image = self.sprites[int(self.current_image)]


# Variáveis

game_speed = 5
jump_count = 10
player_score = 0
game_over = False
obstacle_timer = 0
obstacle_spawn = False
obstacle_cooldown = 1000


# Superfícies

ground = pygame.image.load(resource_path("assets/ground.png"))
ground = pygame.transform.scale(ground, (1280, 20))
ground_x = 0
ground_rect = ground.get_rect(center=(640, 405))
cloud = pygame.image.load(resource_path("assets/cloud.png"))
cloud = pygame.transform.scale(cloud, (200, 80))

# Grupos

cloud_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()
turtle_group = pygame.sprite.GroupSingle()
ptero_group = pygame.sprite.Group()

# Objetos
turtle = Turtle(50, 360)
turtle_group.add(turtle)

# Sons
death_sfx = pygame.mixer.Sound(resource_path("assets/sfx/lose.mp3"))
points_sfx = pygame.mixer.Sound(resource_path("assets/sfx/100points.mp3"))
jump_sfx = pygame.mixer.Sound(resource_path("assets/sfx/jump.mp3"))

# Eventos
CLOUD_EVENT = pygame.USEREVENT
pygame.time.set_timer(CLOUD_EVENT, 3000)

# Funções

def end_game():
    global player_score, game_speed
    game_over_text = game_font.render("Game Over!", True, "black")
    game_over_rect = game_over_text.get_rect(center=(640, 300))
    score_text = game_font.render(f"Score: {int(player_score)}", True, "black")
    score_rect = score_text.get_rect(center=(640, 340))
    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    game_speed = 5
    cloud_group.empty()
    obstacle_group.empty()



while True:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        turtle.duck()
    else:
        if turtle.ducking:
            turtle.unduck()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == CLOUD_EVENT:
            current_cloud_y = random.randint(50, 300)
            current_cloud = Cloud(cloud, 1380, current_cloud_y)
            cloud_group.add(current_cloud)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                turtle.jump()
                if game_over:
                    game_over = False
                    game_speed = 5
                    player_score = 0

    screen.fill("white")

    # Colisões
    if pygame.sprite.spritecollide(turtle_group.sprite, obstacle_group, False):
        game_over = True
        death_sfx.play()
    if game_over:
        end_game()

    if not game_over:
        game_speed += 0.0025
        if round(player_score, 1) % 100 == 0 and int(player_score) > 0:
            points_sfx.play()

        if pygame.time.get_ticks() - obstacle_timer >= obstacle_cooldown:
            obstacle_spawn = True

        if obstacle_spawn:
            obstacle_random = random.randint(1, 50)
            if obstacle_random in range(1, 7):
                new_obstacle = PalmTree(1280, 355)
                obstacle_group.add(new_obstacle)
                obstacle_timer = pygame.time.get_ticks()
                obstacle_spawn = False
            elif obstacle_random in range(7, 10):
                new_obstacle = Ptero()
                obstacle_group.add(new_obstacle)
                obstacle_timer = pygame.time.get_ticks()
                obstacle_spawn = False

        player_score += 0.1
        player_score_surface = game_font.render(
            str(int(player_score)), True, ("black"))
        screen.blit(player_score_surface, (1150, 10))

        # Atualiza e desenha o chão
        ground_x -= game_speed  # Move o chão para a esquerda
        if ground_x <= -1280:
            ground_x = 0
        screen.blit(ground, (ground_x, ground_rect.y))  # Primeiro chão
        screen.blit(ground, (ground_x + 1280, ground_rect.y))  # Segundo chão

        # Atualiza e desenha outros objetos
        cloud_group.update()
        cloud_group.draw(screen)

        ptero_group.update()
        ptero_group.draw(screen)

        turtle_group.update()
        turtle_group.draw(screen)

        obstacle_group.update()
        obstacle_group.draw(screen)

        # Exibir créditos
        credits_text = credits_font.render("Desenvolvido por Welington Pereira RU: 4471040", True, "black")
        credits_rect = credits_text.get_rect(center=(640, 700))  # Alinha ao centro, perto do rodapé
        screen.blit(credits_text, credits_rect)


    clock.tick(120)
    pygame.display.update()
