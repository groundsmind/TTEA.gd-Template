#################################################################################
######################### SOFTWARE BASE - PROJETO T-TEA #########################
#################################################################################
################################# VERSÃO 1.0 ####################################
#################################################################################
import csv
import cv2
import numpy as np
import time
import random
import settings
import os
from pathlib import Path

CURR_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURR_FILE.parent
#################################################################################
################################## Hora de Inicio ###############################
#################################################################################
inicio_da_sessao=False
if inicio_da_sessao==False:
    inicio_da_sessao_t0 = int(time.time())
    inicio_da_sessao=True
#################################################################################
#################################### Hardware ###################################
#################################################################################
# Tamanho das Telas:
largura_projetor = 800  # Altere este valor de acordo com a resolução da projeção do jogo.
altura_projetor = 600  # Altere este valor de acordo com a resolução da projeção do jogo.
largura_tela_controle = 640  # Esta tela é usada pelo terapeuta/operador. Altere o valor caso necessário.
altura_tela_controle = 480  # Esta tela é usada pelo terapeuta/operador. Altere o valor caso necessário.
relacao_largura = (largura_projetor / largura_tela_controle)  # Esta relação é usada na correção de perspectiva.
relacao_altura = (altura_projetor / altura_tela_controle)  # Esta relação é usada na correção de perspectiva.
tela_de_calibracao = np.zeros((altura_projetor, largura_projetor, 3),
                            np.uint8)  # Tela que será usada para o projetar o jogo.
tela_de_controle = np.zeros((altura_tela_controle, largura_tela_controle, 3),
                            np.uint8)  # Tela que será usada para o projetar o jogo.


csv.register_dialect(
    'mydialect',
    delimiter = ';',
    quotechar = '"',
    doublequote = True,
    skipinitialspace = True,
    lineterminator = '\n',
    quoting = csv.QUOTE_MINIMAL)

#################################################################################
################################## CORES & FONTES ###############################
#################################################################################
azul = 0, 0, 255
verde = 0, 255, 0
vermelho = 255, 0, 0
amarelo = 255, 255, 0
branco = 255, 255, 255
preto = 0, 0, 0

fonte = cv2.FONT_HERSHEY_SIMPLEX

#################################################################################
############################# VARIÁVEIS DE PROGRAMA #############################
#################################################################################
pontos_calibracao = settings.pontos_calibracao  # Matriz para os pontos de calibração de perspectiva - 4 linhas/ 2 colunas
contador = 0  # Contador utilizado nos 4 pontos de calibração
figura_selecionada=False # Usada para evitar que o usuário apenas selecione uma vez a figura e não ficar piscando
x_pose = 0
y_pose = 0

def resetar_vars():

    global pontos_calibracao, contador
    contador = 0


