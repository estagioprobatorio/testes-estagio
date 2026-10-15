"""
Script de processamento e classificação do CSV do PDP 2025.
Atende integralmente às regras do rules.md e da TASK 1.
"""

import os
import shutil
import glob
import pandas as pd

def classify_dataset():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    docs_dir = os.path.join(base_dir, 'docs')
    data_dir = os.path.join(base_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # Localizar CSV original
    csv_candidates = glob.glob(os.path.join(docs_dir, '*.csv'))
    if not csv_candidates:
        raise FileNotFoundError("Nenhum arquivo CSV encontrado na pasta docs.")
    
    original_csv_path = csv_candidates[0]
    backup_csv_path = os.path.join(data_dir, 'arquivo_original.csv')
    preenchido_csv_path = os.path.join(data_dir, 'arquivo_preenchido.csv')
    
    # 1.4 Preservação e cópia de segurança
    shutil.copy2(original_csv_path, backup_csv_path)
    print(f"[1] Backup realizado com sucesso em: {backup_csv_path}")
    
    # Leitura com UTF-8
    df = pd.read_csv(original_csv_path, encoding='utf-8')
    initial_rows, initial_cols = df.shape
    print(f"[2] CSV original carregado: {initial_rows} linhas, {initial_cols} colunas.")
    
    # Critérios de _DOC_PDP_2025.md
    t1_criteria_plan = [
        'descreve o objetivo da proposta pedagógica',
        'a proposta pedagógica apresenta um recurso educacional digital oferecido pela secretaria',
        'o recurso educacional digital selecionado do seu componente, caso tenha',
        'a proposta apresenta para a recomposição uma habilidade prioritária de seu componente',
        'a proposta de planejamento explora o recurso educacional digital relacionando-o à recomposição das aprendizagens',
        'descreve as ações a serem realizadas na implementação da prática respondendo a todas as questões do planejamento',
        'descreve os resultados esperados com a implementação do planejamento'
    ]

    t1_prat_all = [
        'informa aos estudantes os objetivos de aprendizagem da proposta pedagógica',
        'explica aos estudantes o porquê da aula e/ou atividade voltada para a recomposição',
        'apresenta aos estudantes o recurso educacional digital que será utilizado durante aula e/ou atividade',
        'a aula e/ou atividade corresponde à descrição das ações presentes no planejamento',
        'evidencia-se o domínio do professor na utilização do recurso educacional digital utilizado',
        'adapta a prática a possíveis imprevistos técnicos que possam ocorrer',
        'promove uma personalização do ensino a partir do trabalho com o recurso educacional escolhido'
    ]

    t2_plan_all = [
        'descreve o objetivo da proposta pedagógica',
        'a proposta pedagógica apresenta mais de uma ferramenta educacional oferecida pela secretaria',
        'a proposta apresenta para a recomposição de um habilidade prioritária de seu componente',
        'a proposta de planejamento explora ferramentas educacionais relacionando-as à recomposição das aprendizagens',
        'descreve as ações a serem realizadas na implementação da prática respondendo a todas as questões do planejamento',
        'descreve os resultados esperados com a implementação do planejamento'
    ]

    t2_prat_all = [
        'informa aos estudantes os objetivos de aprendizagem da proposta pedagógica',
        'explica aos estudantes o porquê da aula e/ou atividade voltada para a recomposição',
        'apresenta aos estudantes a(s) ferramenta(s) educacional(is) que serão utilizados na aula e/ou atividade',
        'a aula e/ou atividade corresponde à descrição das ações presentes no planejamento',
        'evidencia-se o domínio do professor,na utilização da(s) ferramenta(s) educacional(is)',
        'adapta a prática a possíveis imprevistos técnicos que possam ocorrer',
        'promove uma personalização do ensino a partir do trabalho com a ferramenta educacional escolhida'
    ]

    supera_patterns = [
        'supera as expectativas', 'superou as expectativas',
        'supera a expectativa', 'superou a expectativa',
        'digna de indicação como boa prática', 'digna de indicacao como boa pratica',
        'indicação como boa prática', 'indicacao como boa pratica'
    ]

    def is_supera(pf_val, ref_val):
        comb = (str(pf_val) + ' ' + str(ref_val)).lower()
        return any(p in comb for p in supera_patterns)

    def classify_eval(val, criteria_list, cond_item=None, supera_flag=False):
        """
        Classificação por Faixas Percentuais Gradativas (Sugestão 1):
        - Não atende (0% a 25%): 0 a 1 critério atendido ou ausência comprovada.
        - Atende parcialmente (26% a 70%): 2 a 4 critérios atendidos.
        - Atende integralmente (71% a 99% ou 100% regular): 5 a 6 critérios (ou 100% sem evidência extra de superação).
        - Supera (100% + impacto): 100% dos critérios cumpridos com evidência explícita de superação/boa prática.
        """
        if not isinstance(val, str) or not val.strip():
            return None
        val_lower = val.lower()
        
        # Contagem de critérios atendidos
        cnt = sum(1 for c in criteria_list if c in val_lower)
        total = len(criteria_list)
        pct = cnt / total
        
        if cnt <= 1:
            return 'Não atende'
        elif pct <= 0.70:
            return 'Atende parcialmente'
        elif pct < 1.0:
            return 'Atende integralmente'
        else: # 100% dos critérios cumpridos
            if supera_flag:
                return 'Supera'
            return 'Atende integralmente'

    # Identificação das colunas
    col_mod = df.columns[33]      # 2º ANO - Selecione a modalidade do cursista
    col_tema = df.columns[86]     # DOC-2ANO-T05-REF04. Qual é o tema escolhido pelo cursista...
    col_pf = df.columns[58]       # Pontos fortes
    col_ref = df.columns[65]      # Reflexões
    
    col_t2_plan_src = df.columns[79]
    col_t2_plan_dst = df.columns[78]  # Descrição Nível IA Planejamento T2
    
    col_t2_prat_src = df.columns[81]
    col_t2_prat_dst = df.columns[80]  # Descrição Nível IA Planejamento T2.1 (Prática T2)
    
    col_t1_plan_src = df.columns[83]
    col_t1_plan_dst = df.columns[82]  # Descrição Nível IA Planejamento T1
    
    col_t1_prat_src = df.columns[85]
    col_t1_prat_dst = df.columns[84]  # Descrição Nível IA Planejamento T1.1 (Prática T1)

    # Ensure target columns are object dtype to allow string values without warning
    for col_dst in [col_t1_plan_dst, col_t1_prat_dst, col_t2_plan_dst, col_t2_prat_dst]:
        df[col_dst] = df[col_dst].astype(object)

    counts = {
        'T1_Plan': {'Não atende': 0, 'Atende parcialmente': 0, 'Atende integralmente': 0, 'Supera': 0},
        'T1_Prat': {'Não atende': 0, 'Atende parcialmente': 0, 'Atende integralmente': 0, 'Supera': 0},
        'T2_Plan': {'Não atende': 0, 'Atende parcialmente': 0, 'Atende integralmente': 0, 'Supera': 0},
        'T2_Prat': {'Não atende': 0, 'Atende parcialmente': 0, 'Atende integralmente': 0, 'Supera': 0},
    }
    pendentes_count = 0

    for idx in range(len(df)):
        mod = df.at[idx, col_mod]
        # Restrição estrita à modalidade DOCENTE conforme rules.md
        if mod != 'Docentes':
            pendentes_count += 1
            continue
            
        tema = df.at[idx, col_tema]
        pf = df.at[idx, col_pf]
        ref = df.at[idx, col_ref]
        sup = is_supera(pf, ref)
        
        if tema == 'Tema I':
            c_plan = classify_eval(df.at[idx, col_t1_plan_src], t1_criteria_plan, None, sup)
            c_prat = classify_eval(df.at[idx, col_t1_prat_src], t1_prat_all, None, sup)
            if c_plan:
                df.at[idx, col_t1_plan_dst] = c_plan
                counts['T1_Plan'][c_plan] += 1
            if c_prat:
                df.at[idx, col_t1_prat_dst] = c_prat
                counts['T1_Prat'][c_prat] += 1
        elif tema == 'Tema II':
            c_plan = classify_eval(df.at[idx, col_t2_plan_src], t2_plan_all, None, sup)
            c_prat = classify_eval(df.at[idx, col_t2_prat_src], t2_prat_all, None, sup)
            if c_plan:
                df.at[idx, col_t2_plan_dst] = c_plan
                counts['T2_Plan'][c_plan] += 1
            if c_prat:
                df.at[idx, col_t2_prat_dst] = c_prat
                counts['T2_Prat'][c_prat] += 1
        else:
            pendentes_count += 1

    # Validações finais de integridade
    assert len(df) == initial_rows, f"Erro: Quantidade de linhas alterada! ({len(df)} vs {initial_rows})"
    assert len(df.columns) == initial_cols, f"Erro: Quantidade de colunas alterada! ({len(df.columns)} vs {initial_cols})"
    
    # Salvar arquivo preenchido
    df.to_csv(preenchido_csv_path, index=False, encoding='utf-8')
    print(f"[3] CSV preenchido salvo em: {preenchido_csv_path}")
    
    print("\n[4] Resumo das classificações:")
    for dim, dist in counts.items():
        print(f"  {dim}: {dist}")
    print(f"  Registros Docentes pendentes de evidência ou não-docentes: {pendentes_count}")

    return df, counts

if __name__ == '__main__':
    classify_dataset()
