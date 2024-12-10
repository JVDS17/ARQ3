# imt.py
from scalar import ScalarCPU
from superscalar import SuperscalarCPU

class IMTCPUScalar(ScalarCPU):
    def __init__(self):
        super().__init__()  # Inicializa a classe base ScalarCPU

    def execute_instructions(self, threads):
        # Executa as instruções em múltiplas threads
        active_threads = len(threads)  # Número de threads ativas

        while any(thread.has_instructions() for thread in threads):
            for thread_id, thread in enumerate(threads):
                if thread.has_instructions():
                    instruction = thread.fetch_instruction()  # Busca a próxima instrução da thread
                    self.execute_instruction(instruction, thread_id)  # Executa a instrução

class IMTCPU(SuperscalarCPU):
    def __init__(self, width):
        super().__init__(width)  # Inicializa a classe base SuperscalarCPU
        self.current_thread = 0  # Índice da thread atual

    def execute_instructions(self, threads):
        # Executa as instruções em múltiplas threads
        while any(thread.has_instructions() for thread in threads):
            current_thread = threads[self.current_thread]
            if current_thread.has_instructions():
                instructions = []
                for _ in range(self.width):
                    if current_thread.has_instructions():
                        instructions.append(current_thread.fetch_instruction())  # Busca a próxima instrução da thread
                    else:
                        break

                blocked = False  # Flag para verificar bloqueios
                for instruction in instructions:
                    stage_durations = {'IF': 1, 'ID': 1, 'EX': instruction.cycles, 'MEM': 1, 'WB': 1}  # Duração de cada estágio
                    for stage in self.stages:
                        for _ in range(stage_durations[stage]):
                            self.pipeline.append({
                                'cycle': self.cycles,  # Ciclo em que a instrução entra neste estágio
                                'thread': self.current_thread,  # ID da thread executando a instrução
                                'stage': stage,  # Estágio atual
                                'instruction': instruction.name  # Nome da instrução
                            })
                            self.cycles += 1
                            # Verifica se há um bloqueio de recurso ou dependência de dados
                            if stage in ['MEM', 'EX'] and stage_durations[stage] > 1:
                                blocked = True
                    self.instructions_executed += 1  # Atualiza o contador de instruções executadas
                    if instruction.cycles > 1:
                        self.bubble_cycles += instruction.cycles - 1  # Adiciona ciclos de bolha se a instrução for longa
                if blocked:
                    self.current_thread = (self.current_thread + 1) % len(threads)  # Alterna para a próxima thread
            else:
                self.current_thread = (self.current_thread + 1) % len(threads)  # Alterna para a próxima thread


class SuperscalarIMTCPU(SuperscalarCPU):
    def __init__(self, width):
        super().__init__(width)  # Inicializa a classe base SuperscalarCPU
