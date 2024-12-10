# instruction.py
class Instruction:
    def __init__(self, name, cycles):
        # Inicializa a instrução com um nome e um número de ciclos
        self.name = name  # Nome da instrução (ex: 'add', 'sub')
        self.cycles = cycles  # Número de ciclos necessários para executar a instrução

# Definindo as instruções e seus ciclos
instructions = {
    'add': Instruction('add', 1),  # Instrução 'add' leva 1 ciclo
    'sub': Instruction('sub', 1),  # Instrução 'sub' leva 1 ciclo
    'mul': Instruction('mul', 2),  # Instrução 'mul' leva 2 ciclos
    'load': Instruction('load', 3),  # Instrução 'load' leva 3 ciclos
    'store': Instruction('store', 3)  # Instrução 'store' leva 3 ciclos
}
