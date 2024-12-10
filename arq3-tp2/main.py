from matplotlib import pyplot as plt
from instruction import instructions
from archs.smt import SMTCPU
from archs.imt import IMTCPUScalar, SuperscalarIMTCPU
from archs.bmt import BMTSuperscalarCPU, BMTCPUScalar
from thread import Thread

def run_simulation(cpu_class, instruction_sets, width=None):
    # Inicializa as threads com os conjuntos de instruções fornecidos
    threads = [Thread(instructions) for instructions in instruction_sets]
    if width:
        cpu = cpu_class(width)  # Inicializa a CPU com largura se fornecido
    else:
        cpu = cpu_class()  # Inicializa a CPU sem largura
    cpu.execute_instructions(threads)  # Executa as instruções nas threads
    if cpu_class == SMTCPU:
        cpu.print_pipeline_smt()  # Imprime o pipeline para SMT
    elif cpu_class == IMTCPUScalar or cpu_class == BMTCPUScalar:
        cpu.print_pipeline_scalar()  # Imprime o pipeline para CPUs escalares
    else:
        cpu.print_pipeline()  # Imprime o pipeline para outras CPUs
    metrics = cpu.get_performance_metrics()  # Obtém as métricas de desempenho
    print(metrics)

    return cpu

"""
add = 1
sub = 1
mul = 2
load = 3
store = 3
"""

# Definindo os conjuntos de instruções
instruction_set_1 = [instructions['add'], instructions['mul'], instructions['sub']]
instruction_set_2 = [instructions['load'], instructions['store'], instructions['add']]

# Executando as simulações
print("\nSimulacao - IMT Escalar")
imt_scalar = run_simulation(IMTCPUScalar, [instruction_set_1, instruction_set_2]).get_performance_metrics()

print("\nSimulacao - BMT Escalar")
bmt_scalar = run_simulation(BMTCPUScalar, [instruction_set_1, instruction_set_2]).get_performance_metrics()

print("\nSimulacao - IMT Superescalar")
imt_superscalar = run_simulation(SuperscalarIMTCPU, [instruction_set_1, instruction_set_2], width=2).get_performance_metrics()

print("\nSimulacao - BMT Superscalar")
bmt_superscalar = run_simulation(BMTSuperscalarCPU, [instruction_set_1, instruction_set_2], width=2).get_performance_metrics()

print("\nSimulacao - SMT")
smt_superscalar = run_simulation(SMTCPU, [instruction_set_1, instruction_set_2], width=2).get_performance_metrics()

# Função para formatar os valores na fatia da pizza
def format_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = (pct * total / 100.0)
        return f'{val:.2f} ({pct:.1f}%)'
    return my_autopct

# Dados para os gráficos
ipc_values = [imt_scalar['IPC'], bmt_scalar['IPC'], imt_superscalar['IPC'], bmt_superscalar['IPC'], smt_superscalar['IPC']]
cycles_values = [imt_scalar['Total de Ciclos'], bmt_scalar['Total de Ciclos'], imt_superscalar['Total de Ciclos'], bmt_superscalar['Total de Ciclos'], smt_superscalar['Total de Ciclos']]
bubble_values = [imt_scalar['Bolhas'], bmt_scalar['Bolhas'], imt_superscalar['Bolhas'], bmt_superscalar['Bolhas'], smt_superscalar['Bolhas']]

# Plotando os gráficos
plt.figure()
plt.pie(ipc_values, labels=['IMT Escalar', 'BMT Escalar', 'IMT Superescalar', 'BMT Superescalar', 'SMT'], autopct=format_autopct(ipc_values))
plt.title('IPC')
plt.show()

plt.figure()
plt.pie(cycles_values, labels=['IMT Escalar', 'BMT Escalar', 'IMT Superescalar', 'BMT Superescalar', 'SMT'], autopct=format_autopct(cycles_values))
plt.title('Total de Ciclos')
plt.show()

plt.figure()
plt.pie(bubble_values, labels=['IMT Escalar', 'BMT Escalar', 'IMT Superescalar', 'BMT Superescalar', 'SMT'], autopct=format_autopct(bubble_values))
plt.title('Bolhas')
plt.show()
