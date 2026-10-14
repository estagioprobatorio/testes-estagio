"""
Módulo de carregamento e preparação de dados para o painel PDP 2025.
Implementa a filtragem estrita na camada de dados para a modalidade DOCENTE.
"""

import os
from pathlib import Path
import pandas as pd

# Mapeamento oficial dos critérios e taxonomia de Bloom conforme _DOC_PDP_2025.md e _taxonomia_bloom.md
CRITERIA_METADATA = [
    # TEMA I - PLANEJAMENTO
    {
        'id_criterio': 'T1_PL_01',
        'tema': 'Tema I',
        'tema_titulo': 'Recursos Educacionais Digitais',
        'dimensao': 'Planejamento',
        'criterio': 'Descreve o objetivo da proposta pedagógica',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando um recurso educacional digital como apoio pedagógico.',
        'categoria_bloom': 'Compreender',
        'processo_cognitivo': 'Explicar e estruturar a intencionalidade didática da proposta pedagógica'
    },
    {
        'id_criterio': 'T1_PL_02',
        'tema': 'Tema I',
        'tema_titulo': 'Recursos Educacionais Digitais',
        'dimensao': 'Planejamento',
        'criterio': 'A proposta pedagógica apresenta um recurso educacional digital oferecido pela secretaria',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando um recurso educacional digital como apoio pedagógico.',
        'categoria_bloom': 'Lembrar',
        'processo_cognitivo': 'Reconhecer e selecionar recurso educacional digital oficial'
    },
    {
        'id_criterio': 'T1_PL_03',
        'tema': 'Tema I',
        'tema_titulo': 'Recursos Educacionais Digitais',
        'dimensao': 'Planejamento',
        'criterio': 'O recurso educacional digital selecionado do seu componente, caso tenha',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando um recurso educacional digital como apoio pedagógico.',
        'categoria_bloom': 'Compreender',
        'processo_cognitivo': 'Classificar e relacionar a ferramenta digital ao componente curricular'
    },
    {
        'id_criterio': 'T1_PL_04',
        'tema': 'Tema I',
        'tema_titulo': 'Recursos Educacionais Digitais',
        'dimensao': 'Planejamento',
        'criterio': 'A proposta apresenta para a recomposição uma habilidade prioritária de seu componente',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando um recurso educacional digital como apoio pedagógico.',
        'categoria_bloom': 'Analisar',
        'processo_cognitivo': 'Diagnosticar e selecionar habilidade prioritária a partir de dados de defasagem'
    },
    {
        'id_criterio': 'T1_PL_05',
        'tema': 'Tema I',
        'tema_titulo': 'Recursos Educacionais Digitais',
        'dimensao': 'Planejamento',
        'criterio': 'A proposta de planejamento explora o recurso educacional digital relacionando-o à recomposição das aprendizagens',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando um recurso educacional digital como apoio pedagógico.',
        'categoria_bloom': 'Analisar',
        'processo_cognitivo': 'Articular o uso da plataforma digital com a superação de lacunas de aprendizagem'
    },
    {
        'id_criterio': 'T1_PL_06',
        'tema': 'Tema I',
        'tema_titulo': 'Recursos Educacionais Digitais',
        'dimensao': 'Planejamento',
        'criterio': 'Descreve as ações a serem realizadas na implementação da prática respondendo a todas as questões do planejamento',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando um recurso educacional digital como apoio pedagógico.',
        'categoria_bloom': 'Criar',
        'processo_cognitivo': 'Estruturar e planejar uma sequência didática articulada e completa'
    },
    {
        'id_criterio': 'T1_PL_07',
        'tema': 'Tema I',
        'tema_titulo': 'Recursos Educacionais Digitais',
        'dimensao': 'Planejamento',
        'criterio': 'Descreve os resultados esperados com a implementação do planejamento',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando um recurso educacional digital como apoio pedagógico.',
        'categoria_bloom': 'Avaliar',
        'processo_cognitivo': 'Formular metas avaliativas e critérios de verificação do sucesso pedagógico'
    },

    # TEMA I - PRÁTICA
    {
        'id_criterio': 'T1_PR_01',
        'tema': 'Tema I',
        'tema_titulo': 'Recursos Educacionais Digitais',
        'dimensao': 'Prática',
        'criterio': 'Informa aos estudantes os objetivos de aprendizagem da proposta pedagógica',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando um recurso educacional digital como apoio pedagógico.',
        'categoria_bloom': 'Compreender',
        'processo_cognitivo': 'Comunicar e esclarecer aos alunos o sentido e o objetivo da aprendizagem'
    },
    {
        'id_criterio': 'T1_PR_02',
        'tema': 'Tema I',
        'tema_titulo': 'Recursos Educacionais Digitais',
        'dimensao': 'Prática',
        'criterio': 'Explica aos estudantes o porquê da aula e/ou atividade voltada para a recomposição',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando um recurso educacional digital como apoio pedagógico.',
        'categoria_bloom': 'Compreender',
        'processo_cognitivo': 'Contextualizar a relevância e o propósito da recomposição formativa'
    },
    {
        'id_criterio': 'T1_PR_03',
        'tema': 'Tema I',
        'tema_titulo': 'Recursos Educacionais Digitais',
        'dimensao': 'Prática',
        'criterio': 'Apresenta aos estudantes o recurso educacional digital que será utilizado durante aula e/ou atividade',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando um recurso educacional digital como apoio pedagógico.',
        'categoria_bloom': 'Compreender',
        'processo_cognitivo': 'Apresentar e demonstrar o funcionamento do recurso tecnológico aos alunos'
    },
    {
        'id_criterio': 'T1_PR_04',
        'tema': 'Tema I',
        'tema_titulo': 'Recursos Educacionais Digitais',
        'dimensao': 'Prática',
        'criterio': 'A aula e/ou atividade corresponde à descrição das ações presentes no planejamento',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando um recurso educacional digital como apoio pedagógico.',
        'categoria_bloom': 'Aplicar',
        'processo_cognitivo': 'Executar e implementar as ações didáticas em conformidade com o plano elaborado'
    },
    {
        'id_criterio': 'T1_PR_05',
        'tema': 'Tema I',
        'tema_titulo': 'Recursos Educacionais Digitais',
        'dimensao': 'Prática',
        'criterio': 'Evidencia-se o domínio do professor na utilização do recurso educacional digital utilizado',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando um recurso educacional digital como apoio pedagógico.',
        'categoria_bloom': 'Aplicar',
        'processo_cognitivo': 'Operar com destreza prática e segurança instrumental a ferramenta tecnológica'
    },
    {
        'id_criterio': 'T1_PR_06',
        'tema': 'Tema I',
        'tema_titulo': 'Recursos Educacionais Digitais',
        'dimensao': 'Prática',
        'criterio': 'Adapta a prática a possíveis imprevistos técnicos que possam ocorrer',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando um recurso educacional digital como apoio pedagógico.',
        'categoria_bloom': 'Avaliar',
        'processo_cognitivo': 'Julgar a situação de imprevisto técnico e tomar decisões corretivas adequadas'
    },
    {
        'id_criterio': 'T1_PR_07',
        'tema': 'Tema I',
        'tema_titulo': 'Recursos Educacionais Digitais',
        'dimensao': 'Prática',
        'criterio': 'Promove uma personalização do ensino a partir do trabalho com o recurso educacional escolhido',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando um recurso educacional digital como apoio pedagógico.',
        'categoria_bloom': 'Criar',
        'processo_cognitivo': 'Elaborar e modular percursos de aprendizagem personalizados e diferenciados'
    },

    # TEMA II - PLANEJAMENTO
    {
        'id_criterio': 'T2_PL_01',
        'tema': 'Tema II',
        'tema_titulo': 'Ferramentas Educacionais',
        'dimensao': 'Planejamento',
        'criterio': 'Descreve o objetivo da proposta pedagógica',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando duas ou mais ferramentas educacionais.',
        'categoria_bloom': 'Compreender',
        'processo_cognitivo': 'Explicar e estruturar o objetivo didático da proposta pedagógica'
    },
    {
        'id_criterio': 'T2_PL_02',
        'tema': 'Tema II',
        'tema_titulo': 'Ferramentas Educacionais',
        'dimensao': 'Planejamento',
        'criterio': 'A proposta pedagógica apresenta mais de uma ferramenta educacional oferecida pela secretaria',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando duas ou mais ferramentas educacionais.',
        'categoria_bloom': 'Compreender',
        'processo_cognitivo': 'Articular e selecionar ferramentas educacionais complementares da secretaria'
    },
    {
        'id_criterio': 'T2_PL_03',
        'tema': 'Tema II',
        'tema_titulo': 'Ferramentas Educacionais',
        'dimensao': 'Planejamento',
        'criterio': 'A proposta apresenta para a recomposição de um habilidade prioritária de seu componente',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando duas ou mais ferramentas educacionais.',
        'categoria_bloom': 'Analisar',
        'processo_cognitivo': 'Examinar diagnósticos de aprendizagem e selecionar a habilidade prioritária'
    },
    {
        'id_criterio': 'T2_PL_04',
        'tema': 'Tema II',
        'tema_titulo': 'Ferramentas Educacionais',
        'dimensao': 'Planejamento',
        'criterio': 'A proposta de planejamento explora ferramentas educacionais relacionando-as à recomposição das aprendizagens',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando duas ou mais ferramentas educacionais.',
        'categoria_bloom': 'Analisar',
        'processo_cognitivo': 'Estabelecer relações funcionais entre as ferramentas selecionadas e a recomposição'
    },
    {
        'id_criterio': 'T2_PL_05',
        'tema': 'Tema II',
        'tema_titulo': 'Ferramentas Educacionais',
        'dimensao': 'Planejamento',
        'criterio': 'Descreve as ações a serem realizadas na implementação da prática respondendo a todas as questões do planejamento',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando duas ou mais ferramentas educacionais.',
        'categoria_bloom': 'Criar',
        'processo_cognitivo': 'Conceber e detalhar uma proposta pedagógica estruturada de intervenção'
    },
    {
        'id_criterio': 'T2_PL_06',
        'tema': 'Tema II',
        'tema_titulo': 'Ferramentas Educacionais',
        'dimensao': 'Planejamento',
        'criterio': 'Descreve os resultados esperados com a implementação do planejamento',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando duas ou mais ferramentas educacionais.',
        'categoria_bloom': 'Avaliar',
        'processo_cognitivo': 'Definir parâmetros avaliativos para julgar os resultados pretendidos da prática'
    },

    # TEMA II - PRÁTICA
    {
        'id_criterio': 'T2_PR_01',
        'tema': 'Tema II',
        'tema_titulo': 'Ferramentas Educacionais',
        'dimensao': 'Prática',
        'criterio': 'Informa aos estudantes os objetivos de aprendizagem da proposta pedagógica',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando duas ou mais ferramentas educacionais.',
        'categoria_bloom': 'Compreender',
        'processo_cognitivo': 'Compartilhar e explicar aos estudantes os objetivos pedagógicos propostos'
    },
    {
        'id_criterio': 'T2_PR_02',
        'tema': 'Tema II',
        'tema_titulo': 'Ferramentas Educacionais',
        'dimensao': 'Prática',
        'criterio': 'Explica aos estudantes o porquê da aula e/ou atividade voltada para a recomposição',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando duas ou mais ferramentas educacionais.',
        'categoria_bloom': 'Compreender',
        'processo_cognitivo': 'Construir significado sobre a necessidade formativa da recomposição'
    },
    {
        'id_criterio': 'T2_PR_03',
        'tema': 'Tema II',
        'tema_titulo': 'Ferramentas Educacionais',
        'dimensao': 'Prática',
        'criterio': 'Apresenta aos estudantes a(s) ferramenta(s) educacional(is) que serão utilizados na aula e/ou atividade',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando duas ou mais ferramentas educacionais.',
        'categoria_bloom': 'Compreender',
        'processo_cognitivo': 'Orientar e apresentar o ecossistema de ferramentas digitais aos alunos'
    },
    {
        'id_criterio': 'T2_PR_04',
        'tema': 'Tema II',
        'tema_titulo': 'Ferramentas Educacionais',
        'dimensao': 'Prática',
        'criterio': 'A aula e/ou atividade corresponde à descrição das ações presentes no planejamento',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando duas ou mais ferramentas educacionais.',
        'categoria_bloom': 'Aplicar',
        'processo_cognitivo': 'Implementar em sala de aula o plano pedagógico anteriormente traçado'
    },
    {
        'id_criterio': 'T2_PR_05',
        'tema': 'Tema II',
        'tema_titulo': 'Ferramentas Educacionais',
        'dimensao': 'Prática',
        'criterio': 'Evidencia-se o domínio do professor,na utilização da(s) ferramenta(s) educacional(is)',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando duas ou mais ferramentas educacionais.',
        'categoria_bloom': 'Aplicar',
        'processo_cognitivo': 'Empregar e operar com destreza as ferramentas educacionais na mediação'
    },
    {
        'id_criterio': 'T2_PR_06',
        'tema': 'Tema II',
        'tema_titulo': 'Ferramentas Educacionais',
        'dimensao': 'Prática',
        'criterio': 'Adapta a prática a possíveis imprevistos técnicos que possam ocorrer',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando duas ou mais ferramentas educacionais.',
        'categoria_bloom': 'Avaliar',
        'processo_cognitivo': 'Julgar e contornar imprevistos técnicos com alternativas didáticas'
    },
    {
        'id_criterio': 'T2_PR_07',
        'tema': 'Tema II',
        'tema_titulo': 'Ferramentas Educacionais',
        'dimensao': 'Prática',
        'criterio': 'Promove uma personalização do ensino a partir do trabalho com a ferramenta educacional escolhida',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando duas ou mais ferramentas educacionais.',
        'categoria_bloom': 'Criar',
        'processo_cognitivo': 'Estruturar atividades e ritmos customizados para os diferentes perfis discentes'
    }
]

