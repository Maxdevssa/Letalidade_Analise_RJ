# -*- coding: utf-8 -*-
"""
Script para Análise Exploratória de Dados (EDA) dos dados de letalidade do Rio de Janeiro (2024).
"""
import pandas as pd
import os

# Define os caminhos dos arquivos
DATA_DIR = "/home/ubuntu/rio_lethality_analysis/data"
CLEANED_DATA_FILE = os.path.join(DATA_DIR, "cleaned_rj_lethality_data.csv")
OUTPUT_SUMMARY_FILE = os.path.join("/home/ubuntu/rio_lethality_analysis", "eda_summary_pt.txt") # Salva resumo traduzido

# --- Carregar Dados Limpos ---
try:
    df = pd.read_csv(CLEANED_DATA_FILE, sep=";", parse_dates=["date"], encoding="utf-8")
    print(f"Arquivo {os.path.basename(CLEANED_DATA_FILE)} carregado com sucesso. Shape: {df.shape}")
    print("\nInformações dos Dados:")
    df.info()
    print("\nPrimeiras 5 linhas:")
    print(df.head())
except FileNotFoundError:
    print(f"Erro: Arquivo de dados limpos não encontrado em {CLEANED_DATA_FILE}")
    exit()
except Exception as e:
    print(f"Erro ao carregar dados limpos: {e}")
    exit()

# --- Realizar EDA --- #

analysis_summary = []
analysis_summary.append("--- Análise Exploratória de Dados (EDA) - Letalidade Violenta no Rio de Janeiro (2024) ---")
analysis_summary.append(f'Período Analisado: Ano de {df["ano"].iloc[0]}')
analysis_summary.append(f"Fonte dos Dados: ISP-RJ (BaseMunicipioMensal.csv)")
analysis_summary.append("Município: Rio de Janeiro")
analysis_summary.append("\n---\n")

# 1. Total de Letalidade Violenta no Ano
total_lethality = df["letalidade_violenta"].sum()
analysis_summary.append(f'1. Total de Ocorrências de Letalidade Violenta em {df["ano"].iloc[0]}: {total_lethality}')
print(f'\nTotal de Letalidade Violenta em {df["ano"].iloc[0]}: {total_lethality}')

# 2. Evolução Mensal da Letalidade Violenta
monthly_lethality = df.groupby("mes")["letalidade_violenta"].sum().reset_index()
analysis_summary.append("\n2. Evolução Mensal da Letalidade Violenta:")
analysis_summary.append(monthly_lethality.to_string(index=False))
print("\nEvolução Mensal:")
print(monthly_lethality)

# Identifica mês com maior e menor letalidade
max_month = monthly_lethality.loc[monthly_lethality["letalidade_violenta"].idxmax()]
min_month = monthly_lethality.loc[monthly_lethality["letalidade_violenta"].idxmin()]
analysis_summary.append(f'   - Mês com maior letalidade: {int(max_month["mes"])} ({int(max_month["letalidade_violenta"])}) ocorrências')
analysis_summary.append(f'   - Mês com menor letalidade: {int(min_month["mes"])} ({int(min_month["letalidade_violenta"])}) ocorrências')

# 3. Composição da Letalidade Violenta (Tipos de Crime)
lethality_cols = [
    "hom_doloso",
    "latrocinio",
    "lesao_corp_morte",
    "hom_por_interv_policial"
]

# Calcula o total para cada crime componente
component_totals = df[lethality_cols].sum().reset_index()
component_totals.columns = ["Tipo de Crime", "Total Ocorrências"]
component_totals["Percentual (%)"] = (component_totals["Total Ocorrências"] / total_lethality * 100).round(2)
component_totals = component_totals.sort_values(by="Total Ocorrências", ascending=False)

analysis_summary.append("\n3. Composição da Letalidade Violenta por Tipo de Crime:")
analysis_summary.append(component_totals.to_string(index=False))
print("\nComposição por Tipo de Crime:")
print(component_totals)

# --- Salvar Resumo --- #
try:
    with open(OUTPUT_SUMMARY_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(analysis_summary))
    print(f"\nResumo da EDA salvo em {OUTPUT_SUMMARY_FILE}")
except Exception as e:
    print(f"\nErro ao salvar resumo da EDA: {e}")

print("\n--- Script EDA Finalizado ---")

