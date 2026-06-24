import pygame
import random
#import background
import os




pygame.init()
#Configurações:
largura, altura = 800, 600
#Rotas verticais:
faixa_1 = 150
faixa_2 = 300
faixa_3 = 450

#Timers:
spawn_timer = pygame.USEREVENT + 1
tempo_para_nascer = 2000
pygame.time.set_timer(spawn_timer, tempo_para_nascer)

#som:
pygame.mixer.init()
splash = pygame.mixer.Sound(r"Assets\Audios\splash.mp3")
tema = pygame.mixer.music.load(r"Assets\Audios\tema.mp3")
pygame.mixer.music.play(-1)



#Telas:
estado_do_jogo = "Menu"
#Menu, Jogo, Fim

velocidade = 5

fonte = pygame.font.Font("Assets\Fonte\Fonte.ttf", 50)
fonte_menor = pygame.font.Font("Assets\Fonte\Fonte.ttf", 15)
fps = 30
clock = pygame.time.Clock()


tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("TucunaRED")


#Cores:
vermelho = (255, 0, 0)
preto = (0, 0, 0)
verde = (0, 255, 0)
dourado = (255, 215, 0)
branco = (255, 255, 255)


class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        imagem = pygame.image.load(r"Assets\Imagens\Barco\Variações\Barco004.png")
        self.image = pygame.transform.scale(imagem, (80, 64))
        self.rect = self.image.get_rect()
        self.rota = 2
        self.peixes_pescados = 0
        self.vida = 1
        self.vida_padrao = 1
        self.vivo = True

jogador = Jogador() 
jogador_grupo = pygame.sprite.Group()
jogador_grupo.add(jogador)


class Fundo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        imagem = pygame.image.load(caminho).convert()
        self.image = pygame.transform.scale(imagem, (largura, altura))

# Pasta onde estão as imagens
PASTA_IMAGENS = r"Assets\Imagens\Background"  
frame = 62

# Carrega todas as imagens em uma lista
frames = []
for i in range(1, 64): 
    caminho = os.path.join(PASTA_IMAGENS, f"waterAnimation\\waterAnimation{i}.png")


    img = pygame.image.load(caminho).convert_alpha()
    img = pygame.transform.scale(img, (largura, altura)) 
        
    frames.append(img)

# Animação (area de pesca):
PASTA_BOLHAS = r"Assets\Imagens\Area de pesca"
animacao_pesca = 0

#Colocar todas as imagens na lista
pescas = []

for i in range(1, 21):
    caminho = os.path.join(PASTA_BOLHAS, f"area_de_pesca_{i}.png")


    img = pygame.image.load(caminho).convert_alpha()
    img = pygame.transform.scale(img, (64, 16))  
    pescas.append(img)

class Bolhas(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self) 
        imagem = pescas[animacao_pesca]
        self.image = pygame.transform.scale(imagem, (64, 16))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
bolhas_group = pygame.sprite.Group()
lista_bolhas = [
    Bolhas(800, 150 + jogador.rect.height - 25),
    Bolhas(800 + 50, 150 + jogador.rect.height - 25),
    Bolhas(800 + 100, 150 + jogador.rect.height - 25),
    Bolhas(800 + 150, 150 + jogador.rect.height - 25)
]
for elementos in lista_bolhas:
    bolhas_group.add(elementos)