def get_criteria_metadata():
    """Retorna DataFrame com o catálogo oficial dos critérios institucionais e Taxonomia de Bloom."""
    return pd.DataFrame(CRITERIA_METADATA)

def find_modality_column(df):
    """
    Identifica com segurança a coluna que define a modalidade do cursista.
    Lança ValueError explicativo caso não seja identificável.
    """
    candidates = [
        col for col in df.columns 
        if 'modalidade do cursista' in col.lower() and '2º ano' in col.lower()
    ]
    if not candidates:
        candidates = [col for col in df.columns if 'modalidade do cursista' in col.lower()]
    if not candidates:
        candidates = [col for col in df.columns if 'modalidade' in col.lower() and 'feedback' not in col.lower()]
    
    if not candidates:
        raise ValueError(
            "Coluna de modalidade não encontrada no conjunto de dados. "
            "A análise foi interrompida para preservar a integridade metodológica."
        )
    return candidates[0]

def load_and_filter_docentes(csv_path=None):
    """
    Carrega o CSV e aplica a filtragem estrita na camada de dados
    para a modalidade DOCENTE antes de quaisquer cálculos ou visualizações.
    """
    if csv_path is None:
        base_dir = Path(__file__).resolve().parent.parent
        csv_path = base_dir / 'data' / 'arquivo_preenchido.csv'
        if not csv_path.exists():
            csv_path = base_dir / 'docs' / 'Observações e feedbacks 2024 - Teste Análise IA Checklist.csv'
            
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"Arquivo CSV de dados não encontrado no caminho: {csv_path}")

    # Verificar se CSV está vazio
    try:
        df = pd.read_csv(csv_path, encoding='utf-8')
    except pd.errors.EmptyDataError:
        return pd.DataFrame(), "O arquivo CSV fornecido está completamente vazio."
    
    if df.empty:
        return pd.DataFrame(), "O arquivo CSV não possui registros."

    # Identificar coluna de modalidade
    mod_col = find_modality_column(df)
    
    # Filtragem estrita: apenas DOCENTE (case-insensitive)
    df_docente = df[df[mod_col].astype(str).str.strip().str.lower() == 'docentes'].copy()
    
    if df_docente.empty:
        return df_docente, "Nenhum registro da modalidade DOCENTE foi encontrado na base de dados."
        
    return df_docente, None

