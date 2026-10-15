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
    },
    {
        'id_criterio': 'T1_PL_02',
        'tema': 'Tema I',
        'tema_titulo': 'Recursos Educacionais Digitais',
        'dimensao': 'Planejamento',
        'criterio': 'A proposta pedagógica apresenta um recurso educacional digital oferecido pela secretaria',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando um recurso educacional digital como apoio pedagógico.',
    },
    {
        'id_criterio': 'T1_PL_03',
        'tema': 'Tema I',
        'tema_titulo': 'Recursos Educacionais Digitais',
        'dimensao': 'Planejamento',
        'criterio': 'O recurso educacional digital selecionado do seu componente, caso tenha',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando um recurso educacional digital como apoio pedagógico.',
    },
    {
        'id_criterio': 'T1_PL_04',
        'tema': 'Tema I',
        'tema_titulo': 'Recursos Educacionais Digitais',
        'dimensao': 'Planejamento',
        'criterio': 'A proposta apresenta para a recomposição uma habilidade prioritária de seu componente',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando um recurso educacional digital como apoio pedagógico.',
    },
    {
        'id_criterio': 'T1_PL_05',
        'tema': 'Tema I',
        'tema_titulo': 'Recursos Educacionais Digitais',
        'dimensao': 'Planejamento',
        'criterio': 'A proposta de planejamento explora o recurso educacional digital relacionando-o à recomposição das aprendizagens',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando um recurso educacional digital como apoio pedagógico.',
    },
    {
        'id_criterio': 'T1_PL_06',
        'tema': 'Tema I',
        'tema_titulo': 'Recursos Educacionais Digitais',
        'dimensao': 'Planejamento',
        'criterio': 'Descreve as ações a serem realizadas na implementação da prática respondendo a todas as questões do planejamento',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando um recurso educacional digital como apoio pedagógico.',
    },
    {
        'id_criterio': 'T1_PL_07',
        'tema': 'Tema I',
        'tema_titulo': 'Recursos Educacionais Digitais',
        'dimensao': 'Planejamento',
        'criterio': 'Descreve os resultados esperados com a implementação do planejamento',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando um recurso educacional digital como apoio pedagógico.',
    },

    # TEMA I - PRÁTICA
    {
        'id_criterio': 'T1_PR_01',
        'tema': 'Tema I',
        'tema_titulo': 'Recursos Educacionais Digitais',
        'dimensao': 'Prática',
        'criterio': 'Informa aos estudantes os objetivos de aprendizagem da proposta pedagógica',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando um recurso educacional digital como apoio pedagógico.',
    },
    {
        'id_criterio': 'T1_PR_02',
        'tema': 'Tema I',
        'tema_titulo': 'Recursos Educacionais Digitais',
        'dimensao': 'Prática',
        'criterio': 'Explica aos estudantes o porquê da aula e/ou atividade voltada para a recomposição',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando um recurso educacional digital como apoio pedagógico.',
    },
    {
        'id_criterio': 'T1_PR_03',
        'tema': 'Tema I',
        'tema_titulo': 'Recursos Educacionais Digitais',
        'dimensao': 'Prática',
        'criterio': 'Apresenta aos estudantes o recurso educacional digital que será utilizado durante aula e/ou atividade',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando um recurso educacional digital como apoio pedagógico.',
    },
    {
        'id_criterio': 'T1_PR_04',
        'tema': 'Tema I',
        'tema_titulo': 'Recursos Educacionais Digitais',
        'dimensao': 'Prática',
        'criterio': 'A aula e/ou atividade corresponde à descrição das ações presentes no planejamento',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando um recurso educacional digital como apoio pedagógico.',
    },
    {
        'id_criterio': 'T1_PR_05',
        'tema': 'Tema I',
        'tema_titulo': 'Recursos Educacionais Digitais',
        'dimensao': 'Prática',
        'criterio': 'Evidencia-se o domínio do professor na utilização do recurso educacional digital utilizado',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando um recurso educacional digital como apoio pedagógico.',
    },
    {
        'id_criterio': 'T1_PR_06',
        'tema': 'Tema I',
        'tema_titulo': 'Recursos Educacionais Digitais',
        'dimensao': 'Prática',
        'criterio': 'Adapta a prática a possíveis imprevistos técnicos que possam ocorrer',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando um recurso educacional digital como apoio pedagógico.',
    },
    {
        'id_criterio': 'T1_PR_07',
        'tema': 'Tema I',
        'tema_titulo': 'Recursos Educacionais Digitais',
        'dimensao': 'Prática',
        'criterio': 'Promove uma personalização do ensino a partir do trabalho com o recurso educacional escolhido',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando um recurso educacional digital como apoio pedagógico.',
    },

    # TEMA II - PLANEJAMENTO
    {
        'id_criterio': 'T2_PL_01',
        'tema': 'Tema II',
        'tema_titulo': 'Ferramentas Educacionais',
        'dimensao': 'Planejamento',
        'criterio': 'Descreve o objetivo da proposta pedagógica',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando duas ou mais ferramentas educacionais.',
    },
    {
        'id_criterio': 'T2_PL_02',
        'tema': 'Tema II',
        'tema_titulo': 'Ferramentas Educacionais',
        'dimensao': 'Planejamento',
        'criterio': 'A proposta pedagógica apresenta mais de uma ferramenta educacional oferecida pela secretaria',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando duas ou mais ferramentas educacionais.',
    },
    {
        'id_criterio': 'T2_PL_03',
        'tema': 'Tema II',
        'tema_titulo': 'Ferramentas Educacionais',
        'dimensao': 'Planejamento',
        'criterio': 'A proposta apresenta para a recomposição de um habilidade prioritária de seu componente',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando duas ou mais ferramentas educacionais.',
    },
    {
        'id_criterio': 'T2_PL_04',
        'tema': 'Tema II',
        'tema_titulo': 'Ferramentas Educacionais',
        'dimensao': 'Planejamento',
        'criterio': 'A proposta de planejamento explora ferramentas educacionais relacionando-as à recomposição das aprendizagens',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando duas ou mais ferramentas educacionais.',
    },
    {
        'id_criterio': 'T2_PL_05',
        'tema': 'Tema II',
        'tema_titulo': 'Ferramentas Educacionais',
        'dimensao': 'Planejamento',
        'criterio': 'Descreve as ações a serem realizadas na implementação da prática respondendo a todas as questões do planejamento',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando duas ou mais ferramentas educacionais.',
    },
    {
        'id_criterio': 'T2_PL_06',
        'tema': 'Tema II',
        'tema_titulo': 'Ferramentas Educacionais',
        'dimensao': 'Planejamento',
        'criterio': 'Descreve os resultados esperados com a implementação do planejamento',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando duas ou mais ferramentas educacionais.',
    },

    # TEMA II - PRÁTICA
    {
        'id_criterio': 'T2_PR_01',
        'tema': 'Tema II',
        'tema_titulo': 'Ferramentas Educacionais',
        'dimensao': 'Prática',
        'criterio': 'Informa aos estudantes os objetivos de aprendizagem da proposta pedagógica',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando duas ou mais ferramentas educacionais.',
    },
    {
        'id_criterio': 'T2_PR_02',
        'tema': 'Tema II',
        'tema_titulo': 'Ferramentas Educacionais',
        'dimensao': 'Prática',
        'criterio': 'Explica aos estudantes o porquê da aula e/ou atividade voltada para a recomposição',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando duas ou mais ferramentas educacionais.',
    },
    {
        'id_criterio': 'T2_PR_03',
        'tema': 'Tema II',
        'tema_titulo': 'Ferramentas Educacionais',
        'dimensao': 'Prática',
        'criterio': 'Apresenta aos estudantes a(s) ferramenta(s) educacional(is) que serão utilizados na aula e/ou atividade',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando duas ou mais ferramentas educacionais.',
    },
    {
        'id_criterio': 'T2_PR_04',
        'tema': 'Tema II',
        'tema_titulo': 'Ferramentas Educacionais',
        'dimensao': 'Prática',
        'criterio': 'A aula e/ou atividade corresponde à descrição das ações presentes no planejamento',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando duas ou mais ferramentas educacionais.',
    },
    {
        'id_criterio': 'T2_PR_05',
        'tema': 'Tema II',
        'tema_titulo': 'Ferramentas Educacionais',
        'dimensao': 'Prática',
        'criterio': 'Evidencia-se o domínio do professor,na utilização da(s) ferramenta(s) educacional(is)',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando duas ou mais ferramentas educacionais.',
    },
    {
        'id_criterio': 'T2_PR_06',
        'tema': 'Tema II',
        'tema_titulo': 'Ferramentas Educacionais',
        'dimensao': 'Prática',
        'criterio': 'Adapta a prática a possíveis imprevistos técnicos que possam ocorrer',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando duas ou mais ferramentas educacionais.',
    },
    {
        'id_criterio': 'T2_PR_07',
        'tema': 'Tema II',
        'tema_titulo': 'Ferramentas Educacionais',
        'dimensao': 'Prática',
        'criterio': 'Promove uma personalização do ensino a partir do trabalho com a ferramenta educacional escolhida',
        'expectativa': 'Espera-se que o docente desenvolva uma proposta pedagógica de recomposição das aprendizagens com uma habilidade prioritária de seu componente, utilizando duas ou mais ferramentas educacionais.',
    }
]