class Ceu(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        imagem = pygame.image.load("Assets\Imagens\Background\ceu.png").convert()
        self.image = pygame.transform.scale(imagem, (largura, altura))
        self.rect = self.image.get_rect()
ceu_grupo = pygame.sprite.Group()
ceu = Ceu()
ceu_grupo.add(ceu)

class Tsunami(pygame.sprite.Sprite):
     def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        imagem = pygame.image.load(r"Assets\Imagens\Tsunami\wave.png")
        self.image = pygame.transform.scale(imagem, (48, 32))
        self.rect = self.image.get_rect()
        self.rect.x = 800
        self.rect.y = faixa_2 + 20

tsunami_forte = Tsunami()
tsunami_group = pygame.sprite.Group()
tsunami_group.add(tsunami_forte)


#Cachoeira:
PASTA_CACHOEIRA = r"Assets\Imagens\Cachoeira"
cachoeira_animada = []
sprite_cachoeira = 0
#Colocar as imagens da cachoeira em uma pasta para animar
for i in range(1, 9):
    caminho = os.path.join(PASTA_CACHOEIRA, f"Sprite-000{i}.png")


    img = pygame.image.load(caminho).convert_alpha()
    img = pygame.transform.scale(img, (96, 48))  
    cachoeira_animada.append(img)


class Cachoeira(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        imagem = cachoeira_animada[sprite_cachoeira]
        self.image = pygame.transform.scale(imagem, (96, 48))
        self.rect = self.image.get_rect()
        self.rect.x = 800
        self.rect.y = faixa_3 + 20
cachoeira = Cachoeira()
cachoeira_grupo = pygame.sprite.Group()
cachoeira_grupo.add(cachoeira)

    

class Botao(pygame.sprite.Sprite):
    def __init__(self, png):
        pygame.sprite.Sprite.__init__(self)
        imagem = pygame.image.load(png)
        self.image = pygame.transform.scale(imagem, (143, 79))
        self.rect = self.image.get_rect()
    def clicou(self):
        seta = pygame.mouse.get_pos()
        if self.rect.collidepoint(seta):
            if pygame.mouse.get_pressed()[0] == 1:
                return True
                 


#Funções:

def bolhas():
    global animacao_pesca
    bolhas_group.draw(tela)
    pygame.display.flip()
    for elementos in bolhas_group:
        elementos.image = pescas[animacao_pesca]
    animacao_pesca += 1
    if animacao_pesca >= 20:
        animacao_pesca = 1



def movimento():
    jogador.rect.x = 100 - 60
    jogador.rect.y = jogador.rota*150

def correnteza():
    global velocidade
    for bolhinhas in bolhas_group:
        bolhinhas.rect.x -= velocidade
        if bolhinhas.rect.x <= 0:
            bolhas_group.remove(bolhinhas)

         





def eventos():
    global rodando

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        
        #if estado_do_jogo == "Menu":
            

        if estado_do_jogo == "Jogo":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    if jogador.rota < 3:
                        jogador.rota += 1
                        

                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    if jogador.rota > 1:
                        jogador.rota -= 1

                #Jogador pescar:
                sobre_peixes = pygame.sprite.spritecollide(jogador, bolhas_group, True)
                if event.key == pygame.K_SPACE and sobre_peixes:
                    jogador.peixes_pescados += 1
                    splash.play() #Som de pesca
                    splash.set_volume(1) 
                    if jogador.peixes_pescados >= 5:  #Melhorias do barco
                        barco_com_peixe = pygame.image.load(r"Assets\Imagens\Barco\Variações\Barco008.png")
                        jogador.image = pygame.transform.scale(barco_com_peixe, (80, 64))
                    elif jogador.vida >= 3:
                        barco_melhoria_1 = pygame.image.load(r"Assets\Imagens\Barco\Variações\Barco009.png")
                        jogador.image = pygame.transform.scale(barco_melhoria_1, (80, 64))
                        
            
            #cria os obstáculos:
            #verifica o timer
            elif event.type == spawn_timer:
                
                #analisa quantos vão nascer
                quantos = random.randint(1,3)
                if quantos == 1:
                    criar_obstaculos()
                elif quantos == 2: #Cria 2 ao mesmo tempo
                    for i in range(2):
                        criar_obstaculos()
                        
                elif quantos == 3: #aumentamos a dificuldade por meio da velocidade
                    global velocidade
                    if velocidade < 15:
                        velocidade += 1
                    else:
                        global tempo_para_nascer
                        if tempo_para_nascer >= 200:
                            
                            tempo_para_nascer -= 50
                            pygame.time.set_timer(spawn_timer, tempo_para_nascer)

def verificar_duplas():
    duplas_B_T = pygame.sprite.groupcollide(bolhas_group, tsunami_group, False, False)
    # Detectar colisões

    # Mudar posição de um sprite que colidiu
    for foto_bolha, lista_tsunami in duplas_B_T.items():
        # mover o sprite de tsunami para posição aleatória
        for tsunamis in lista_tsunami:
            tsunamis.rect.y = random.randint(1, 3) * 150 + 20

    duplas_B_C = pygame.sprite.groupcollide(bolhas_group, cachoeira_grupo, False, False)
    # Detectar colisões

    # Mudar posição de um sprite que colidiu
    for foto_bolha, lista_de_cachoeiras in duplas_B_C.items():
        # mover o sprite de cachoeira para posição aleatória
        for cachoeiras in lista_de_cachoeiras:
            cachoeiras.rect.y = random.randint(1, 3) * 150 + 20
    
    duplas_C_T = pygame.sprite.groupcollide(cachoeira_grupo, tsunami_group, False, False)
    # Detectar colisões

    # Mudar posição de um sprite que colidiu
    for foto_cachoeira, lista_tsunami in duplas_C_T.items():
        # mover o sprite de tsunami para posição aleatória
        for tsunamis in lista_tsunami:
            tsunamis.rect.y = random.randint(1, 3) * 150 + 20


def criar_obstaculos():
    qual = random.randint(1,3)
    if qual == 1:#Bolha
        #define em qual faixa irá nascer
        faixa = random.randint(1,3)
        novo_evento = Bolhas(largura, faixa * 150 + jogador.rect.height - 25)
        bolhas_group.add(novo_evento)
    elif qual == 2:#Cachoeira
        faixa = random.randint(1,3)
        novo_evento = Cachoeira()
        novo_evento.rect.y = faixa * 150 + 20
        cachoeira_grupo.add(novo_evento)
    elif qual == 3:#Tsunami
        faixa = random.randint(1,3)
        novo_evento = Tsunami()
        novo_evento.rect.y = faixa * 150 + 20
        tsunami_group.add(novo_evento)
def tutorial():                    
    tutoriais = [
            "Comandos:",
            "W(cima) e S (baixo) movem",
            "(espaço) para pescar"
            ]
    paragrafo = 450
    for linha in tutoriais:

        label_tutorial = fonte_menor.render(linha, True, branco)
        paragrafo += fonte_menor.get_height() + 15
        tela.blit(label_tutorial, (50, paragrafo))
                
    
def menu():
    global estado_do_jogo

    tela.fill(preto)
    jogar = Botao(r"Assets\Imagens\Botões\jogar.png")
    pontos = Botao(r"Assets\Imagens\Peixes\Clownfish Outline.png")
    loja = Botao(r"Assets\Imagens\Barco\Boat Shop.png")
    vida = Botao(r"Assets\Imagens\Botões\vida.png")

    label_peixes = fonte.render(f"Peixes: {jogador.peixes_pescados}", True, branco)
    label_loja = fonte.render(f"Loja", True, branco)

    tutorial()

    #Organizando a tabela de pontos
    pontos.rect.x = 500
    pontos.rect.y = 50
    pontos.image = pygame.transform.scale(pontos.image, (36, 36))

    #organizando a tabela de loja
    loja.rect.x = 600
    loja.rect.y = 300
    loja.image = pygame.transform.scale(loja.image, (72, 72) )

    #organizando o botao de vida extra
    vida.rect.x = 495
    vida.rect.y = 375
    vida.image = pygame.transform.scale_by(vida.image, 0.75)


    botao_grupo = pygame.sprite.Group()
    botao_grupo.add(jogar)
    botao_grupo.add(pontos)
    botao_grupo.add(loja)
    botao_grupo.add(vida)

    jogar.rect.x = largura/2 - 100
    jogar.rect.y = altura/2 - 60

    #Desenhando o menu
    botao_grupo.draw(tela)
    tela.blit(label_peixes, (540, 40))
    tela.blit(label_loja, (500, 300))

    #Analisando os botoes clicados:
    if jogar.clicou() == True:
        estado_do_jogo = "Jogo"
    if vida.clicou():
        if jogador.peixes_pescados >= 5:
            jogador.vida += 1
            jogador.vida_padrao += 1
            jogador.peixes_pescados -= 5
    pygame.display.flip()



        
def ondas():
    global frame
    tela.blit(frames[frame], (0, 0))
    tela.blit(frames[frame], (0, -185))
        
        #Atualiza a animação
    frame -= 1
    if frame <= 2:
        frame = 62  #Reinicia a animação

def config_tsunami():
    for tsunami in tsunami_group:
        tsunami.rect.x -= velocidade
        if tsunami.rect.x <= 0:
            tsunami_group.remove(tsunami)
    tsunami_colidido = pygame.sprite.spritecollide(jogador, tsunami_group, True)
    if tsunami_colidido:
        if jogador.vida > 0:
            jogador.vida -= 1


def config_cachoeiras():
    global sprite_cachoeira
    for cachoeira in cachoeira_grupo:
        cachoeira.image = cachoeira_animada[sprite_cachoeira]
        sprite_cachoeira += 1
        if sprite_cachoeira >= 7:
            sprite_cachoeira = 0
        cachoeira.rect.x -= velocidade
        if cachoeira.rect.x <= 0:
            cachoeira_grupo.remove(cachoeira)

        cachoeiras_colididas = pygame.sprite.spritecollide(jogador, cachoeira_grupo, False)
        if cachoeiras_colididas:
            jogador.rota = 2

def morte():
    global estado_do_jogo
    if jogador.vida <= 0:
        jogador.vivo = False
    if jogador.vivo == False:
        estado_do_jogo = "Fim"
        for cachoeira in cachoeira_grupo:
            cachoeira_grupo.remove(cachoeira)
        for tsunami in tsunami_group:
            tsunami_group.remove(tsunami)
        for bolha in bolhas_group:
            bolhas_group.remove(bolha)

def game_over():
    global estado_do_jogo


    tela.fill(preto)
    
    texto_central = fonte.render(f"Fim da pescaria", True, branco)

    voltar_menu = Botao(r"Assets\Imagens\Botões\menu.png")
    voltar_menu.rect.x = largura/2 - voltar_menu.rect.width + 50
    voltar_menu.rect.y = altura/2 + voltar_menu.rect.height
    fim_de_jogo_grupo = pygame.sprite.Group()
    fim_de_jogo_grupo.add(voltar_menu)
    if voltar_menu.clicou():
        estado_do_jogo = "Menu"
        jogador.vida = jogador.vida_padrao
        jogador.vivo = True
        

    fundo_fim = pygame.image.load(r"Assets\Imagens\Background\fim de jogo\fundo_fim.png").convert_alpha()

    pontos = pygame.image.load(r"Assets\Imagens\Peixes\Clownfish Outline.png")
    pontos = pygame.transform.scale2x(pontos)
    label_peixes = fonte.render(f"Peixes: {jogador.peixes_pescados}", True, branco)


    tela.blit(fundo_fim, (0,0))
    tela.blit(texto_central, (largura/2, altura/2 - 50))
    tela.blit(label_peixes, (400, 200))
    tela.blit(pontos, (600, 220))
    fim_de_jogo_grupo.draw(tela)

    
    pygame.display.flip()




def desenhar():
    #tela.fill(preto)
    

    ceu_grupo.draw(tela)

    ondas()

    tsunami_group.draw(tela)

    bolhas()

    cachoeira_grupo.draw(tela)

    config_cachoeiras()

    jogador_grupo.draw(tela)

    label_peixes = fonte.render(f"Peixes: {jogador.peixes_pescados}", True, branco)

    label_vida = fonte.render(f"Vida: {jogador.vida}", True, branco)

    tela.blit(label_vida, (50, 50))

    tela.blit(label_peixes, (540, 40))
  
    pygame.display.flip()

rodando = True

while rodando == True:
    clock.tick(fps)


    eventos()

    if estado_do_jogo == "Menu":
        menu()

        
    elif estado_do_jogo == "Jogo":
        movimento()

        correnteza()

        config_tsunami()

        morte()

        verificar_duplas()

        desenhar()

    
    elif estado_do_jogo == "Fim":
        game_over()

        
        

        

        
    