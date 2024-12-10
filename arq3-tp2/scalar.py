# scalar.py
from cpu import CPU

class ScalarCPU(CPU):
    def __init__(self):
        super().__init__()  # Inicializa a classe base CPU

    def execute_instruction(self, instruction, thread_id=0):
        # Define a duração de cada estágio para a instrução
        stage_durations = {'IF': 1, 'ID': 1, 'EX': instruction.cycles, 'MEM': 1, 'WB': 1}

        for stage in self.stages:
            # Adiciona a instrução ao pipeline para cada estágio
            for _ in range(stage_durations[stage]):
                self.pipeline.append({
                    'cycle': self.cycles,  # Ciclo em que a instrução entra neste estágio
                    'thread': thread_id,  # ID da thread executando a instrução
                    'stage': stage,  # Estágio atual
                    'instruction': instruction.name  # Nome da instrução
                })
                self.cycles += 1  # Incrementa o contador de ciclos

        self.instructions_executed += 1  # Atualiza o contador de instruções executadas
        if instruction.cycles > 1:
            self.bubble_cycles += instruction.cycles - 1  # Adiciona ciclos de bolha se a instrução for longa

    def execute_instructions(self, threads):
        # Executa as instruções em múltiplas threads
        active_threads = len(threads)  # Número de threads ativas

        while any(thread.has_instructions() for thread in threads):
            for thread_id, thread in enumerate(threads):
                if thread.has_instructions():
                    instruction = thread.fetch_instruction()  # Busca a próxima instrução da thread
                    self.execute_instruction(instruction, thread_id)  # Executa a instrução

    def get_performance_metrics(self):
        # Calcula as métricas de desempenho
        self.ipc = self.instructions_executed / self.cycles if self.cycles > 0 else 0  # Instruções por ciclo (IPC)
        return {
            'IPC': self.ipc,
            'Total de Ciclos': self.cycles,
            'Bolhas': self.bubble_cycles
        }

    def print_pipeline(self):
        # Imprime o estado do pipeline
        print("CICLOS | THREAD |   IF  |  ID   |  EX   |  MEM  | WB")
        last_cycle = -1
        current_stages = {'IF': '', 'ID': '', 'EX': '', 'MEM': '', 'WB': ''}
        for entry in self.pipeline:
            if entry['cycle'] != last_cycle:
                if last_cycle != -1:
                    print(f"{last_cycle:6} | {entry['thread']:6} | "
                          f"{current_stages['IF']:^5} | {current_stages['ID']:^5} | "
                          f"{current_stages['EX']:^5} | {current_stages['MEM']:^5} | "
                          f"{current_stages['WB']:^5}")
                current_stages = {'IF': '', 'ID': '', 'EX': '', 'MEM': '', 'WB': ''}
                last_cycle = entry['cycle']

            current_stages[entry['stage']] = entry['instruction']

        # Imprime o último ciclo registrado
        print(f"{last_cycle:6} | {entry['thread']:6} | "
              f"{current_stages['IF']:^5} | {current_stages['ID']:^5} | "
              f"{current_stages['EX']:^5} | {current_stages['MEM']:^5} | "
              f"{current_stages['WB']:^5}")
