# -*- coding: utf-8 -*-
"""
Script para Análise Exploratória de Dados (EDA) dos dados de letalidade do Rio de Janeiro.
"""
import pandas as pd
import os
import config  # Importa o módulo de configuração

def analyze_data():
    """
    Realiza a Análise Exploratória de Dados (EDA) a partir dos dados limpos.
    """
    print("--- Iniciando Script de Análise EDA ---")

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

    # --- Realizar EDA --- #
    analysis_summary = []

    header = f"--- Análise Exploratória de Dados (EDA) - Letalidade Violenta em {config.TARGET_MUNICIPALITY.title()} ({config.TARGET_YEAR}) ---"
    analysis_summary.append(header)
    analysis_summary.append(f"Fonte dos Dados: ISP-RJ (BaseMunicipioMensal.csv)")
    analysis_summary.append("\n---\n")

    # 1. Total de Letalidade Violenta no Ano
    total_lethality = df[config.LETHALITY_TOTAL_COL].sum()
    analysis_summary.append(f'1. Total de Ocorrências de Letalidade Violenta em {config.TARGET_YEAR}: {total_lethality}')
    print(f'\nTotal de Letalidade Violenta: {total_lethality}')

    # 2. Evolução Mensal da Letalidade Violenta
    monthly_lethality = df.groupby(config.MONTH_COL)[config.LETHALITY_TOTAL_COL].sum().reset_index()
    analysis_summary.append("\n2. Evolução Mensal da Letalidade Violenta:")
    analysis_summary.append(monthly_lethality.to_string(index=False))
    print("\nEvolução Mensal:")
    print(monthly_lethality)

    # Identifica mês com maior e menor letalidade
    max_month = monthly_lethality.loc[monthly_lethality[config.LETHALITY_TOTAL_COL].idxmax()]
    min_month = monthly_lethality.loc[monthly_lethality[config.LETHALITY_TOTAL_COL].idxmin()]
    analysis_summary.append(f'   - Mês com maior letalidade: {int(max_month[config.MONTH_COL])} ({int(max_month[config.LETHALITY_TOTAL_COL])} ocorrências)')
    analysis_summary.append(f'   - Mês com menor letalidade: {int(min_month[config.MONTH_COL])} ({int(min_month[config.LETHALITY_TOTAL_COL])} ocorrências)')

    # 3. Composição da Letalidade Violenta (Tipos de Crime)
    # Garante que apenas as colunas existentes sejam usadas
    existing_lethality_cols = [col for col in config.LETHALITY_COLS if col in df.columns]

    component_totals = df[existing_lethality_cols].sum().reset_index()
    component_totals.columns = ["Tipo de Crime", "Total Ocorrências"]
    component_totals["Percentual (%)"] = (component_totals["Total Ocorrências"] / total_lethality * 100).round(2)
    component_totals = component_totals.sort_values(by="Total Ocorrências", ascending=False)

    analysis_summary.append("\n3. Composição da Letalidade Violenta por Tipo de Crime:")
    analysis_summary.append(component_totals.to_string(index=False))
    print("\nComposição por Tipo de Crime:")
    print(component_totals)

    # --- Salvar Resumo --- #
    try:
        with open(config.OUTPUT_SUMMARY_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(analysis_summary))
        print(f"\nResumo da EDA salvo com sucesso em: {config.OUTPUT_SUMMARY_FILE}")
    except Exception as e:
        print(f"\nErro ao salvar o resumo da EDA: {e}")

    print("\n--- Script de Análise EDA Finalizado ---")

if __name__ == '__main__':
    analyze_data()
