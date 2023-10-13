#
# Instituto Federal de Educação, Ciência e Tecnologia - IFPE
# Campus: Igarassu
# Curso: Sistemas para Internet
# Disciplina: Metodologia Científica
# Professor: Allan Lima - allan.lima@igarassu.ifpe.edu.br
#
# Código de Domínio Público, sinta-se livre para usá-lo, modificá-lo e redistribuí-lo.
#

# Caso o interpretador não reconheça a classe enum:
#
# 1) Tente instalá-la: sudo pip install enum34
#
# 2) Force a execução do código no Python 3: python3 randomWalkModel.py

#import PIL

import enum
import random

from PIL import Image  # pip install Pillow


class State(enum.Enum):
    healthy = 0
    sick = 1
    dead = 2
    immune = 3
    guerra = 4

class Individual:
    def __init__(self, state):
        self.state = state

class RandomWalkModel:
    def __init__(self, populationMatrixSize):
        self.population = []
        self.nextPopulation = []
        self.currentGeneration = 0

        # Tabela de probabilidades de transição:
        #       healthy sick    dead   immune  guerra
        # healthy 0.5    0.0     0.0    0.0     0.5
        # sick    0.1    0.2     0.1    0.2     0.4
        # dead    0.0    0.0     0.0    0.0     0.0
        # immune  0.1    0.0     0.0    0.0     0.5
        # guerra  0.0    0.0     0.0    0.0     0.0
        #
        # Observe que não há transição do estado "healthy"
        self.transitionProbabilities = [
            [1.0, 0.0, 0.0, 0.1, 0.5],
            [0.1, 0.2, 0.1, 0.2, 0.4],
            [0.0, 0.0, 0.0, 0.0, 0.0],
            [0.1, 0.0, 0.0, 0.0, 0.5],
            [0.0, 0.0, 0.0, 0.0, 0.0]
        ]
        self.contagionFactor = 0.5

        for i in range(populationMatrixSize):
            self.population.append([])
            self.nextPopulation.append([])
            for j in range(populationMatrixSize):
                self.population[i].append(Individual(State.healthy))
                self.nextPopulation[i].append(Individual(State.healthy))

        # TODO: Coloque o primeiro caso em uma posição aleatória
        startIndex = int(populationMatrixSize / 2)
        self.population[startIndex][startIndex].state = State.sick
        self.nextPopulation[startIndex][startIndex].state = State.sick

    # TODO: Lide com todas as transições como uma função em vez de probabilidades
    def individualTransition(self, line, column):
        individual = self.population[line][column]

        # Otimização
        if individual.state == State.dead:
            return

        # Pessoas saudáveis interagem entre si
        if individual.state == State.healthy:
            self.computeSocialInteractions(line, column)

        # Outros estados são tratados como uma máquina de estados
        else:
            probabilities = self.transitionProbabilities[individual.state.value]
            number = random.random()

            cumulativeProbability = 0
            for index in range(len(probabilities)):
                cumulativeProbability += probabilities[index]

                if number > 0.0 and number <= cumulativeProbability:
                    self.nextPopulation[line][column].state = State(index)
                    break

    def computeSickContact(self, individual, neighbour):
        if individual.state == State.dead:
            print("ERRO: TRANSIÇÃO DE MORTE ", individual, neighbour)

        number = random.random()

        if number < self.contagionFactor:
            individual.state = State.sick

    def computeSocialInteractions(self, line, column):
        initialLine = max(0, line - 1)
        finalLine = min(line + 2, len(self.population))

        for i in range(initialLine, finalLine):
            initialColumn = max(0, column - 1)
            finalColumn = min(column + 2, len(self.population[i]))

            for j in range(initialColumn, finalColumn):
                neighbour = self.population[i][j]

                socialDistanceEffect = False  # bool(random.getrandbits(1))

                if not socialDistanceEffect:
                    if neighbour.state == State.sick:
                        self.computeSickContact(self.nextPopulation[line][column], neighbour)

    def nextGeneration(self):
        for i in range(len(self.population)):
            for j in range(len(self.population[i])):
                self.individualTransition(i, j)

        for i in range(len(self.population)):
            for j in range(len(self.population[i])):
                self.population[i][j].state = self.nextPopulation[i][j].state

    def report(self):
        states = list(State)
        cases = []

        for s in states:
            cases.append(0)

        for line in self.population:
            for individual in line:
                cases[individual.state.value] += 1

        return cases

    def printReport(self, report):
        for cases in report:
            print(cases, '\t', end=' ')

        print()

    def logHeaders(self, verbose):
        if verbose:
            states = list(State)

            for state in states:
                print(state, '\t', end=' ')

            print()

    def logReport(self, verbose):
        if verbose:
            report = self.report()
            self.printReport(report)

    def simulation(self, generations, verbose):
        self.logHeaders(verbose)

        self.logReport(verbose)

        for i in range(generations):
            self.nextGeneration()
            self.logReport(verbose)
            if i == generations -1:
                model.printImage(i)

    def numberOfDeaths(self):
        deaths = 0

        for line in self.population:
            for individual in line:
                if individual.state == State.dead :
                    deaths += 1
                elif individual.state == State.guerra:
                    deaths += 1

        return deaths

    def logPopulation(self, population):
        for i in range(len(population)):
            for j in range(len(population)):
                print(population[i][j].state.value, '\t', end=' ')
            print()
        print()

    def printImage(self, name):
        lines = len(self.population)
        columns = len(self.population[0])
        img = Image.new(mode="RGB", size=(columns, lines))

        for i in range(lines):
            for j in range(columns):
                if self.population[i][j].state == State.healthy:
                    img.putpixel((i, j), (0, 256, 0))
                elif self.population[i][j].state == State.sick:
                    img.putpixel((i, j), (256, 256, 0))
                elif self.population[i][j].state == State.dead:
                    img.putpixel((i, j), (256, 0, 0))
                elif self.population[i][j].state == State.immune:
                    img.putpixel((i, j), (0, 0, 256))
                elif self.population[i][j].state == State.guerra:
                    img.putpixel((i, j), (0, 0, 0))
                else:
                    print("ESTADO INVÁLIDO")

        img.save("gen" + str(name) + ".png")

numberOfRuns = 1000
gridSize = 100
numberOfGenerations = 52  # número de semanas em um ano

for i in range(0, numberOfRuns):
    model = RandomWalkModel(gridSize)
    model.simulation(numberOfGenerations, False)
    print(model.numberOfDeaths())
