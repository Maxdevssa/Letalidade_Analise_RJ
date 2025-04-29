# -*- coding: utf-8 -*-
"""
Script para criar visualizações baseadas nos dados limpos de letalidade do Rio de Janeiro (2024).
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Define os caminhos dos arquivos
DATA_DIR = "/home/ubuntu/rio_lethality_analysis/data"
CLEANED_DATA_FILE = os.path.join(DATA_DIR, "cleaned_rj_lethality_data.csv")
PLOTS_DIR = "/home/ubuntu/rio_lethality_analysis/plots"

# Garante que o diretório de plots exista
os.makedirs(PLOTS_DIR, exist_ok=True)

# --- Carregar Dados Limpos ---
try:
    df = pd.read_csv(CLEANED_DATA_FILE, sep=";", parse_dates=["date"], encoding="utf-8")
    print(f"Arquivo {os.path.basename(CLEANED_DATA_FILE)} carregado com sucesso. Shape: {df.shape}")
except FileNotFoundError:
    print(f"Erro: Arquivo de dados limpos não encontrado em {CLEANED_DATA_FILE}")
    exit()
except Exception as e:
    print(f"Erro ao carregar dados limpos: {e}")
    exit()

# Define o estilo do plot
sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)

# --- Criar Visualizações --- #

TARGET_YEAR = df["ano"].iloc[0]

# 1. Gráfico de Linha: Evolução Mensal da Letalidade Total
print("\nGerando gráfico de evolução mensal...")
monthly_total = df.groupby("mes")["letalidade_violenta"].sum().reset_index()
plt.figure()
sns.lineplot(data=monthly_total, x="mes", y="letalidade_violenta", marker=".", markersize=12)
plt.title(f"Evolução Mensal da Letalidade Violenta - Rio de Janeiro ({TARGET_YEAR})")
plt.xlabel("Mês")
plt.ylabel("Total de Ocorrências")
plt.xticks(range(1, 13))
plt.grid(True)
plot_path_line = os.path.join(PLOTS_DIR, f"rj_lethality_monthly_evolution_{TARGET_YEAR}.png") # Mantém nome original
plt.savefig(plot_path_line)
plt.close()
print(f"Salvo: {plot_path_line}")

# 2. Gráfico de Barras: Letalidade Total no Ano
print("\nGerando gráfico de barras da letalidade total...")
total_lethality = df["letalidade_violenta"].sum()
plt.figure(figsize=(6, 4))
sns.barplot(x=[f"{TARGET_YEAR}"], y=[total_lethality])
plt.title(f"Total de Letalidade Violenta - Rio de Janeiro ({TARGET_YEAR})")
plt.ylabel("Total de Ocorrências")
plot_path_bar_total = os.path.join(PLOTS_DIR, f"rj_lethality_total_{TARGET_YEAR}.png") # Mantém nome original
plt.savefig(plot_path_bar_total)
plt.close()
print(f"Salvo: {plot_path_bar_total}")

# 3. Gráfico de Barras Empilhadas: Composição Mensal da Letalidade
print("\nGerando gráfico de barras empilhadas da composição mensal...")
lethality_cols = [
    "hom_doloso",
    "latrocinio",
    "lesao_corp_morte",
    "hom_por_interv_policial"
]
monthly_composition = df.groupby("mes")[lethality_cols].sum()

plt.figure()
monthly_composition.plot(kind="bar", stacked=True, figsize=(14, 7))
plt.title(f"Composição Mensal da Letalidade Violenta por Tipo de Crime - Rio de Janeiro ({TARGET_YEAR})")
plt.xlabel("Mês")
plt.ylabel("Número de Ocorrências")
plt.xticks(rotation=0)
plt.legend(title="Tipo de Crime")
plt.tight_layout()
plot_path_stacked_bar = os.path.join(PLOTS_DIR, f"rj_lethality_monthly_composition_{TARGET_YEAR}.png") # Mantém nome original
plt.savefig(plot_path_stacked_bar)
plt.close()
print(f"Salvo: {plot_path_stacked_bar}")

# 4. Gráfico de Pizza: Composição Geral da Letalidade
print("\nGerando gráfico de pizza da composição geral...")
component_totals = df[lethality_cols].sum()
plt.figure(figsize=(8, 8))
plt.pie(component_totals, labels=component_totals.index, autopct="%1.1f%%", startangle=140)
plt.title(f"Composição Geral da Letalidade Violenta - Rio de Janeiro ({TARGET_YEAR})")
plot_path_pie = os.path.join(PLOTS_DIR, f"rj_lethality_overall_composition_{TARGET_YEAR}.png") # Mantém nome original
plt.savefig(plot_path_pie)
plt.close()
print(f"Salvo: {plot_path_pie}")

print("\n--- Script de Visualização Finalizado ---")

