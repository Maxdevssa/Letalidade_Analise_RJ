# -*- coding: utf-8 -*-
"""
Módulo de Configuração para a Análise de Letalidade do Rio de Janeiro.

Centraliza todos os caminhos de arquivos, nomes de colunas e parâmetros
para facilitar a manutenção e a portabilidade do projeto.
"""
import os

# --- Diretórios Base ---
# Obtém o diretório raiz do projeto (o diretório pai deste arquivo de config)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define os diretórios de dados e plots de forma relativa ao diretório base
DATA_DIR = os.path.join(BASE_DIR, "data")
PLOTS_DIR = os.path.join(BASE_DIR, "plots")

# --- Arquivos de Dados ---
# Arquivos de entrada
CRIME_DATA_FILE = os.path.join(DATA_DIR, "BaseMunicipioMensal.csv")
AISP_MAP_FILE = os.path.join(DATA_DIR, "Relacao_RISPxAISPxCISP.csv")

# Arquivos de saída
CLEANED_DATA_FILE = os.path.join(DATA_DIR, "cleaned_rj_lethality_data.csv")
OUTPUT_SUMMARY_FILE = os.path.join(BASE_DIR, "eda_summary_pt.txt")

# --- Parâmetros da Análise ---
# Ano alvo para a análise. Pode ser ajustado para analisar outros anos.
# Se definido como None, o script de limpeza tentará determinar o último ano completo.
TARGET_YEAR = 2024
TARGET_MUNICIPALITY = "RIO DE JANEIRO"

# --- Nomes de Colunas ---
# Colunas de crimes que compõem a "letalidade violenta"
LETHALITY_COLS = [
    "hom_doloso",                # Homicídio doloso
    "latrocinio",                # Roubo seguido de morte
    "lesao_corp_morte",          # Lesão corporal seguida de morte
    "hom_por_interv_policial"    # Homicídio por intervenção de agente do Estado
]

# Coluna que representa o município no dataset original
MUNICIPALITY_COL = "fmun"

# Coluna para a data criada durante a limpeza
DATE_COL = "date"

# Coluna para o ano
YEAR_COL = "ano"

# Coluna para o mês
MONTH_COL = "mes"

# Coluna agregada para a letalidade violenta
LETHALITY_TOTAL_COL = "letalidade_violenta"
