# -*- coding: utf-8 -*-
"""
Script Principal para Orquestrar a Análise de Letalidade do Rio de Janeiro.

Este script executa o fluxo completo de trabalho:
1. Limpeza e preparação dos dados.
2. Análise exploratória dos dados (EDA).
3. Criação de visualizações.

Para executar o projeto, basta rodar este arquivo: `python main.py`
"""
import data_cleaner
import data_analyzer
import visualizer

def main():
    """
    Função principal que orquestra a execução dos módulos da análise.
    """
    print("==========================================================")
    print("=== INICIANDO FLUXO DE ANÁLISE DE LETALIDADE VIOLENTA ===")
    print("==========================================================")

    # Passo 1: Limpeza dos Dados
    print("\n>>> PASSO 1: Limpeza e Preparação dos Dados")
    data_cleaner.clean_data()

    # Passo 2: Análise Exploratória de Dados
    print("\n>>> PASSO 2: Análise Exploratória de Dados (EDA)")
    data_analyzer.analyze_data()

    # Passo 3: Criação de Visualizações
    print("\n>>> PASSO 3: Criação de Visualizações")
    visualizer.create_visualizations()

    print("\n==========================================================")
    print("=== FLUXO DE ANÁLISE FINALIZADO COM SUCESSO        ===")
    print("==========================================================")
    print("\nResultados:")
    print("- Dados limpos salvos em 'data/'.")
    print("- Resumo da análise salvo em 'eda_summary_pt.txt'.")
    print("- Gráficos salvos em 'plots/'.")

if __name__ == '__main__':
    main()
