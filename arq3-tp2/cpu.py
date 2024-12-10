from thread import Thread

class CPU:
    def __init__(self):
        # Inicializa os atributos da CPU
        self.cycles = 0  # Contador de ciclos
        self.ipc = 0  # Instruções por ciclo (IPC)
        self.instructions_executed = 0  # Contador de instruções executadas
        self.bubble_cycles = 0  # Contador de ciclos de bolha
        self.pipeline = []  # Lista para rastrear as instruções no pipeline
        self.stages = ['IF', 'ID', 'EX', 'MEM', 'WB']  # Estágios do pipeline
        self.stage_cycles = {'IF': 1, 'ID': 1, 'EX': 1, 'MEM': 1, 'WB': 1}  # Duração de cada estágio
        self.current_stage_instruction = {stage: None for stage in self.stages}  # Instrução atual em cada estágio

    def execute_instruction(self, instruction, thread_id=0):
        # Executa uma instrução específica e atualiza o pipeline
        stage_durations = {'IF': 1, 'ID': 1, 'EX': instruction.cycles, 'MEM': 1, 'WB': 1}  # Duração de cada estágio para esta instrução
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

        # Atualiza o contador de ciclos e instruções executadas
        self.cycles += max(stage_durations.values())
        self.instructions_executed += 1
        if instruction.cycles > 1:
            self.bubble_cycles += instruction.cycles - 1  # Adiciona ciclos de bolha se a instrução for longa

    def execute_instructions(self, threads):
        # Executa as instruções em múltiplas threads
        active_threads = len(threads)  # Número de threads ativas

        while any(thread.has_instructions() for thread in threads):
            instructions_to_execute = []
            for thread_id, thread in enumerate(threads):
                if thread.has_instructions() and len(instructions_to_execute) < self.width:
                    instruction = thread.fetch_instruction()  # Busca a próxima instrução da thread
                    instructions_to_execute.append((instruction, thread_id))

            if not instructions_to_execute:
                # Adiciona ciclos de bolha se não houver instruções a serem executadas
                self.cycles += 1
                self.bubble_cycles += 1
                self.pipeline.append({
                    'cycle': self.cycles,
                    'thread': None,
                    'stage': 'Bubble',
                    'instruction': 'Bubble'
                })
                continue

            for instruction, thread_id in instructions_to_execute:
                self.execute_instruction(instruction, thread_id)  # Executa cada instrução

    def get_performance_metrics(self):
        # Calcula as métricas de desempenho
        self.ipc = self.instructions_executed / self.cycles if self.cycles > 0 else 0  # Instruções por ciclo
        return {
            'IPC': self.ipc,
            'Total de Ciclos': self.cycles,
            'Bolhas': self.bubble_cycles
        }

    def print_pipeline_scalar(self):
        # Imprime o estado do pipeline em uma visão escalar
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

        # Printa o ultimo ciclo registrado
        print(f"{last_cycle:6} | {entry['thread']:6} | "
              f"{current_stages['IF']:^5} | {current_stages['ID']:^5} | "
              f"{current_stages['EX']:^5} | {current_stages['MEM']:^5} | "
              f"{current_stages['WB']:^5}")

    def print_pipeline(self):
        # Imprime o estado do pipeline em uma visão básica
        print("CICLOS\t|IF\t\t|ID\t\t|EX\t\t|MEM\t\t|WB")
        pipeline_by_cycle = {}

        for entry in self.pipeline:
            cycle = entry['cycle']
            if cycle not in pipeline_by_cycle:
                pipeline_by_cycle[cycle] = {}
            pipeline_by_cycle[cycle][entry['stage']] = f"{entry['thread']}:{entry['instruction']}"

        for cycle in sorted(pipeline_by_cycle.keys()):
            stages = pipeline_by_cycle[cycle]
            print(f"{cycle:6}\t|{stages.get('IF', ''):7}\t|{stages.get('ID', ''):7}\t|{stages.get('EX', ''):7}\t|{stages.get('MEM', ''):7}\t|{stages.get('WB', ''):7}")

    def print_pipeline_smt(self):
        # Imprime o estado do pipeline em uma visão SMT
        print("CICLOS\t|IF\t\t\t|ID\t\t\t|EX\t\t\t|MEM\t\t\t|WB")
        pipeline_by_cycle = {}

        for entry in self.pipeline:
            cycle = entry['cycle']
            if cycle not in pipeline_by_cycle:
                pipeline_by_cycle[cycle] = {stage: "" for stage in self.stages}
            thread_instruction = f"{entry['thread']}:{entry['instruction']}"
            if pipeline_by_cycle[cycle][entry['stage']]:
                pipeline_by_cycle[cycle][entry['stage']] += f", {thread_instruction}"
            else:
                pipeline_by_cycle[cycle][entry['stage']] = thread_instruction

        for cycle in sorted(pipeline_by_cycle.keys()):
            stages = pipeline_by_cycle[cycle]
            print(f"{cycle}\t|{stages.get('IF', ''):15}\t|{stages.get('ID', ''):15}\t|{stages.get('EX', ''):15}\t|{stages.get('MEM', ''):15}\t|{stages.get('WB', ''):15}")
