# -*- coding: utf-8 -*-
"""
Script para limpeza e preparação dos dados do ISP-RJ para análise.
"""
import pandas as pd
import os
import config  # Importa o módulo de configuração

def load_data(file_path, encoding="latin1", separator=";"):
    """Carrega dados de um arquivo CSV, com fallback para UTF-8."""
    try:
        df = pd.read_csv(file_path, encoding=encoding, sep=separator)
        print(f"Arquivo {os.path.basename(file_path)} carregado com sucesso (latin1). Shape: {df.shape}")
    except Exception as e:
        print(f"Erro ao carregar {file_path} com latin1: {e}")
        try:
            print("Tentando carregar com codificação UTF-8...")
            df = pd.read_csv(file_path, encoding='utf-8', sep=separator)
            print(f"Arquivo {os.path.basename(file_path)} carregado com sucesso (UTF-8). Shape: {df.shape}")
        except Exception as e_utf8:
            print(f"Erro ao carregar {file_path} com UTF-8: {e_utf8}")
            return None

    # Limpa os nomes das colunas
    df.columns = df.columns.str.strip()
    print("Nomes das colunas limpos.")
    return df

def clean_data():
    """
    Executa o processo completo de limpeza e preparação dos dados.
    """
    print("--- Iniciando Script de Limpeza de Dados ---")

    # --- Carregar Dados ---
    print("\n--- Carregando Dados Criminais ---")
    df_crime = load_data(config.CRIME_DATA_FILE)

    if df_crime is None:
        print("\nErro fatal ao carregar dados criminais. Saindo.")
        return

    # --- Limpeza e Transformação ---
    print("\n--- Iniciando Limpeza e Transformação ---")

    # 1. Filtrar para o Município Alvo
    if config.MUNICIPALITY_COL not in df_crime.columns:
        print(f"Erro: Coluna de município '{config.MUNICIPALITY_COL}' não encontrada.")
        return

    df_rj = df_crime[df_crime[config.MUNICIPALITY_COL].str.strip().str.upper() == config.TARGET_MUNICIPALITY.upper()].copy()
    print(f"Filtrado para o município: '{config.TARGET_MUNICIPALITY}'. Shape: {df_rj.shape}")

    if df_rj.empty:
        print("Aviso: O DataFrame está vazio após filtrar pelo município. Verifique o nome do município em 'config.py'.")
        return

    # 2. Filtrar para o Ano Alvo
    if config.YEAR_COL not in df_rj.columns:
        print(f"Erro: Coluna de ano '{config.YEAR_COL}' não encontrada.")
        return

    df_filtered = df_rj[df_rj[config.YEAR_COL] == config.TARGET_YEAR].copy()
    print(f"Filtrado para o ano: {config.TARGET_YEAR}. Shape: {df_filtered.shape}")

    if df_filtered.empty:
        print(f"Aviso: O DataFrame está vazio após filtrar pelo ano {config.TARGET_YEAR}. Verifique o ano em 'config.py'.")
        return

    # 3. Verificar e Selecionar Colunas de Letalidade
    missing_cols = [col for col in config.LETHALITY_COLS if col not in df_filtered.columns]
    if missing_cols:
        print(f"\nAviso: As seguintes colunas de letalidade não foram encontradas: {missing_cols}")

    # Usar apenas as colunas de letalidade que existem no DataFrame
    existing_lethality_cols = [col for col in config.LETHALITY_COLS if col in df_filtered.columns]
    if not existing_lethality_cols:
        print("Erro: Nenhuma das colunas de letalidade especificadas foi encontrada. Impossível continuar.")
        return

    base_cols = [config.YEAR_COL, config.MONTH_COL, config.MUNICIPALITY_COL]
    relevant_cols = base_cols + existing_lethality_cols
    df_selected = df_filtered[relevant_cols].copy()
    print(f"\nColunas relevantes selecionadas. Shape: {df_selected.shape}")

    # 4. Tratar Valores Ausentes
    for col in existing_lethality_cols:
        df_selected[col] = df_selected[col].fillna(0)
    print("Valores ausentes nas colunas de crime preenchidos com 0.")

    # 5. Converter Tipos de Dados e Criar Coluna 'date'
    for col in existing_lethality_cols:
        df_selected[col] = df_selected[col].astype(int)

    df_selected[config.YEAR_COL] = df_selected[config.YEAR_COL].astype(int)
    df_selected[config.MONTH_COL] = df_selected[config.MONTH_COL].astype(int)
    df_selected[config.DATE_COL] = pd.to_datetime(df_selected[config.YEAR_COL].astype(str) + '-' + df_selected[config.MONTH_COL].astype(str) + '-01')
    print("Tipos de dados convertidos e coluna 'date' criada.")

    # 6. Criar Coluna Agregada de Letalidade
    df_selected[config.LETHALITY_TOTAL_COL] = df_selected[existing_lethality_cols].sum(axis=1)
    print(f"Coluna agregada '{config.LETHALITY_TOTAL_COL}' criada.")

    # --- Salvar Dados Limpos ---
    try:
        # Garante que o diretório de dados exista
        os.makedirs(config.DATA_DIR, exist_ok=True)
        df_selected.to_csv(config.CLEANED_DATA_FILE, index=False, sep=';', encoding='utf-8')
        print(f"\nDados limpos salvos com sucesso em: {config.CLEANED_DATA_FILE}")
    except Exception as e:
        print(f"\nErro ao salvar dados limpos: {e}")

    print("\n--- Script de Limpeza de Dados Finalizado ---")

if __name__ == '__main__':
    clean_data()
