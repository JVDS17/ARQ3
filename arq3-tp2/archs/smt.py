# smt.py
from superscalar import SuperscalarCPU

class SMTCPU(SuperscalarCPU):
    def __init__(self, width):
        super().__init__(width)  # Inicializa a classe base SuperscalarCPU

    def execute_instructions(self, threads):
        # Executa as instruções em múltiplas threads
        while any(thread.has_instructions() for thread in threads):
            instructions_to_execute = []

            # Busca instruções para cada thread até o limite de largura da CPU
            for thread_id, thread in enumerate(threads):
                if thread.has_instructions():
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

            # Executa instruções simultaneamente
            for cycle_offset in range(max([inst.cycles for inst, _ in instructions_to_execute])):
                for stage in self.stages:
                    for instruction, thread_id in instructions_to_execute:
                        if cycle_offset < instruction.cycles:
                            self.pipeline.append({
                                'cycle': self.cycles + cycle_offset,  # Ciclo em que a instrução entra neste estágio
                                'thread': thread_id,  # ID da thread executando a instrução
                                'stage': stage,  # Estágio atual
                                'instruction': instruction.name  # Nome da instrução
                            })
                            if stage == 'EX':
                                cycle_offset += instruction.cycles - 1  # Ajusta o deslocamento de ciclo para estágios longos

                self.cycles += 1  # Atualiza o contador de ciclos
                self.instructions_executed += len(instructions_to_execute)  # Atualiza o contador de instruções executadas
                self.bubble_cycles += sum(inst.cycles - 1 for inst, _ in instructions_to_execute if inst.cycles > 1)  # Adiciona ciclos de bolha para instruções longas
