from cpu import CPU

class SuperscalarCPU(CPU):
    def __init__(self, width):
        super().__init__()  # Inicializa a classe base CPU
        self.width = width  # Número de instruções que podem ser executadas em paralelo por ciclo

    def execute_instructions(self, threads):
        # Executa as instruções em múltiplas threads
        while any(thread.has_instructions() for thread in threads):
            instructions_to_execute = []  # Lista de instruções a serem executadas neste ciclo
            for thread_id, thread in enumerate(threads):
                if thread.has_instructions() and len(instructions_to_execute) < self.width:
                    instruction = thread.fetch_instruction()  # Busca a próxima instrução da thread
                    instructions_to_execute.append((instruction, thread_id))

            if not instructions_to_execute:
                # Adiciona ciclos de bolha se não houver instruções a serem executadas
                self.cycles += 1
                self.bubble_cycles += 1
                self.pipeline.append({
                    'cycle': self.cycles,  # Ciclo atual
                    'thread': None,  # Nenhuma thread específica
                    'stage': 'Bubble',  # Estágio de bolha
                    'instruction': 'Bubble'  # Instrução de bolha
                })
                continue

            # Executa cada instrução no conjunto de instruções a serem executadas
            for instruction, thread_id in instructions_to_execute:
                self.execute_instruction(instruction, thread_id)  # Executa a instrução
