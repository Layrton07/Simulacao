#
# Instituto Federal de Educação, Ciência e Tecnologia - IFPE
# Campus: Igarassu
# Curso: Sistemas para Internet
# Disciplina: Metodologia Científica
# Professor: Allan Lima - allan.lima@igarassu.ifpe.edu.br
#
# Código de Domínio Público, sinta-se livre para usá-lo, modificá-lo e redistribuí-lo.
#


# No caso de o interpretador não reconhecer a classe enum:
#
# 1) tente instalá-la: sudo pip install enum34
#
# 2) force a execução do código no Python 3: python3 randomWalkModel.py
import enum
import random


from PIL import Image # pip install Pillow

class Estado(enum.Enum):
    saudavel = 0
    doente = 1
    morto = 2
    imune = 3

class Individuo:
    def __init__(self, estado):
        self.estado = estado

class ModeloCaminhadaAleatoria:
    def __init__(self, tamanhoMatrizPopulacional): # se o parâmetro self for sempre explícito, podemos realmente dizer que o Python é uma linguagem orientada a objetos?
    
        self.populacao = []
        self.proximaPopulacao = []
        self.geracaoAtual = 0
        
        #
        #             saudável     doente     morto     imune
        # saudável     1.0         0.0        0.0       0.1
        # doente       0.1         0.2        0.3       0.4
        # morto        0.0         0.0        0.0       0.0
        # imune        0.1         0.0        0.0       0.0
        #
        # observe como não há transição do estado saudável
        self.probabilidadesTransicao = [[1.0, 0.0, 0.0, 0.1], [0.1, 0.2, 0.3, 0.4], [0.0, 0.0, 0.0, 0.0], [0.1, 0.0, 0.0, 0.0]]
        self.fatorContagio = 0.5

        for i in range(tamanhoMatrizPopulacional):
            self.populacao.append([])
            self.proximaPopulacao.append([])
            for j in range(tamanhoMatrizPopulacional):
                self.populacao[i].append(Individuo(Estado.saudavel))
                self.proximaPopulacao[i].append(Individuo(Estado.saudavel))

        # TODO: Colocar o primeiro caso em uma posição aleatória
        indiceInicial = int(tamanhoMatrizPopulacional / 2)
        self.populacao[indiceInicial][indiceInicial].estado = Estado.doente
        self.proximaPopulacao[indiceInicial][indiceInicial].estado = Estado.doente

    # TODO: Lidar com todas as transições como funções em vez de probabilidades
    def transicaoIndividual(self, linha, coluna):
        individuo = self.populacao[linha][coluna]

        # otimização
        if individuo.estado == Estado.morto:
            return

        # pessoas saudáveis interagem entre si
        if individuo.estado == Estado.saudavel:
            self.calcularInteracoesSociais(linha, coluna)

        # outros estados são tratados como uma máquina de estados
        else:
            probabilidades = self.probabilidadesTransicao[individuo.estado.value]
            numero = random.random()

            # print(individuo, individuo.estado.value)
            # print(numero, probabilidades)

            probabilidadeCumulativa = 0
            for indice in range(len(probabilidades)):
                probabilidadeCumulativa = probabilidadeCumulativa + probabilidades[indice]
                # print(probabilidadeCumulativa, probabilidades[j])

                if 0.0 < numero <= probabilidadeCumulativa:
                    # print('Transição de', self.populacao[index], 'para', Estado(j))

                    # Código de depuração para avisar se alguém ressuscitar
                    if individuo.estado == Estado.morto:
                        print("ERRO: TRANSIÇÃO DE MORTE", numero, probabilidadeCumulativa, indice, probabilidades[indice])

                    self.proximaPopulacao[linha][coluna].estado = Estado(indice)
                    break

    def calcularContatoDoente(self, individuo, vizinho):
        if individuo.estado == Estado.morto:
            print("ERRO: TRANSIÇÃO DE MORTE", individuo, vizinho)

        numero = random.random()

        if numero < self.fatorContagio:
            individuo.estado = Estado.doente

    def calcularInteracoesSociais(self, linha, coluna):
        linhaInicial = max(0, linha - 1)
        linhaFinal = min(linha + 2, len(self.populacao))
        
        for i in range(linhaInicial, linhaFinal):

            colunaInicial = max(0, coluna - 1)
            colunaFinal = min(coluna + 2, len(self.populacao[i]))

            for j in range(colunaInicial, colunaFinal):
                vizinho = self.populacao[i][j]

                efeitoDistanciaSocial = False # bool(random.getrandbits(1))

                if not efeitoDistanciaSocial:
                    if vizinho.estado == Estado.doente:
                        # Alterações são realizadas apenas na próxima população
                        self.calcularContatoDoente(self.proximaPopulacao[linha][coluna], vizinho)

    def proximaGeracao(self):
        for i in range(len(self.populacao)):
            for j in range(len(self.populacao[i])):
                self.transicaoIndividual(i, j)

        for i in range(len(self.populacao)):
            for j in range(len(self.populacao[i])):
                self.populacao[i][j].estado = self.proximaPopulacao[i][j].estado
                # print("test")

    def relatorio(self):
        estados = list(Estado)
        casos = []

        for s in estados:
            casos.append(0)

        for linha in self.populacao:
            for individuo in linha:
                casos[individuo.estado.value] += 1

        return casos

    def imprimirRelatorio(self, relatorio):
        for casos in relatorio:
            print(casos, '\t', end=' ')

        print()

    def cabecalhoLog(self, detalhado):
        if detalhado:
            estados = list(Estado)

            for estado in estados:
                print(estado, '\t', end=' ')