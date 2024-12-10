# thread.py
class Thread:
    def __init__(self, instructions):
        # Inicializa a thread com uma lista de instruções
        self.instructions = instructions  # Lista de instruções a serem executadas
        self.instruction_pointer = 0  # Ponteiro para a instrução atual

    def fetch_instruction(self):
        # Busca a próxima instrução a ser executada
        if self.instruction_pointer < len(self.instructions):
            instruction = self.instructions[self.instruction_pointer]  # Obtém a instrução atual
            self.instruction_pointer += 1  # Incrementa o ponteiro da instrução
            return instruction  # Retorna a instrução
        return None  # Retorna None se não houver mais instruções

    def has_instructions(self):
        # Verifica se há mais instruções a serem executadas
        return self.instruction_pointer < len(self.instructions)
