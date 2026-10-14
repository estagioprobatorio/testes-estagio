"""
Módulo de validação de dados para o PDP 2025.
Garante a integridade do arquivo preenchido em comparação com o original,
conforme as diretrizes de rules.md e task1.md.
"""

import os
import pandas as pd

ALLOWED_LEVELS = {'Não atende', 'Atende parcialmente', 'Atende integralmente', 'Supera'}

def validate_filled_dataset(original_csv_path, filled_csv_path):
    """
    Executa validações rigorosas entre a base original e a base preenchida.
    """
    if not os.path.exists(original_csv_path):
        raise FileNotFoundError(f"Arquivo original não encontrado: {original_csv_path}")
    if not os.path.exists(filled_csv_path):
        raise FileNotFoundError(f"Arquivo preenchido não encontrado: {filled_csv_path}")
        
    df_orig = pd.read_csv(original_csv_path, encoding='utf-8')
    df_filled = pd.read_csv(filled_csv_path, encoding='utf-8')
    
    report = {
        'total_rows_original': len(df_orig),
        'total_rows_filled': len(df_filled),
        'total_cols_original': len(df_orig.columns),
        'total_cols_filled': len(df_filled.columns),
        'columns_match': list(df_orig.columns) == list(df_filled.columns),
        'filled_columns_summary': {},
        'invalid_values': {},
        'errors': []
    }
    
    # 1. Checagem de integridade de dimensões
    if report['total_rows_original'] != report['total_rows_filled']:
        report['errors'].append(f"Discrepância no número de linhas: {report['total_rows_original']} vs {report['total_rows_filled']}")
        
    if report['total_cols_original'] != report['total_cols_filled']:
        report['errors'].append(f"Discrepância no número de colunas: {report['total_cols_original']} vs {report['total_cols_filled']}")
        
    if not report['columns_match']:
        report['errors'].append("Os cabeçalhos das colunas não coincidem com o arquivo original.")

    # Colunas de classificação IA
    col_t2_plan = df_filled.columns[78]
    col_t2_prat = df_filled.columns[80]
    col_t1_plan = df_filled.columns[82]
    col_t1_prat = df_filled.columns[84]
    
    target_cols = [col_t1_plan, col_t1_prat, col_t2_plan, col_t2_prat]
    
    for col in target_cols:
        non_null_count = df_filled[col].notna().sum()
        null_count = df_filled[col].isna().sum()
        unique_vals = set(df_filled[col].dropna().unique())
        
        report['filled_columns_summary'][col] = {
            'preenchidos': int(non_null_count),
            'pendentes_ou_vazios': int(null_count),
            'valores_distintos': list(unique_vals)
        }
        
        # Validar valores permitidos estritos
        invalid = unique_vals - ALLOWED_LEVELS
        if invalid:
            report['invalid_values'][col] = list(invalid)
            report['errors'].append(f"Valores inválidos encontrados na coluna '{col}': {invalid}")

    # Verificar se colunas não-alvo foram mantidas íntegras
    non_target_cols = [c for c in df_filled.columns if c not in target_cols]
    for c in non_target_cols:
        # Comparar nulos e não-nulos
        orig_series = df_orig[c].fillna("")
        filled_series = df_filled[c].fillna("")
        if not orig_series.equals(filled_series):
            report['errors'].append(f"A coluna '{c}' sofreu alterações indevidas fora do escopo da tarefa.")

    report['is_valid'] = len(report['errors']) == 0
    return report

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    orig = os.path.join(base_dir, 'data', 'arquivo_original.csv')
    filled = os.path.join(base_dir, 'data', 'arquivo_preenchido.csv')
    res = validate_filled_dataset(orig, filled)
    print("Resultado da Validação:", "SUCESSO" if res['is_valid'] else "FALHA")
    for k, v in res.items():
        if k != 'filled_columns_summary':
            print(f"{k}: {v}")
    print("\nResumo das Colunas Preenchidas:")
    for col, summary in res['filled_columns_summary'].items():
        print(f"  {col}: {summary}")
