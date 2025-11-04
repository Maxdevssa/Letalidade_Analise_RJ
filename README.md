# Análise Exploratória da Letalidade Violenta no Rio de Janeiro (2024)

Este repositório contém uma análise exploratória dos dados de letalidade violenta na cidade do Rio de Janeiro, focando no ano de 2024. O projeto foi estruturado de forma modular para facilitar a manutenção, portabilidade e execução.

## Objetivo

Analisar os dados de letalidade violenta no município do Rio de Janeiro, identificando padrões mensais e a composição dos crimes que a integram no período mais recente disponível (2024).

## Estrutura do Projeto

O projeto é organizado em módulos, cada um com uma responsabilidade clara:

- `main.py`: Ponto de entrada que orquestra todo o fluxo de trabalho.
- `config.py`: Módulo de configuração que centraliza caminhos, nomes de colunas e parâmetros da análise.
- `data_cleaner.py`: Módulo responsável pela limpeza e preparação dos dados.
- `data_analyzer.py`: Módulo que realiza a análise exploratória dos dados (EDA).
- `visualizer.py`: Módulo encarregado de gerar as visualizações gráficas.
- `data/`: Diretório para armazenar os dados brutos e os dados limpos.
- `plots/`: Diretório onde as visualizações geradas são salvas.
- `requirements.txt`: Lista de dependências Python do projeto.

## Fonte dos Dados

Os dados são públicos e foram obtidos do portal de Dados Abertos do Instituto de Segurança Pública do Rio de Janeiro (ISP-RJ).

- **Dataset Principal:** `BaseMunicipioMensal.csv`

## Período Analisado

A análise concentra-se no ano de **2024**, conforme definido no arquivo `config.py`.

## Limitações

A principal limitação é a granularidade dos dados, que são agregados por município, impedindo uma análise detalhada por Área Integrada de Segurança Pública (AISP) ou bairros.

## Como Executar

O projeto foi refatorado para ser executado de forma simples e direta. Siga os passos abaixo:

1.  **Clone o Repositório:**
    ```bash
    git clone <URL_DO_REPOSITÓRIO>
    cd <NOME_DO_REPOSITÓRIO>
    ```

2.  **Crie e Ative um Ambiente Virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Linux/macOS
    # venv\Scripts\activate   # Windows
    ```

3.  **Instale as Dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute a Análise Completa:**
    Basta executar o script `main.py` para rodar todo o fluxo de trabalho (limpeza, análise e visualização):
    ```bash
    python main.py
    ```

Após a execução, os resultados serão gerados e salvos nos seguintes locais:
- **Dados Limpos:** `data/cleaned_rj_lethality_data.csv`
- **Resumo da Análise:** `eda_summary_pt.txt`
- **Gráficos:** Dentro da pasta `plots/`

## Resultados

Os principais resultados da análise para o Rio de Janeiro em 2024, gerados automaticamente pelo fluxo, incluem:

- **Total de Ocorrências:** 1.375 casos de letalidade violenta.
- **Tendência Mensal:** Picos em Maio (145) e Dezembro (142), com os menores valores em Janeiro/Fevereiro (94).
- **Composição dos Crimes:**
  - Homicídio Doloso: ~70%
  - Homicídio por Intervenção Policial: ~25%
  - Latrocínio: ~3%
  - Lesão Corporal Seguida de Morte: ~2%

Os gráficos com a evolução mensal e a composição detalhada podem ser encontrados na pasta `plots/`.
