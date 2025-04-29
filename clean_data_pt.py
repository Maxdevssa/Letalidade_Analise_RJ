# -*- coding: utf-8 -*-
"""
Script para limpeza e preparação dos dados do ISP-RJ para análise.
"""
import pandas as pd
import os

# Define os caminhos dos arquivos
DATA_DIR = "/home/ubuntu/rio_lethality_analysis/data"
CRIME_DATA_FILE = os.path.join(DATA_DIR, "BaseMunicipioMensal.csv")
AISP_MAP_FILE = os.path.join(DATA_DIR, "Relacao_RISPxAISPxCISP.csv")
OUTPUT_FILE = os.path.join(DATA_DIR, "cleaned_rj_lethality_data.csv") # Mantém o nome do arquivo de saída original

# --- Carregar Dados ---
def load_data(file_path, encoding="latin1", separator=";"):
    """Carrega dados de um arquivo CSV."""
    try:
        df = pd.read_csv(file_path, encoding=encoding, sep=separator)
        print(f"Arquivo {os.path.basename(file_path)} carregado com sucesso. Shape: {df.shape}")
        # Remove espaços em branco dos nomes das colunas
        df.columns = df.columns.str.strip()
        print(f"Colunas após remover espaços em branco: {df.columns.tolist()}") # Imprime colunas limpas
        print("\nColunas reais (objeto Index):", df.columns)
        print("\nPrimeiras 5 linhas:")
        print(df.head())
        print("\nInformações:")
        df.info()
        return df
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em {file_path}")
        return None
    except Exception as e:
        print(f"Erro ao carregar {file_path}: {e}")
        # Tenta com UTF-8 como alternativa
        try:
            print("Tentando carregar com codificação UTF-8...")
            df = pd.read_csv(file_path, encoding=\'utf-8\', sep=separator)
            print(f"Arquivo {os.path.basename(file_path)} carregado com sucesso com UTF-8. Shape: {df.shape}")
            df.columns = df.columns.str.strip() # Limpa colunas aqui também
            print(f"Colunas (UTF-8): {df.columns.tolist()}")
            print("\nPrimeiras 5 linhas (UTF-8):")
            print(df.head())
            print("\nInformações (UTF-8):")
            df.info()
            return df
        except Exception as e_utf8:
            print(f"Erro ao carregar {file_path} com UTF-8: {e_utf8}")
            return None

print("--- Carregando Dados Criminais ---")
df_crime = load_data(CRIME_DATA_FILE)

print("\n--- Carregando Dados de Mapeamento AISP ---")
df_aisp_map = load_data(AISP_MAP_FILE)

if df_crime is None or df_aisp_map is None:
    print("\nErro ao carregar um ou ambos os datasets. Saindo.")
else:
    # --- Limpeza de Dados (Passos Iniciais) ---
    print("\n--- Iniciando Limpeza de Dados ---")

    # Imprime colunas antes do acesso
    print("\nColunas em df_crime antes de filtrar:", df_crime.columns.tolist())

    # 1. Filtrar para o Município do Rio de Janeiro
    # Verifica valores únicos na coluna do município para confirmar o nome
    # Usa o nome exato da coluna como impresso acima
    municipality_col_name = "fmun" # Assumindo que está correto baseado na saída anterior
    print(f"\nTentando acessar a coluna: ", municipality_col_name)
    # Verifica se a coluna existe antes de acessar
    if municipality_col_name in df_crime.columns:
        print(f"\nValores únicos em {municipality_col_name}:", df_crime[municipality_col_name].unique()[:20]) # Mostra os primeiros 20
        df_rj = df_crime[df_crime[municipality_col_name].str.strip().str.upper() == "RIO DE JANEIRO"].copy()
        print(f"\nFiltrado para Rio de Janeiro. Shape: {df_rj.shape}")
        if df_rj.empty:
            print("Aviso: Filtrar por \'RIO DE JANEIRO\' resultou em um DataFrame vazio. Verifique a grafia/caixa.")
            # Imprime valores únicos novamente para dupla verificação
            print("Valores únicos novamente:", df_crime[municipality_col_name].unique())
            exit()
    else:
        print(f"Erro: Coluna ", municipality_col_name, " não encontrada nas colunas de df_crime:", df_crime.columns.tolist())
        exit()

    # 2. Determinar o período mais recente (ex: 2023 ou último ano completo)
    latest_year = df_rj["ano"].max()
    print(f"\nÚltimo ano nos dados: {latest_year}")
    # Vamos focar no último ano completo para análise
    TARGET_YEAR = latest_year -1 if latest_year == 2025 else latest_year # Assumindo que os dados podem ir até o ano atual parcial
    # Verifica se os dados de 2024 estão completos, senão usa 2023
    months_in_latest_year = df_rj[df_rj["ano"] == latest_year]["mes"].nunique()
    if months_in_latest_year < 12:
         TARGET_YEAR = latest_year - 1
         print(f"Último ano ({latest_year}) está incompleto ({months_in_latest_year} meses). Focando em {TARGET_YEAR}.")
    else:
         TARGET_YEAR = latest_year
         print(f"Último ano ({latest_year}) parece completo. Focando em {TARGET_YEAR}.")

    df_rj_filtered = df_rj[df_rj["ano"] == TARGET_YEAR].copy()
    print(f"Filtrado para o ano alvo {TARGET_YEAR}. Shape: {df_rj_filtered.shape}")

    # 3. Identificar Colunas de Letalidade (baseado nos nomes esperados, verificar na saída de load_data)
    # Colunas esperadas: hom_doloso, latrocinio, lesao_corp_morte, hom_por_interv_policial
    lethality_cols = [
        \'hom_doloso\',        # Homicídio doloso
        \'latrocinio\',        # Latrocínio (roubo seguido de morte)
        \'lesao_corp_morte\',  # Lesão corporal seguida de morte
        \'hom_por_interv_policial\' # Homicídio por intervenção de agente do Estado
    ]

    # Verifica se as colunas existem
    missing_cols = [col for col in lethality_cols if col not in df_rj_filtered.columns]
    if missing_cols:
        print(f"\nAviso: Colunas de letalidade esperadas ausentes: {missing_cols}")
        # Ajusta lethality_cols para incluir apenas as existentes
        lethality_cols = [col for col in lethality_cols if col in df_rj_filtered.columns]
        if not lethality_cols:
             print("Erro: Nenhuma coluna de letalidade encontrada. Não é possível prosseguir.")
             exit()

    # Seleciona colunas relevantes + identificador AISP (se disponível diretamente, senão mesclar depois)
    # Precisa da coluna \'aisp\' para agrupar
    base_cols = ["ano", "mes", "fmun", "aisp"]
    relevant_cols = base_cols + lethality_cols

    # Verifica se \'aisp\' está diretamente nos dados criminais
    if \'aisp\' not in df_rj_filtered.columns:
        print("\nColuna \'aisp\' não encontrada nos dados criminais. Será necessário mesclar depois.")
        # Verifica se \'cod_mun\' ou similar existe para mesclar com df_aisp_map
        # Nota: A coluna correta é fmun_cod
        if \'fmun_cod\' in df_rj_filtered.columns and \'cod_mun\' in df_aisp_map.columns: # df_aisp_map não tem fmun_cod
             print("Encontrado \'fmun_cod\' para possível mesclagem (mas df_aisp_map não tem essa coluna).")
             # Tentaremos a mesclagem após a limpeza inicial
             relevant_cols = ["ano", "mes", "fmun", "fmun_cod"] + lethality_cols
        elif \'CISP\' in df_rj_filtered.columns and \'CISP\' in df_aisp_map.columns:
             print("Encontrado \'CISP\' para possível mesclagem.")
             relevant_cols = ["ano", "mes", "fmun", "CISP"] + lethality_cols
        else:
             print("Erro: Não foi possível encontrar uma chave comum (\'aisp\', \'fmun_cod\', \'CISP\') para ligar os dados criminais com o mapeamento AISP.")
             # Verifica as colunas de df_aisp_map novamente
             print("Colunas do Mapa AISP:", df_aisp_map.columns.tolist())
             # Os dados criminais parecem agregados no nível municipal, não AISP/CISP.
             # Reavalia os arquivos baixados. Talvez BaseDelegaciaMes.csv fosse necessário?
             # Por enquanto, prossegue sem AISP se não estiver diretamente disponível ou facilmente mesclável.
             print("Prosseguindo com análise em nível municipal por enquanto.")
             relevant_cols = ["ano", "mes", "fmun"] + lethality_cols
             # Remove \'aisp\' de base_cols se não estiver presente
             if \'aisp\' in base_cols and \'aisp\' not in df_rj_filtered.columns:
                 base_cols.remove(\'aisp\')

    # Garante que todas as colunas selecionadas existem antes de subsetar
    final_relevant_cols = [col for col in relevant_cols if col in df_rj_filtered.columns]
    df_selected = df_rj_filtered[final_relevant_cols].copy()
    print(f"\nColunas relevantes selecionadas: {final_relevant_cols}. Shape: {df_selected.shape}")

    # 4. Tratar Valores Ausentes
    print("\nVerificando valores ausentes:")
    print(df_selected.isnull().sum())
    # Preenche NAs numéricos com 0, assumindo que NA significa zero ocorrências
    numeric_cols = df_selected.select_dtypes(include=[\'number\']).columns
    for col in numeric_cols:
        if col in lethality_cols:
             df_selected[col] = df_selected[col].fillna(0)
    print("\nValores ausentes após preencher NAs em colunas numéricas com 0:")
    print(df_selected.isnull().sum())

    # 5. Converter Tipos de Dados
    # Converte colunas de letalidade para inteiro
    for col in lethality_cols:
        if col in df_selected.columns:
            df_selected[col] = df_selected[col].astype(int)
    # Converte ano e mês
    df_selected["ano"] = df_selected["ano"].astype(int)
    df_selected["mes"] = df_selected["mes"].astype(int)
    # Cria uma coluna Date
    df_selected["date"] = pd.to_datetime(df_selected["ano"].astype(str) + "-" + df_selected["mes"].astype(str) + "-01")
    print("\nTipos de dados após conversão:")
    print(df_selected.dtypes)

    # 6. Criar coluna \'letalidade_violenta\'
    df_selected[\'letalidade_violenta\'] = df_selected[lethality_cols].sum(axis=1)
    print("\nColuna \'letalidade_violenta\' criada.")
    print(df_selected[[\'date\'] + lethality_cols + [\'letalidade_violenta\']].head())

    # --- Mapeamento AISP --- (Tentativa se possível)
    # O BaseMunicipioMensal.csv NÃO contém AISP ou CISP.
    # Ele só tem \'fmun\' e \'fmun_cod\'.
    # O Relacao_RISPxAISPxCISP.csv mapeia CISP para AISP e RISP, e tem \'Município\', mas não \'fmun_cod\'.
    # Para realizar a análise por AISP, provavelmente precisaríamos dos dados agregados por Delegacia (CISP) ou AISP diretamente.
    # O arquivo BaseDelegaciaMes.csv (que falhou no download) poderia conter isso.
    # Por enquanto, não podemos realizar análise em nível de AISP com os dados atuais.
    # Prosseguiremos com a análise em nível de cidade e anotaremos essa limitação.

    print("\n*** Limitação: Análise em nível de AISP não é possível com BaseMunicipioMensal.csv. Requer dados por Delegacia/CISP ou AISP. ***")

    # --- Salvar Dados Limpos ---
    try:
        df_selected.to_csv(OUTPUT_FILE, index=False, sep=\';\', encoding=\'utf-8\')
        print(f"\nDados limpos salvos em {OUTPUT_FILE}")
    except Exception as e:
        print(f"\nErro ao salvar dados limpos: {e}")

print("\n--- Script Finalizado ---")

