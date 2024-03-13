import pygame
import random
import math

# Inicializa o Pygame
pygame.init()

# Constantes
LARGURA_TELA = 900
ALTURA_TELA = 600
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
TAMANHO_NAVE = 40
TAMANHO_PLANETA = 120
VELOCIDADE_NAVE = 5
FPS = 60
TAMANHO_GRADE = 60

# Define cores mais agradáveis
AZUL_CLARO = (173, 216, 230)
CINZA_CLARO = (200, 200, 200)
CINZA_ESCURO = (100, 100, 100)
AMARELO = (255, 255, 0)

# Cria a janela do jogo
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Rocket Distance")

# Carrega imagens
imagem_nave = pygame.image.load('spaceship_hd.png').convert_alpha()
imagem_planeta = pygame.image.load('planet_hd.png').convert_alpha()

# Carrega imagem de estrela para o fundo
imagem_estrela = pygame.image.load('star.png').convert_alpha()
imagem_estrela = pygame.transform.scale(imagem_estrela, (2, 2))


# Classes
class Nave(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_original = pygame.transform.scale(imagem_nave, (TAMANHO_NAVE, TAMANHO_NAVE))
        self.image = self.image_original
        self.rect = self.image.get_rect()
        self.rect.center = (LARGURA_TELA // 2, ALTURA_TELA // 2)
        self.velocidade = VELOCIDADE_NAVE

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidade
        elif teclas[pygame.K_RIGHT] and self.rect.right < LARGURA_TELA:
            self.rect.x += self.velocidade
        elif teclas[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.velocidade
        elif teclas[pygame.K_DOWN] and self.rect.bottom < ALTURA_TELA:
            self.rect.y += self.velocidade

        if teclas[pygame.K_LEFT]:
            self.image = pygame.transform.rotate(self.image_original, 180)
        elif teclas[pygame.K_RIGHT]:
            self.image = self.image_original
        elif teclas[pygame.K_UP]:
            self.image = pygame.transform.rotate(self.image_original, 90)
        elif teclas[pygame.K_DOWN]:
            self.image = pygame.transform.rotate(self.image_original, -90)

class Planeta(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(
            imagem_planeta, (TAMANHO_PLANETA, TAMANHO_PLANETA))
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(100, LARGURA_TELA - 100)
        self.rect.centery = random.randint(100, ALTURA_TELA - 100)


# Grupos de sprites
todos_sprites = pygame.sprite.Group()
planetas = pygame.sprite.Group()

# Cria objetos do jogo
nave = Nave()
planeta = Planeta()
todos_sprites.add(nave, planeta)

# Gera estrelas para o fundo
estrelas = []
for _ in range(100):
    x = random.randint(0, LARGURA_TELA)
    y = random.randint(0, ALTURA_TELA)
    estrelas.append((x, y))

# Loop principal do jogo
relogio = pygame.time.Clock()
executando = True
exibir_grade = True  # Flag para alternar visibilidade da grade

while executando:
    # Tratamento de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_g:
                exibir_grade = not exibir_grade  # Alternar visibilidade da grade

    # Atualiza
    todos_sprites.update()

    # Move estrelas com base no movimento da nave (efeito de paralaxe)
    for i, estrela in enumerate(estrelas):
        velocidade_estrela = 1 + i / 20  # Ajusta a velocidade com base no índice da estrela
        estrelas[i] = (estrela[0] - nave.velocidade * velocidade_estrela, estrela[1])
        # Envolve as bordas da tela
        if estrelas[i][0] < 0:
            estrelas[i] = (LARGURA_TELA, random.randint(0, ALTURA_TELA))
        elif estrelas[i][0] > LARGURA_TELA:
            estrelas[i] = (0, random.randint(0, ALTURA_TELA))
        if estrelas[i][1] < 0:
            estrelas[i] = (random.randint(0, LARGURA_TELA), ALTURA_TELA)
        elif estrelas[i][1] > ALTURA_TELA:
            estrelas[i] = (random.randint(0, LARGURA_TELA), 0)

    # Desenha
    tela.fill(PRETO)

    # Desenha estrelas para o fundo
    for estrela in estrelas:
        pygame.draw.rect(tela, AZUL_CLARO, (estrela[0], estrela[1], 2, 2))

    # Desenha a grade cartesiana se ativada
    if exibir_grade:
        min_x = -LARGURA_TELA // 2
        max_x = LARGURA_TELA // 2
        min_y = -ALTURA_TELA // 2
        max_y = ALTURA_TELA // 2
        offset_y = ALTURA_TELA // 2 - (max_y + min_y) // 2
        offset_x = LARGURA_TELA // 2 - (max_x + min_x) // 2

        for x in range(min_x, max_x + 1, TAMANHO_GRADE):
            pygame.draw.line(tela, CINZA_CLARO, (x + offset_x, 0), (x + offset_x, ALTURA_TELA))
            fonte = pygame.font.Font(None, 20)
            rotulo = fonte.render(str(x), True, CINZA_CLARO)
            tela.blit(rotulo, (x + LARGURA_TELA // 2 + 5, ALTURA_TELA // 2))

        for y in range(min_y, max_y + 1, TAMANHO_GRADE):
            pygame.draw.line(tela, CINZA_CLARO, (0, y + offset_y), (LARGURA_TELA, y + offset_y))
            fonte = pygame.font.Font(None, 20)
            rotulo = fonte.render(str(y), True, CINZA_CLARO)
            tela.blit(rotulo, (LARGURA_TELA // 2 + 5, ALTURA_TELA // 2 - y - 10))

    todos_sprites.draw(tela)

    # Define a cor, tamanho e fonte do texto
    COR_TEXTO = (255, 255, 255)
    TAMANHO_TEXTO = 24
    fonte = pygame.font.SysFont('arial', TAMANHO_TEXTO)

    # Exibe a distância até o planeta
    distancia_x = planeta.rect.centerx - nave.rect.centerx
    distancia_y = planeta.rect.centery - nave.rect.centery
    distancia = math.sqrt(distancia_x ** 2 + distancia_y ** 2)
    texto_distancia = fonte.render(f"Distância até o planeta: {distancia:.2f} unidades", True, COR_TEXTO)
    retangulo_texto_distancia = texto_distancia.get_rect()
    retangulo_texto_distancia.topleft = (10, 10)
    pygame.draw.rect(tela, PRETO, retangulo_texto_distancia)
    tela.blit(texto_distancia, retangulo_texto_distancia)

    x_planeta = planeta.rect.centerx - LARGURA_TELA // 2
    y_planeta = planeta.rect.centery - ALTURA_TELA // 2
    y_nave = nave.rect.centery - ALTURA_TELA // 2
    x_nave = nave.rect.centerx - LARGURA_TELA // 2

    # Exibe a fórmula
    texto_formula = fonte.render(f"Distância = √( ({x_planeta} - {x_nave})² + ({y_planeta} - {y_nave})² )", True, COR_TEXTO)
    retangulo_texto_formula = texto_formula.get_rect()
    retangulo_texto_formula.topleft = (10, 40)
    pygame.draw.rect(tela, PRETO, retangulo_texto_formula)
    tela.blit(texto_formula, retangulo_texto_formula)

    # Exibe as coordenadas da nave
    texto_coordenadas_nave = fonte.render(f"Coordenadas da Nave: ({nave.rect.centerx - LARGURA_TELA // 2}, { (nave.rect.centery - ALTURA_TELA // 2) * -1})", True, COR_TEXTO)
    retangulo_texto_coordenadas_nave = texto_coordenadas_nave.get_rect()
    retangulo_texto_coordenadas_nave.topleft = (10, 70)
    pygame.draw.rect(tela, PRETO, retangulo_texto_coordenadas_nave)
    tela.blit(texto_coordenadas_nave, retangulo_texto_coordenadas_nave)

    # Exibe as coordenadas do planeta
    texto_coordenadas_planeta = fonte.render(f"Coordenadas do Planeta: ({planeta.rect.centerx - LARGURA_TELA // 2}, { (planeta.rect.centery - ALTURA_TELA // 2) * -1})", True, COR_TEXTO)
    retangulo_texto_coordenadas_planeta = texto_coordenadas_planeta.get_rect()
    retangulo_texto_coordenadas_planeta.topleft = (10, 100)
    pygame.draw.rect(tela, PRETO, retangulo_texto_coordenadas_planeta)
    tela.blit(texto_coordenadas_planeta, retangulo_texto_coordenadas_planeta)

    pygame.display.flip()

    # Limita a taxa de quadros
    relogio.tick(FPS)

pygame.quit()
