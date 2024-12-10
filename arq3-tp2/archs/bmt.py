# bmt.py
from scalar import ScalarCPU
from superscalar import SuperscalarCPU

class BMTCPUScalar(ScalarCPU):
    def __init__(self):
        super().__init__()  # Inicializa a classe base ScalarCPU
        self.current_thread = 0  # Índice da thread atual

    def execute_instruction(self, instruction, thread_id):
        # Executa uma instrução específica e atualiza o pipeline
        stage_durations = {'IF': 1, 'ID': 1, 'EX': instruction.cycles, 'MEM': 1, 'WB': 1}  # Duração de cada estágio
        blocked = False  # Flag para verificar bloqueios de recursos ou dependência de dados

        for stage in self.stages:
            # Adiciona a instrução ao pipeline para cada estágio
            for _ in range(stage_durations[stage]):
                self.pipeline.append({
                    'cycle': self.cycles,  # Ciclo em que a instrução entra neste estágio
                    'thread': thread_id,  # ID da thread executando a instrução
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

        return blocked  # Retorna se houve bloqueio

    def execute_instructions(self, threads):
        # Executa as instruções em múltiplas threads
        while any(thread.has_instructions() for thread in threads):
            current_thread = threads[self.current_thread]
            if current_thread.has_instructions():
                instruction = current_thread.fetch_instruction()  # Busca a próxima instrução da thread
                blocked = self.execute_instruction(instruction, self.current_thread)  # Executa a instrução
                if blocked:
                    self.current_thread = (self.current_thread + 1) % len(threads)  # Alterna para a próxima thread
            else:
                self.current_thread = (self.current_thread + 1) % len(threads)  # Alterna para a próxima thread


class BMTSuperscalarCPU(SuperscalarCPU):
    def __init__(self, width):
        super().__init__(width)  # Inicializa a classe base SuperscalarCPU
        self.current_thread = 0  # Índice da thread atual

    def execute_instruction(self, instruction, thread_id):
        # Executa uma instrução específica e atualiza o pipeline
        stage_durations = {'IF': 1, 'ID': 1, 'EX': instruction.cycles, 'MEM': 1, 'WB': 1}  # Duração de cada estágio
        cycle_offset = 0  # Deslocamento de ciclo para o início de cada estágio

        for stage in self.stages:
            # Adiciona a instrução ao pipeline para cada estágio
            for _ in range(stage_durations[stage]):
                self.pipeline.append({
                    'cycle': self.cycles + cycle_offset,  # Ciclo em que a instrução entra neste estágio
                    'thread': thread_id,  # ID da thread executando a instrução
                    'stage': stage,  # Estágio atual
                    'instruction': instruction.name  # Nome da instrução
                })
                cycle_offset += 1

        self.cycles += max(stage_durations.values())  # Atualiza o contador de ciclos
        self.instructions_executed += 1  # Atualiza o contador de instruções executadas
        if instruction.cycles > 1:
            self.bubble_cycles += instruction.cycles - 1  # Adiciona ciclos de bolha se a instrução for longa

    def execute_instructions(self, threads):
        # Executa as instruções em múltiplas threads
        while any(thread.has_instructions() for thread in threads):
            current_thread = threads[self.current_thread]
            blocked = False  # Flag para verificar bloqueios

            while current_thread.has_instructions() and not blocked:
                instruction = current_thread.fetch_instruction()  # Busca a próxima instrução da thread
                self.execute_instruction(instruction, self.current_thread)  # Executa a instrução
                if instruction.cycles > 1:
                    blocked = True  # Verifica se a instrução causa bloqueio
            
            self.current_thread = (self.current_thread + 1) % len(threads)  # Alterna para a próxima thread
