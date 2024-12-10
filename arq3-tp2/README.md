
# Descrição Detalhada do Código

## Estrutura Geral

Este projeto simula diferentes arquiteturas de CPU (Unidades de Processamento Central) e suas execuções de instruções em threads. As arquiteturas abordadas incluem CPU Escalar, Superescalar, SMT (Simultaneous Multithreading) e suas variações.

### Arquivos e Classes

1. **instruction.py**
    - Define a classe `Instruction` que representa uma instrução com nome e número de ciclos.
    - Contém um dicionário `instructions` que define algumas instruções padrão (`add`, `sub`, `mul`, `load`, `store`).

2. **thread.py**
    - Define a classe `Thread` que representa uma thread com uma lista de instruções.
    - Métodos:
        - `fetch_instruction()`: Busca a próxima instrução a ser executada.
        - `has_instructions()`: Verifica se há mais instruções a serem executadas.

3. **cpu.py**
    - Define a classe base `CPU` que contém a lógica comum a todas as arquiteturas de CPU.
    - Atributos:
        - `cycles`: Contador de ciclos.
        - `ipc`: Instruções por ciclo.
        - `instructions_executed`: Contador de instruções executadas.
        - `bubble_cycles`: Contador de ciclos de bolha.
        - `pipeline`: Lista para rastrear as instruções no pipeline.
        - `stages`: Estágios do pipeline.
        - `stage_cycles`: Duração de cada estágio.
        - `current_stage_instruction`: Instrução atual em cada estágio.
    - Métodos:
        - `execute_instruction(instruction, thread_id=0)`: Executa uma instrução específica e atualiza o pipeline.
        - `execute_instructions(threads)`: Executa as instruções em múltiplas threads.
        - `get_performance_metrics()`: Calcula as métricas de desempenho.
        - `print_pipeline()`: Imprime o estado do pipeline.

4. **scalar.py**
    - Define a classe `ScalarCPU` que herda de `CPU` e representa uma CPU escalar (executa uma instrução por ciclo).

5. **superscalar.py**
    - Define a classe `SuperscalarCPU` que herda de `CPU` e representa uma CPU superescalar (executa múltiplas instruções por ciclo).

6. **smt.py**
    - Define a classe `SMTCPU` que herda de `SuperscalarCPU` e implementa o SMT (Simultaneous Multithreading).

7. **bmt.py**
    - Define as classes `BMTCPUScalar` e `BMTSuperscalarCPU` que representam variações da CPU escalar e superescalar com uma abordagem diferente para executar instruções.

8. **imt.py**
    - Define as classes `IMTCPUScalar`, `IMTCPU` e `SuperscalarIMTCPU` que representam variações da CPU escalar e superescalar com outra abordagem para executar instruções.

## Lógica de Funcionamento

### Execução de Instruções

1. **Busca e Execução**:
    - As instruções são buscadas da lista de instruções da thread.
    - Dependendo da arquitetura, uma ou várias instruções podem ser buscadas e executadas por ciclo.

2. **Pipeline**:
    - Cada instrução passa por vários estágios no pipeline (`IF`, `ID`, `EX`, `MEM`, `WB`).
    - Cada estágio pode ter uma duração diferente, e o pipeline é atualizado a cada ciclo.

3. **Ciclos de Bolha**:
    - Ciclos de bolha são adicionados quando não há instruções a serem executadas ou quando há dependências de dados ou recursos que impedem a execução.

### Cálculo de Métricas

- **IPC (Instruções por Ciclo)**:
    - Calculado como o número de instruções executadas dividido pelo número total de ciclos.

- **Total de Ciclos**:
    - Contador de quantos ciclos a CPU levou para executar todas as instruções.

- **Ciclos de Bolha**:
    - Contador de quantos ciclos foram perdidos devido a bolhas no pipeline.

## Exemplo de Execução

### Simulação

- O arquivo principal realiza simulações usando diferentes arquiteturas de CPU e conjuntos de instruções.
- A função `run_simulation` é usada para inicializar a CPU e as threads, executar as instruções, imprimir o pipeline e calcular as métricas de desempenho.
- Exemplo de conjuntos de instruções:
    ```python
    instruction_set_1 = [instructions['add'], instructions['mul'], instructions['sub']]
    instruction_set_2 = [instructions['load'], instructions['store'], instructions['add']]
    ```

- Exemplo de chamada de simulação:
    ```python
    print("\nSimulacao - SMT")
    smt_superscalar = run_simulation(SMTCPU, [instruction_set_1, instruction_set_2], width=2).get_performance_metrics()
    ```

## Visualização dos Resultados

- Os resultados das simulações são visualizados usando gráficos de pizza para IPC, Total de Ciclos e Ciclos de Bolha.
- Exemplo de criação de gráficos:
    ```python
    plt.figure()
    plt.pie(ipc_values, labels=['IMT Escalar', 'BMT Escalar', 'IMT Superescalar', 'BMT Superescalar', 'SMT'], autopct=format_autopct(ipc_values))
    plt.title('IPC')
    plt.show()
    ```