def get_criteria_metadata():
    """Retorna DataFrame com o catálogo oficial dos critérios institucionais."""
    return pd.DataFrame(CRITERIA_METADATA)

# Estrutura Oficial da Rubrica do PDP 2026 (Referência Docente 04)
RUBRICA_2026_METADATA = {
    'criterio_1': {
        'titulo': 'Critério 1: Articulação Intencional',
        'enunciado': (
            'Articulação intencional entre a habilidade essencial selecionada, '
            'o(s) objetivo(s) de aprendizagem e o recurso ou ferramenta educacional digital, '
            'utilizado como apoio pedagógico à aprendizagem.'
        ),
        'descritores': {
            'Não atende': 'O(A) professor(a): Não cumpre os requisitos mínimos do nível ATENDE PARCIALMENTE.',
            'Atende parcialmente': (
                'O(A) professor(a): Relaciona a habilidade essencial, os objetivos de aprendizagem '
                'e o recurso ou ferramenta educacional digital. Utiliza o recurso ou ferramenta educacional digital, '
                'mas sua função pedagógica não está claramente definida ou aparece de maneira periférica '
                '(ex.: apoio expositivo, sem interação ou contribuição direta para a aprendizagem).'
            ),
            'Atende integralmente': (
                'O(A) professor(a): Articula a habilidade essencial, os objetivos de aprendizagem e o recurso '
                'ou ferramenta educacional digital. Utiliza o recurso ou ferramenta educacional digital com '
                'intencionalidade pedagógica, contribuindo diretamente para o desenvolvimento da habilidade essencial '
                '(ex.: apoio à explicação, prática orientada, realização de atividades pelos estudantes com o uso '
                'do recurso ou ferramenta educacional digital).'
            ),
            'Supera': (
                'O(A) professor(a): Cumpre todos os requisitos do nível ATENDE INTEGRALMENTE e Promove o uso ativo '
                'da tecnologia pelos estudantes em situações de produção, investigação, resolução de problemas ou colaboração.'
            )
        }
    },
    'criterio_2': {
        'titulo': 'Critério 2: Mediação e Uso Ativo pelos Estudantes',
        'enunciado': (
            'Utilização do recurso ou ferramenta educacional digital como apoio pedagógico '
            'para desenvolver a habilidade essencial selecionada.'
        ),
        'descritores': {
            'Não atende': 'O(A) professor(a): Não cumpre os requisitos mínimos do nível ATENDE PARCIALMENTE.',
            'Atende parcialmente': (
                'O(A) professor(a): Mobiliza o uso do recurso ou ferramenta educacional digital em momentos pontuais da aula, '
                'restritos a etapas específicas da atividade. Realiza orientações frequentes e detalhadas, com condução passo '
                'a passo do uso do recurso ou ferramenta educacional digital, limitando a autonomia dos estudantes. Utiliza o recurso '
                'ou ferramenta educacional digital principalmente como apoio complementar (ex.: consulta, reprodução ou execução '
                'mecânica de tarefas), apresentando uma relação limitada com a habilidade essencial selecionada.'
            ),
            'Atende integralmente': (
                'O(A) professor(a): Mobiliza o uso do recurso ou ferramenta educacional digital pelos estudantes de forma intencional '
                'e articulada à atividade pedagógica. Atua como mediador, fornecendo instruções claras quanto à atividade, '
                'possibilitando que os estudantes explorem o recurso ou ferramenta educacional digital. Integra o recurso ou ferramenta '
                'educacional digital às etapas da aula, com o uso ao longo da atividade e não apenas em momentos isolados, '
                'evidenciando uma relação clara com a habilidade essencial selecionada.'
            ),
            'Supera': (
                'O(A) professor(a): Cumpre todos os requisitos do nível ATENDE INTEGRALMENTE e Organiza situações em que '
                'os estudantes utilizam o recurso ou ferramenta educacional digital com autonomia, protagonismo e tomada de decisão. '
                'Promove o uso do recurso ou ferramenta educacional digital em práticas de investigação, produção, resolução de '
                'problemas ou colaboração.'
            )
        }
    },
    'planejamento': {
        'titulo': 'Planejamento Estruturado (Etapas da Proposta I)',
        'enunciado': (
            'Indicação de turma, seleção de habilidade essencial do Currículo Paranaense, definição de objetivos de '
            'aprendizagem articulados, indicação de recursos/ferramentas digitais com intencionalidade pedagógica, '
            'descrição das ações em tópicos e resultados esperados.'
        ),
        'descritores': {
            'Não atende': 'Planejamento inicial ou com ausência dos elementos estruturantes (≤ 1 elemento).',
            'Atende parcialmente': 'Planejamento fragmentado (2 a 3 elementos estruturantes presentes).',
            'Atende integralmente': 'Planejamento articulado e consistente (4 a 6 elementos estruturantes presentes).',
            'Supera': 'Planejamento integral plenamente articulado e com proposta destacada de inovação ou replicação.'
        }
    }
}