def calibrar_ttea(client):

    global gameDisplay#, x_pose, y_pose

    resetar_vars()

    camera = cv2.VideoCapture(0)
    gameExit=False
    cal_ok_sent = False

    #################################################################################
    #################### Inicialização do MediaPipe e Calibração ####################
    #################################################################################
    while not gameExit:

        # with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        if camera.isOpened():
            ret, frame = camera.read()
            tela_de_controle = frame

            cv2.circle(tela_de_controle, (pontos_calibracao[0]), 5, azul, 3)
            cv2.circle(tela_de_controle, (pontos_calibracao[1]), 5, azul, 3)
            cv2.circle(tela_de_controle, (pontos_calibracao[2]), 5, azul, 3)
            cv2.circle(tela_de_controle, (pontos_calibracao[3]), 5, azul, 3)
            # Depois da Calibração.
            if contador == 4:
                cv2.line(tela_de_controle, (pontos_calibracao[0]), (pontos_calibracao[1]), (verde), 2)
                cv2.line(tela_de_controle, (pontos_calibracao[1]), (pontos_calibracao[3]), (verde), 2)
                cv2.line(tela_de_controle, (pontos_calibracao[2]), (pontos_calibracao[0]), (verde), 2)
                cv2.line(tela_de_controle, (pontos_calibracao[2]), (pontos_calibracao[3]), (verde), 2)


                if not cal_ok_sent:
                    client.send("CAL_OK")
                    cal_ok_sent = True
                pass
            

            # Atualização das telas
            cv2.imshow("TELA DE CONTROLE", tela_de_controle)
            cv2.setMouseCallback("TELA DE CONTROLE", mousePoints)
            cv2.waitKey(1)

            msg = client.poll()
            if msg == "CAL_ACK":
                gameExit = True
                cv2.destroyWindow("TELA DE CONTROLE")
                grava_calibracao()
                print('P1: ', pontos_calibracao[0], ' P2: ', pontos_calibracao[1], ' P3: ', pontos_calibracao[2], ' P4: ', pontos_calibracao[3])
                camera.release()

            '''
            # Teclas de Atalho
            for event in pygame.event.get():
                # SAIR
                if event.type == pygame.QUIT:
                    gameExit=True
                    cv2.destroyWindow("TELA DE CONTROLE")
                    grava_calibracao()
                    print('P1: ', pontos_calibracao[0], ' P2: ', pontos_calibracao[1], ' P3: ', pontos_calibracao[2], ' P4: ', pontos_calibracao[3])
                    pygame.display.quit()
                    camera.release()

            # SAIR (ESC)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        cv2.destroyWindow("TELA DE CONTROLE")
                        grava_calibracao()
                        print('P1: ', pontos_calibracao[0], ' P2: ', pontos_calibracao[1], ' P3: ', pontos_calibracao[2], ' P4: ', pontos_calibracao[3])
                        pygame.display.quit()
                        camera.release()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        gameExit = True
                        cv2.destroyWindow("TELA DE CONTROLE")
                        grava_calibracao()
                        print('P1: ', pontos_calibracao[0], ' P2: ', pontos_calibracao[1], ' P3: ', pontos_calibracao[2], ' P4: ', pontos_calibracao[3])
                        pygame.display.quit()
                        camera.release()
            '''



#################################################################################
################################### FUNÇÕES #####################################
#################################################################################

def mousePoints(event, x, y, flags, params):
    # Função para capturar cliques do Mouse:
    global contador
    if event == cv2.EVENT_LBUTTONDOWN:
        pontos_calibracao[contador] = x, y
        contador = contador + 1

def posicao():

    # Função para determinar a posição do jogador na área de projeçao:
    # Transformação de Perspectiva:
    pts1 = np.float32([pontos_calibracao[0], pontos_calibracao[1], pontos_calibracao[2], pontos_calibracao[3]])
    pts2 = np.float32(
        [[0, 0], [largura_tela_controle, 0], [0, altura_tela_controle], [largura_tela_controle, altura_tela_controle]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    perspectiva = cv2.warpPerspective(tela_de_controle, matrix, (largura_tela_controle, altura_tela_controle))

    # Posição do jogador:
    p = (int(x_pose * largura_tela_controle), int(y_pose * altura_tela_controle))
    position_x = (matrix[0][0] * p[0] + matrix[0][1] * p[1] + matrix[0][2]) / (
    (matrix[2][0] * p[0] + matrix[2][1] * p[1] + matrix[2][2]))
    position_y = (matrix[1][0] * p[0] + matrix[1][1] * p[1] + matrix[1][2]) / (
    (matrix[2][0] * p[0] + matrix[2][1] * p[1] + matrix[2][2]))
    p_after = (int((position_x) * (relacao_largura)), int((position_y) * (relacao_altura)))

    return p_after

def delay():
    time.sleep(0.5)

def grava_calibracao():
    Config = ['Ponto 1 x', 'Ponto 1 y', 'Ponto 2 x', 'Ponto 2 y', 'Ponto 3 x', 'Ponto 3 y', 'Ponto 4 x', 'Ponto 4 y']
    Dados =  [pontos_calibracao[0][0], pontos_calibracao[0][1], pontos_calibracao[1][0], pontos_calibracao[1][1], pontos_calibracao[2][0], pontos_calibracao[2][1], pontos_calibracao[3][0], pontos_calibracao[3][1]]
    file = 'TTEA/calibracao.csv'

    with open(file, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, dialect='mydialect')
        csvwriter.writerow(Config)
        csvwriter.writerow(Dados)
