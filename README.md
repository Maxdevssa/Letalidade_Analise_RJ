# Análise Exploratória da Letalidade Violenta - Rio de Janeiro (2024)

Este repositório contém uma análise exploratória dos dados de letalidade violenta na cidade do Rio de Janeiro, focando no ano de 2024.

## Objetivo

Analisar os dados de letalidade violenta na cidade do Rio de Janeiro, identificando padrões mensais e a composição dos crimes que a integram no período mais recente disponível (2024).

## Fonte dos Dados

Os dados utilizados nesta análise são públicos e foram obtidos diretamente do portal de Dados Abertos do Instituto de Segurança Pública do Rio de Janeiro (ISP-RJ).

*   **Link Principal ISP-RJ:** [https://www.ispdados.rj.gov.br/](https://www.ispdados.rj.gov.br/)
*   **Dataset Utilizado:** `BaseMunicipioMensal.csv` (Estatísticas de segurança: série histórica mensal por município desde 2014).
*   **Arquivo Auxiliar:** `Relacao_RISPxAISPxCISP.csv` (Relação das Regiões, Áreas e Circunscrições Integradas de Segurança Pública).

## Período Analisado

A análise concentra-se exclusivamente no ano de **2024**, que representa o último ano completo com dados consolidados disponíveis no dataset `BaseMunicipioMensal.csv` no momento da coleta (Abril de 2025).

## Limitações

*   **Granularidade Geográfica:** A principal limitação desta análise reside na granularidade dos dados. O arquivo `BaseMunicipioMensal.csv` agrega os dados por município, **não permitindo uma análise detalhada por Área Integrada de Segurança Pública (AISP)**. Uma AISP é uma divisão territorial utilizada pela Secretaria de Segurança Pública do RJ para fins de planejamento e policiamento, agrupando bairros sob o comando de um batalhão da PM e delegacias da Polícia Civil. Sem dados desagregados por AISP ou CISP (Circunscrição Integrada de Segurança Pública - delegacia), não foi possível identificar a distribuição espacial da letalidade dentro da cidade do Rio de Janeiro.
*   **Proxy para Violência:** A análise foca na "letalidade violenta" conforme definida pelo ISP-RJ (soma de homicídio doloso, latrocínio, lesão corporal seguida de morte e homicídio por intervenção de agente do Estado). Este é um indicador importante, mas não abrange toda a complexidade da violência urbana.
*   **Mortes de Policiais:** Os dados públicos padrão utilizados não permitem isolar especificamente as mortes de policiais em serviço ou fora dele dentro das categorias de letalidade violenta de forma direta e inequívoca, embora exista uma coluna separada (`pol_militares_mortos_serv`, `pol_civis_mortos_serv`) que não foi o foco principal desta análise específica de letalidade violenta geral.

## Processo de Análise

1.  **Coleta:** Download dos arquivos `BaseMunicipioMensal.csv` e `Relacao_RISPxAISPxCISP.csv` do portal ISP-RJ.
2.  **Limpeza e Preparação:**
    *   Carregamento dos dados utilizando a biblioteca `pandas`.
    *   Correção da codificação de caracteres (utilizado `latin1`).
    *   Limpeza de nomes de colunas (remoção de espaços extras).
    *   Filtragem dos dados para incluir apenas o município do Rio de Janeiro (coluna `fmun`).
    *   Seleção do período de análise (ano de 2024).
    *   Seleção das colunas relevantes: `ano`, `mes`, `fmun`, `hom_doloso`, `latrocinio`, `lesao_corp_morte`, `hom_por_interv_policial`.
    *   Verificação e tratamento de valores ausentes (preenchidos com 0 nas colunas numéricas de crimes).
    *   Conversão de tipos de dados.
    *   Criação da coluna `letalidade_violenta` (soma dos componentes).
    *   Criação de uma coluna `date` para facilitar análises temporais.
    *   Constatação da impossibilidade de mapeamento direto para AISP com os dados disponíveis.
    *   Salvamento do dataset limpo em `data/cleaned_rj_lethality_data.csv`.
3.  **Análise Exploratória (EDA):**
    *   Cálculo do total de ocorrências de letalidade violenta em 2024.
    *   Análise da evolução mensal das ocorrências.
    *   Identificação dos meses com maior e menor número de casos.
    *   Análise da composição percentual da letalidade violenta por tipo de crime.
    *   Salvamento do resumo da análise em `eda_summary.txt`.
4.  **Visualização:**
    *   Criação de gráficos utilizando `matplotlib` e `seaborn` para ilustrar os achados da EDA:
        *   Gráfico de linha da evolução mensal.
        *   Gráfico de barras do total anual.
        *   Gráfico de barras empilhadas da composição mensal.
        *   Gráfico de pizza da composição geral.
    *   Salvamento dos gráficos na pasta `plots/`.
5.  **Relatório:** Elaboração de um relatório (`report.md`) detalhando o processo, os resultados, os insights e as limitações da análise.

## Resultados

Os principais resultados da análise para o Rio de Janeiro em 2024 foram:

*   **Total de Ocorrências:** 1.375 casos de letalidade violenta.
*   **Tendência Mensal:** Flutuação ao longo do ano, com picos em Maio (145) e Dezembro (142), e menores valores em Janeiro/Fevereiro (94).
*   **Composição:**
    *   Homicídio Doloso: 70.0% (963 casos)
    *   Homicídio por Intervenção Policial: 24.7% (339 casos)
    *   Latrocínio: 3.2% (44 casos)
    *   Lesão Corporal Seguida de Morte: 2.1% (29 casos)

Os gráficos gerados podem ser encontrados na pasta `plots/`:

*   `rj_lethality_monthly_evolution_2024.png`
*   `rj_lethality_total_2024.png`
*   `rj_lethality_monthly_composition_2024.png`
*   `rj_lethality_overall_composition_2024.png`

## Questões para Investigação Futura

*   Qual a distribuição geográfica (por AISP/CISP/Bairro) da letalidade violenta dentro do Rio de Janeiro?
*   Como a letalidade violenta em 2024 se compara com anos anteriores?
*   Quais fatores podem explicar os picos mensais observados (eventos, operações policiais, etc.)?
*   Existe correlação entre a letalidade violenta e outros indicadores socioeconômicos ou criminais?

## Como Executar

1.  Clone o repositório.
2.  Certifique-se de ter Python 3 e `pip` instalados.
3.  Crie um ambiente virtual: `python3 -m venv venv`
4.  Ative o ambiente virtual: `source venv/bin/activate` (Linux/macOS) ou `venv\Scripts\activate` (Windows)
5.  Instale as dependências: `pip install pandas matplotlib seaborn`
6.  Execute os scripts na ordem:
    *   `python clean_data.py`
    *   `python eda_analysis.py`
    *   `python create_visualizations.py`

Os resultados (dataset limpo, resumo da EDA, gráficos e relatório) estarão nas pastas `data/`, `plots/` e no diretório raiz.