def get_rubrica_2026_metadata():
    """Retorna os metadados e descritores oficiais da Rubrica PDP 2026."""
    return RUBRICA_2026_METADATA

def get_justificativa_rubrica_2026(dimensao, nivel):
    """Gera a fundamentação pedagógica do enquadramento na régua do PDP 2026."""
    if nivel == 'Pendente':
        return "Registro sem dados suficientes ou pendente de evidência na base original."
    
    if dimensao == 'Planejamento':
        if nivel == 'Não atende':
            return (
                "Planejamento inicial/insuficiente (≤ 1 elemento estruturante). Ausência de articulação "
                "entre habilidade essencial, objetivos pedagógicos e justificativa do recurso digital."
            )
        elif nivel == 'Atende parcialmente':
            return (
                "Planejamento fragmentado (2 a 3 elementos). O plano cita a tecnologia, mas não especifica "
                "a intencionalidade formativa na recomposição ou não detalha as etapas de implementação."
            )
        elif nivel == 'Atende integralmente':
            return (
                "Planejamento estruturado e intencional (4 a 6 elementos). Articula habilidade prioritária, "
                "objetivos didáticos claros, etapas de mediação com tecnologia e resultados de aprendizagem esperados."
            )
        elif nivel == 'Supera':
            return (
                "Planejamento de referência, plenamente articulado aos objetivos curriculares e demonstrando "
                "potencial inovador ou modelo replicável para outros docentes da rede."
            )
    
    # Prática Docente (Critérios 1 e 2 da Rubrica 2026)
    if nivel == 'Não atende':
        return (
            "Critérios 1 e 2 não atendidos: ausência de aula gravada ou evidências mínimas (≤ 1 item do checklist 2025), "
            "sem demonstração de intencionalidade pedagógica ou mediação com os estudantes."
        )
    elif nivel == 'Atende parcialmente':
        return (
            "Enquadramento no nível Parcial de 2026: a tecnologia foi mobilizada de forma periférica ou expositiva "
            "(Critério 1 < 2 itens de articulação) ou com condução mecânica/passo a passo sem promover exploração autônoma "
            "ou mediação ativa com os estudantes (Critério 2)."
        )
    elif nivel == 'Atende integralmente':
        return (
            "Enquadramento pleno na Rubrica 2026: articulação intencional consistente entre objetivos e tecnologia "
            "(Critério 1) aliada à mediação pedagógica efetiva, na qual os estudantes exploram a ferramenta de forma "
            "integrada ao longo da aula (Critério 2)."
        )
    elif nivel == 'Supera':
        return (
            "Enquadramento no nível Supera da Rubrica 2026: cumpre integralmente os requisitos estruturantes dos "
            "Critérios 1 e 2 E organiza situações em que os estudantes utilizam a tecnologia com autonomia, protagonismo, "
            "investigação ou produção ativa, com destaque qualitativo registrado pelo observador pedagógico."
        )
    return "Avaliação em conformidade com as diretrizes do PDP."

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
    respeitando as colunas de classificação e incorporando a justificativa pedagógica
    segundo a Rubrica PDP 2026.
    """
    if df_docente.empty:
        return pd.DataFrame()
        
    records = []
    
    col_nome = df_docente.columns[2]
    col_comp = df_docente.columns[34]
    col_tema = df_docente.columns[86]
    
    col_pf = df_docente.columns[58] if len(df_docente.columns) > 58 else None
    col_pm = df_docente.columns[59] if len(df_docente.columns) > 59 else None
    col_ref = df_docente.columns[65] if len(df_docente.columns) > 65 else None
    
    col_t2_plan_src = df_docente.columns[79] if len(df_docente.columns) > 79 else None
    col_t2_plan_dst = df_docente.columns[78] if len(df_docente.columns) > 78 else None
    col_t2_prat_src = df_docente.columns[81] if len(df_docente.columns) > 81 else None
    col_t2_prat_dst = df_docente.columns[80] if len(df_docente.columns) > 80 else None
    
    col_t1_plan_src = df_docente.columns[83] if len(df_docente.columns) > 83 else None
    col_t1_plan_dst = df_docente.columns[82] if len(df_docente.columns) > 82 else None
    col_t1_prat_src = df_docente.columns[85] if len(df_docente.columns) > 85 else None
    col_t1_prat_dst = df_docente.columns[84] if len(df_docente.columns) > 84 else None
    
    for idx, row in df_docente.iterrows():
        cursista = row[col_nome] if pd.notna(row[col_nome]) else f"Cursista #{idx}"
        comp = row[col_comp] if pd.notna(row[col_comp]) else "Não informado"
        tema = row[col_tema] if pd.notna(row[col_tema]) else "Não informado"
        
        pf_text = str(row[col_pf]) if col_pf and pd.notna(row[col_pf]) else ""
        pm_text = str(row[col_pm]) if col_pm and pd.notna(row[col_pm]) else ""
        
        # Avaliações do Tema I
        if tema == 'Tema I':
            lvl_plan = row[col_t1_plan_dst] if col_t1_plan_dst and pd.notna(row[col_t1_plan_dst]) else "Pendente"
            lvl_prat = row[col_t1_prat_dst] if col_t1_prat_dst and pd.notna(row[col_t1_prat_dst]) else "Pendente"
            src_plan = str(row[col_t1_plan_src]) if col_t1_plan_src and pd.notna(row[col_t1_plan_src]) else ""
            src_prat = str(row[col_t1_prat_src]) if col_t1_prat_src and pd.notna(row[col_t1_prat_src]) else ""
            
            records.append({
                'registro_id': idx,
                'cursista': cursista,
                'componente': comp,
                'tema': 'Tema I',
                'dimensao': 'Planejamento',
                'nivel_atendimento': lvl_plan,
                'situacao': 'Classificado' if lvl_plan != 'Pendente' else 'Pendente',
                'justificativa_rubrica_2026': get_justificativa_rubrica_2026('Planejamento', lvl_plan),
                'evidencias_checklist_2025': src_plan,
                'pontos_fortes': pf_text,
                'pontos_melhoria': pm_text
            })
            records.append({
                'registro_id': idx,
                'cursista': cursista,
                'componente': comp,
                'tema': 'Tema I',
                'dimensao': 'Prática',
                'nivel_atendimento': lvl_prat,
                'situacao': 'Classificado' if lvl_prat != 'Pendente' else 'Pendente',
                'justificativa_rubrica_2026': get_justificativa_rubrica_2026('Prática', lvl_prat),
                'evidencias_checklist_2025': src_prat,
                'pontos_fortes': pf_text,
                'pontos_melhoria': pm_text
            })
        elif tema == 'Tema II':
            lvl_plan = row[col_t2_plan_dst] if col_t2_plan_dst and pd.notna(row[col_t2_plan_dst]) else "Pendente"
            lvl_prat = row[col_t2_prat_dst] if col_t2_prat_dst and pd.notna(row[col_t2_prat_dst]) else "Pendente"
            src_plan = str(row[col_t2_plan_src]) if col_t2_plan_src and pd.notna(row[col_t2_plan_src]) else ""
            src_prat = str(row[col_t2_prat_src]) if col_t2_prat_src and pd.notna(row[col_t2_prat_src]) else ""
            
            records.append({
                'registro_id': idx,
                'cursista': cursista,
                'componente': comp,
                'tema': 'Tema II',
                'dimensao': 'Planejamento',
                'nivel_atendimento': lvl_plan,
                'situacao': 'Classificado' if lvl_plan != 'Pendente' else 'Pendente',
                'justificativa_rubrica_2026': get_justificativa_rubrica_2026('Planejamento', lvl_plan),
                'evidencias_checklist_2025': src_plan,
                'pontos_fortes': pf_text,
                'pontos_melhoria': pm_text
            })
            records.append({
                'registro_id': idx,
                'cursista': cursista,
                'componente': comp,
                'tema': 'Tema II',
                'dimensao': 'Prática',
                'nivel_atendimento': lvl_prat,
                'situacao': 'Classificado' if lvl_prat != 'Pendente' else 'Pendente',
                'justificativa_rubrica_2026': get_justificativa_rubrica_2026('Prática', lvl_prat),
                'evidencias_checklist_2025': src_prat,
                'pontos_fortes': pf_text,
                'pontos_melhoria': pm_text
            })
        else:
            records.append({
                'registro_id': idx,
                'cursista': cursista,
                'componente': comp,
                'tema': 'Pendente/Indefinido',
                'dimensao': 'Geral',
                'nivel_atendimento': 'Pendente',
                'situacao': 'Pendente',
                'justificativa_rubrica_2026': get_justificativa_rubrica_2026('Geral', 'Pendente'),
                'evidencias_checklist_2025': "",
                'pontos_fortes': pf_text,
                'pontos_melhoria': pm_text
            })
            
    return pd.DataFrame(records)