def get_docente_evaluations(df_docente):
    """
    Extrai as avaliações normalizadas dos docentes (linhas x critérios/dimensões)
    respeitando as colunas de classificação e checklists oficiais.
    """
    if df_docente.empty:
        return pd.DataFrame()
        
    records = []
    
    col_nome = df_docente.columns[2]
    col_comp = df_docente.columns[34]
    col_tema = df_docente.columns[86]
    
    col_t1_plan_lvl = df_docente.columns[82]
    col_t1_prat_lvl = df_docente.columns[84]
    col_t2_plan_lvl = df_docente.columns[78]
    col_t2_prat_lvl = df_docente.columns[80]
    
    for idx, row in df_docente.iterrows():
        cursista = row[col_nome] if pd.notna(row[col_nome]) else f"Cursista #{idx}"
        comp = row[col_comp] if pd.notna(row[col_comp]) else "Não informado"
        tema = row[col_tema] if pd.notna(row[col_tema]) else "Não informado"
        
        # Avaliações do Tema I
        if tema == 'Tema I':
            lvl_plan = row[col_t1_plan_lvl] if pd.notna(row[col_t1_plan_lvl]) else "Pendente"
            lvl_prat = row[col_t1_prat_lvl] if pd.notna(row[col_t1_prat_lvl]) else "Pendente"
            records.append({
                'registro_id': idx,
                'cursista': cursista,
                'componente': comp,
                'tema': 'Tema I',
                'dimensao': 'Planejamento',
                'nivel_atendimento': lvl_plan,
                'situacao': 'Classificado' if lvl_plan != 'Pendente' else 'Pendente'
            })
            records.append({
                'registro_id': idx,
                'cursista': cursista,
                'componente': comp,
                'tema': 'Tema I',
                'dimensao': 'Prática',
                'nivel_atendimento': lvl_prat,
                'situacao': 'Classificado' if lvl_prat != 'Pendente' else 'Pendente'
            })
        elif tema == 'Tema II':
            lvl_plan = row[col_t2_plan_lvl] if pd.notna(row[col_t2_plan_lvl]) else "Pendente"
            lvl_prat = row[col_t2_prat_lvl] if pd.notna(row[col_t2_prat_lvl]) else "Pendente"
            records.append({
                'registro_id': idx,
                'cursista': cursista,
                'componente': comp,
                'tema': 'Tema II',
                'dimensao': 'Planejamento',
                'nivel_atendimento': lvl_plan,
                'situacao': 'Classificado' if lvl_plan != 'Pendente' else 'Pendente'
            })
            records.append({
                'registro_id': idx,
                'cursista': cursista,
                'componente': comp,
                'tema': 'Tema II',
                'dimensao': 'Prática',
                'nivel_atendimento': lvl_prat,
                'situacao': 'Classificado' if lvl_prat != 'Pendente' else 'Pendente'
            })
        else:
            records.append({
                'registro_id': idx,
                'cursista': cursista,
                'componente': comp,
                'tema': 'Pendente/Indefinido',
                'dimensao': 'Geral',
                'nivel_atendimento': 'Pendente',
                'situacao': 'Pendente'
            })
            
    return pd.DataFrame(records)
