import random

# Classe que representa um soldado
class Soldado:
    def __init__(self, saudavel):
        self.saudavel = saudavel
        self.vivo = True

# Classe do Modelo de Propagação de Mortalidade durante a Primeira Guerra Mundial
class ModeloPropagacaoGuerra:
    def __init__(self, tamanhoCampoBatalha):
        self.populacao = []  # Matriz representando o campo de batalha
        self.geracaoAtual = 0

        # Taxa de mortalidade durante a guerra
        self.taxaMortalidade = 0.2

        for i in range(tamanhoCampoBatalha):
            self.populacao.append([])
            for j in range(tamanhoCampoBatalha):
                # Inicialmente, todos os soldados estão saudáveis e vivos
                self.populacao[i].append(Soldado(True))

    def propagarMortalidade(self):
        for i in range(len(self.populacao)):
            for j in range(len(self.populacao[i])):
                # Se o soldado estiver saudável e vivo, ele pode morrer com uma certa probabilidade
                if self.populacao[i][j].saudavel and self.populacao[i][j].vivo:
                    if random.random() < self.taxaMortalidade:
                        self.populacao[i][j].vivo = False

    def proximaGeracao(self):
        self.propagarMortalidade()
        self.geracaoAtual += 1

    def relatorio(self):
        totalSoldados = sum(1 for linha in self.populacao for soldado in linha)
        totalMortos = sum(1 for linha in self.populacao for soldado in linha if not soldado.vivo)
        taxaMortalidade = totalMortos / totalSoldados if totalSoldados > 0 else 0

        return totalSoldados, totalMortos, taxaMortalidade

    def simulation(self, geracoes):
        for i in range(geracoes):
            self.proximaGeracao()
            totalSoldados, totalMortos, taxaMortalidade = self.relatorio()
            print(f"Geração {i + 1}: Total de Soldados={totalSoldados}, Mortos={totalMortos}, Taxa de Mortalidade={taxaMortalidade:.2%}")


# Parâmetros da simulação
tamanhoCampoBatalha = 100  # Tamanho do campo de batalha
numeroDeGeracoes = 50  # Número de gerações a simular

# Executando a simulação
modelo = ModeloPropagacaoGuerra(tamanhoCampoBatalha)
modelo.simulation(numeroDeGeracoes)