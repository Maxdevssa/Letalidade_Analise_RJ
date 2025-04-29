# Análise Exploratória da Letalidade Violenta na Cidade do Rio de Janeiro (2024)

## Introdução

Este relatório apresenta uma análise exploratória dos dados de letalidade violenta na cidade do Rio de Janeiro, referente ao ano de 2024. O objetivo principal foi identificar padrões e tendências nas ocorrências criminais que compõem a letalidade violenta, utilizando os dados mais recentes disponíveis publicamente.

Os dados foram obtidos do portal de Dados Abertos do Instituto de Segurança Pública do Rio de Janeiro (ISP-RJ), especificamente o arquivo `BaseMunicipioMensal.csv`, que contém estatísticas criminais agregadas mensalmente por município. O período de análise foca exclusivamente no ano de 2024, que representa o último ano completo com dados consolidados no momento da análise.

É crucial destacar uma limitação importante desta análise: o dataset `BaseMunicipioMensal.csv` não fornece desagregação dos dados por Área Integrada de Segurança Pública (AISP). Consequentemente, a análise se concentra no nível agregado do município do Rio de Janeiro, não sendo possível identificar variações ou concentrações específicas em diferentes AISPs, como originalmente planejado. A análise por AISP exigiria um dataset com granularidade geográfica maior, como o `BaseDelegaciaMes.csv` ou dados diretamente agregados por AISP.

## Principais Achados

A análise dos dados de 2024 para o município do Rio de Janeiro revelou os seguintes pontos:

### Total de Ocorrências

No ano de 2024, foram registradas um total de **1.375 ocorrências** classificadas como letalidade violenta na cidade do Rio de Janeiro. Este número representa a soma dos seguintes crimes: homicídio doloso, latrocínio (roubo seguido de morte), lesão corporal seguida de morte e homicídio por intervenção de agente do Estado.

### Evolução Mensal

A distribuição mensal das ocorrências de letalidade violenta apresentou variações ao longo de 2024. Os meses de **maio** e **dezembro** registraram os maiores números de ocorrências, com 145 e 142 casos, respectivamente. Por outro lado, os meses de **janeiro** e **fevereiro** apresentaram os menores índices, ambos com 94 ocorrências. Observa-se uma flutuação considerável, com picos no meio e no final do ano, sugerindo possíveis influências sazonais ou eventos específicos que podem ter impactado a criminalidade nesses períodos.

### Composição da Letalidade Violenta

Ao analisar a composição da letalidade violenta, verifica-se que o **homicídio doloso** foi o componente predominante, respondendo por **70,04%** do total de ocorrências (963 casos). Em segundo lugar, aparece o **homicídio por intervenção de agente do Estado**, com **24,65%** das ocorrências (339 casos). O **latrocínio** representou **3,20%** (44 casos) e a **lesão corporal seguida de morte** correspondeu a **2,11%** (29 casos).

## Insights e Implicações

Os resultados desta análise, embora limitados à escala municipal, oferecem alguns insights relevantes para a gestão da segurança pública no Rio de Janeiro:

1.  **Predominância do Homicídio Doloso:** A alta concentração de homicídios dolosos (mais de 70%) como principal componente da letalidade violenta reforça a necessidade de políticas focadas na prevenção e investigação deste tipo específico de crime. Estratégias direcionadas para as causas e contextos desses homicídios são fundamentais.
2.  **Relevância da Intervenção Policial:** Os homicídios decorrentes de intervenção policial representam quase um quarto da letalidade violenta registrada. Este dado sublinha a importância do debate contínuo sobre protocolos de atuação, treinamento e transparência nas ações policiais, buscando a redução da letalidade em confrontos.
3.  **Flutuação Mensal:** As variações mensais, com picos em maio e dezembro, podem indicar a necessidade de reforço no policiamento ou em ações preventivas durante períodos específicos do ano. Investigações adicionais poderiam correlacionar esses picos com eventos sazonais, feriados ou operações de segurança.
4.  **Necessidade de Dados Granulares:** A impossibilidade de realizar a análise por AISP evidencia a importância de disponibilizar e utilizar dados com maior granularidade geográfica para um planejamento de segurança pública mais eficaz. A identificação de áreas críticas (hotspots) dentro do município permitiria uma alocação mais eficiente de recursos e o desenvolvimento de estratégias localizadas.

## Visualizações

Para complementar esta análise, foram gerados os seguintes gráficos (disponíveis como arquivos separados):

1.  **Gráfico de Linha:** Evolução mensal do total de ocorrências de letalidade violenta em 2024.
2.  **Gráfico de Barras:** Total de ocorrências de letalidade violenta em 2024.
3.  **Gráfico de Barras Empilhadas:** Composição mensal da letalidade violenta por tipo de crime em 2024.
4.  **Gráfico de Pizza:** Composição percentual geral da letalidade violenta por tipo de crime em 2024.

## Conclusão

A análise dos dados de letalidade violenta para o Rio de Janeiro em 2024 indica um cenário onde o homicídio doloso e as mortes por intervenção policial são os principais componentes. A flutuação mensal sugere a existência de fatores temporais que influenciam esses índices. A principal limitação foi a ausência de dados por AISP, impedindo uma análise espacial mais detalhada dentro da cidade.

Para futuras investigações, recomenda-se fortemente a busca por datasets que permitam a análise por AISP ou CISP (Circunscrição Integrada de Segurança Pública), possibilitando a identificação de áreas com maior concentração de ocorrências e o direcionamento de políticas públicas de forma mais precisa. Além disso, a análise de séries históricas mais longas e a correlação com outros indicadores socioeconômicos poderiam fornecer insights mais profundos sobre as dinâmicas da violência letal na cidade.

