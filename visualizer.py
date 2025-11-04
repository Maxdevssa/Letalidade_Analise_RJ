# -*- coding: utf-8 -*-
"""
Script para criar visualizações baseadas nos dados limpos de letalidade do Rio de Janeiro.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import config  # Importa o módulo de configuração

def create_visualizations():
    """
    Cria e salva visualizações a partir dos dados limpos de letalidade.
    """
    print("--- Iniciando Script de Criação de Visualizações ---")

    # --- Carregar Dados Limpos ---
    try:
        df = pd.read_csv(config.CLEANED_DATA_FILE, sep=";", parse_dates=[config.DATE_COL], encoding="utf-8")
        print(f"Arquivo de dados limpos '{os.path.basename(config.CLEANED_DATA_FILE)}' carregado com sucesso. Shape: {df.shape}")
    except FileNotFoundError:
        print(f"Erro: Arquivo de dados limpos não encontrado em '{config.CLEANED_DATA_FILE}'. Execute o script de limpeza primeiro.")
        return
    except Exception as e:
        print(f"Erro ao carregar dados limpos: {e}")
        return

    # --- Preparação para Plots ---
    # Garante que o diretório de plots exista
    os.makedirs(config.PLOTS_DIR, exist_ok=True)

    # Define o estilo do plot
    sns.set_theme(style="whitegrid")

    # Título base para os gráficos
    base_title = f"Letalidade Violenta - {config.TARGET_MUNICIPALITY.title()} ({config.TARGET_YEAR})"

    # Garante que apenas as colunas de letalidade existentes sejam usadas
    existing_lethality_cols = [col for col in config.LETHALITY_COLS if col in df.columns]

    # --- 1. Gráfico de Linha: Evolução Mensal da Letalidade Total ---
    print("\nGerando gráfico de evolução mensal...")
    monthly_total = df.groupby(config.MONTH_COL)[config.LETHALITY_TOTAL_COL].sum().reset_index()

    plt.figure(figsize=(12, 6))
    sns.lineplot(data=monthly_total, x=config.MONTH_COL, y=config.LETHALITY_TOTAL_COL, marker="o", markersize=8)
    plt.title(f"Evolução Mensal - {base_title}")
    plt.xlabel("Mês")
    plt.ylabel("Total de Ocorrências")
    plt.xticks(range(1, 13))
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)

    plot_path_line = os.path.join(config.PLOTS_DIR, f"monthly_evolution_{config.TARGET_YEAR}.png")
    plt.savefig(plot_path_line)
    plt.close()
    print(f"Gráfico salvo em: {plot_path_line}")

    # --- 2. Gráfico de Barras Empilhadas: Composição Mensal da Letalidade ---
    print("\nGerando gráfico de barras empilhadas da composição mensal...")
    monthly_composition = df.groupby(config.MONTH_COL)[existing_lethality_cols].sum()

    monthly_composition.plot(kind="bar", stacked=True, figsize=(14, 7), colormap="viridis")
    plt.title(f"Composição Mensal por Tipo de Crime - {base_title}")
    plt.xlabel("Mês")
    plt.ylabel("Número de Ocorrências")
    plt.xticks(rotation=0)
    plt.legend(title="Tipo de Crime", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    plot_path_stacked_bar = os.path.join(config.PLOTS_DIR, f"monthly_composition_{config.TARGET_YEAR}.png")
    plt.savefig(plot_path_stacked_bar)
    plt.close()
    print(f"Gráfico salvo em: {plot_path_stacked_bar}")

    # --- 3. Gráfico de Pizza: Composição Geral da Letalidade ---
    print("\nGerando gráfico de pizza da composição geral...")
    component_totals = df[existing_lethality_cols].sum()

    plt.figure(figsize=(10, 8))
    plt.pie(component_totals, labels=component_totals.index, autopct="%1.1f%%", startangle=140, pctdistance=0.85)

    # Adiciona um círculo no centro para criar um "donut chart"
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    plt.title(f"Composição Geral por Tipo de Crime - {base_title}")
    plt.axis('equal')  # Garante que a pizza seja um círculo

    plot_path_pie = os.path.join(config.PLOTS_DIR, f"overall_composition_{config.TARGET_YEAR}.png")
    plt.savefig(plot_path_pie)
    plt.close()
    print(f"Gráfico salvo em: {plot_path_pie}")

    print("\n--- Script de Criação de Visualizações Finalizado ---")

if __name__ == '__main__':
    create_visualizations()
