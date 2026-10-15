"""
Painel Interativo em Python - PDP 2025 (Modalidade DOCENTE)
Desenvolvido com Streamlit, Pandas e Plotly.
Atende integralmente a rules.md e task2.md.
"""

import os
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from data_loader import (
    load_and_filter_docentes,
    get_criteria_metadata,
    get_docente_evaluations
)

# Configuração da página Streamlit
st.set_page_config(
    page_title="Painel PDP 2025 - Modalidade DOCENTE",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS limpa e profissional
st.markdown("""
<style>
    .reportview-container {
        background: #fdfdfd;
    }
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .info-card {
        background-color: #EFF6FF;
        border-left: 5px solid #3B82F6;
        padding: 12px 16px;
        border-radius: 4px;
        margin-bottom: 15px;
        font-size: 0.95rem;
    }
    .warning-card {
        background-color: #FFFBEB;
        border-left: 5px solid #F59E0B;
        padding: 12px 16px;
        border-radius: 4px;
        margin-bottom: 15px;
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Cabeçalho Principal
    st.markdown('<div class="main-header">Painel Analítico PDP 2025</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Acompanhamento e Análise dos Critérios Pedagógicos e Níveis de Atendimento</div>', 
        unsafe_allow_html=True
    )

    # 2.4 Restrição obrigatória documentada
    st.markdown("""
    <div class="info-card">
        <strong>📌 Escopo da Análise:</strong> Este painel opera <strong>exclusivamente sobre registros da modalidade DOCENTE</strong> 
        do 2º Ano (Referência Docente 4 - Ferramentas Educacionais), em conformidade estrita com o documento institucional 
        <code>_DOC_PDP_2025.md</code> e as diretrizes de <code>rules.md</code>. Registros de outras modalidades são descartados na camada de dados antes de qualquer computação.
    </div>
    """, unsafe_allow_html=True)

    # Caminho do CSV
    base_dir = Path(__file__).resolve().parent.parent
    default_csv_path = base_dir / 'data' / 'arquivo_preenchido.csv'
    if not default_csv_path.exists():
        default_csv_path = base_dir / 'docs' / 'Observações e feedbacks 2024 - Teste Análise IA Checklist.csv'

    # Sidebar: Controles e Seleção de Base
    st.sidebar.header("⚙️ Configurações da Base")
    csv_input = st.sidebar.text_input(
        "Caminho do CSV:",
        value=str(default_csv_path),
        help="Informe o caminho absoluto ou relativo para a base de dados preenchida."
    )

    # Carregamento e filtragem na camada de dados
    try:
        df_docente, err_msg = load_and_filter_docentes(csv_input)
    except Exception as e:
        st.error(f"❌ Erro crítico ao carregar dados: {e}")
        st.stop()

    if err_msg:
        st.warning(f"⚠️ {err_msg}")
        st.stop()

    # Carregar metadados dos critérios e avaliações normalizadas
    df_meta = get_criteria_metadata()
    df_evals = get_docente_evaluations(df_docente)

    # Sidebar: Filtros Interativos
    st.sidebar.markdown("---")
    st.sidebar.header("🔍 Filtros Interativos")

    # Filtro 1: Tema
    tema_options = ["Todos"] + sorted(list(df_meta['tema'].unique()))
    selected_tema = st.sidebar.selectbox("Tema do PDP:", tema_options)

    # Filtro 2: Dimensão
    dim_options = ["Todas", "Planejamento", "Prática"]
    selected_dim = st.sidebar.selectbox("Dimensão de Avaliação:", dim_options)

    # Filtro 3: Nível de Atendimento
    nivel_options = ["Todos", "Atende integralmente", "Atende parcialmente", "Supera", "Não atende", "Pendente"]
    selected_nivel = st.sidebar.selectbox("Nível de Atendimento:", nivel_options)

    # Filtro 4: Situação do Preenchimento
    sit_options = ["Todas", "Classificado", "Pendente"]
    selected_sit = st.sidebar.selectbox("Situação do Preenchimento:", sit_options)

    # Filtro 5: Busca textual
    search_query = st.sidebar.text_input("Busca por texto (critério/expectativa):", "").strip().lower()

    # Aplicação dos filtros sobre os metadados dos critérios
    filtered_meta = df_meta.copy()
    if selected_tema != "Todos":
        filtered_meta = filtered_meta[filtered_meta['tema'] == selected_tema]
    if selected_dim != "Todas":
        filtered_meta = filtered_meta[filtered_meta['dimensao'] == selected_dim]
    if search_query:
        filtered_meta = filtered_meta[
            filtered_meta['criterio'].str.lower().str.contains(search_query) |
            filtered_meta['expectativa'].str.lower().str.contains(search_query)
        ]

    # Aplicação dos filtros sobre as avaliações docentes
    filtered_evals = df_evals.copy()
    if selected_tema != "Todos":
        filtered_evals = filtered_evals[filtered_evals['tema'] == selected_tema]
    if selected_dim != "Todas":
        filtered_evals = filtered_evals[filtered_evals['dimensao'] == selected_dim]
    if selected_nivel != "Todos":
        filtered_evals = filtered_evals[filtered_evals['nivel_atendimento'] == selected_nivel]
    if selected_sit != "Todas":
        filtered_evals = filtered_evals[filtered_evals['situacao'] == selected_sit]

    # -------------------------------------------------------------
    # SEÇÃO A: VISÃO GERAL
    # -------------------------------------------------------------
    st.subheader("📊 Seção A — Visão Geral dos Indicadores")
    
    total_registros_docentes = len(df_docente)
    total_criterios_distintos = len(df_meta['id_criterio'].unique())
    criterios_filtrados = len(filtered_meta['id_criterio'].unique())
    
    total_avaliacoes = len(filtered_evals)
    classificados_count = len(filtered_evals[filtered_evals['situacao'] == 'Classificado'])
    pendentes_count = len(filtered_evals[filtered_evals['situacao'] == 'Pendente'])

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Registros DOCENTE", f"{total_registros_docentes}")
    m2.metric("Critérios do PDP 2025", f"{criterios_filtrados} / {total_criterios_distintos}")
    m3.metric("Avaliações Filtradas", f"{total_avaliacoes}")
    m4.metric("Classificações Concluídas", f"{classificados_count}")
    m5.metric("Classificações Pendentes", f"{pendentes_count}")

    # Divisão em abas temáticas para visualização organizada
    tab1, tab2, tab3 = st.tabs([
        "🏛️ Análise por Tema e Critérios",
        "🎯 Níveis de Atendimento",
        "📋 Tabela Detalhada & Dados"
    ])

    # -------------------------------------------------------------
    # SEÇÃO C: ANÁLISE POR TEMA
    # -------------------------------------------------------------
    with tab1:
        st.markdown("### Comparativo e Detalhamento dos Temas do PDP 2025")
        
        c1, c2 = st.columns([1, 1])
        with c1:
            # Gráfico de critérios por tema
            theme_dist = df_meta.groupby(['tema', 'dimensao']).size().reset_index(name='qtd_criterios')
            fig_theme = px.bar(
                theme_dist,
                x='tema',
                y='qtd_criterios',
                color='dimensao',
                barmode='group',
                title="Distribuição Oficial de Critérios por Tema e Dimensão",
                labels={'qtd_criterios': 'Quantidade de Critérios', 'tema': 'Tema do PDP', 'dimensao': 'Dimensão'},
                color_discrete_map={'Planejamento': '#2563EB', 'Prática': '#10B981'}
            )
            fig_theme.update_layout(template="plotly_white")
            st.plotly_chart(fig_theme, use_container_width=True)

        with c2:
            # Avaliações registradas por tema
            eval_by_theme = df_docente[df_docente.columns[86]].value_counts().reset_index()
            eval_by_theme.columns = ['Tema Escolhido', 'Docentes Atendidos']
            fig_doc_theme = px.pie(
                eval_by_theme,
                names='Tema Escolhido',
                values='Docentes Atendidos',
                title="Adesão dos Docentes por Tema de Implementação",
                color_discrete_sequence=['#3B82F6', '#8B5CF6']
            )
            fig_doc_theme.update_layout(template="plotly_white")
            st.plotly_chart(fig_doc_theme, use_container_width=True)

        st.markdown("#### Detalhamento das Expectativas e Critérios Institucionais")
        for tema in ["Tema I", "Tema II"]:
            meta_tema = df_meta[df_meta['tema'] == tema]
            with st.expander(f"📌 {tema} — {meta_tema.iloc[0]['tema_titulo']}", expanded=(tema == "Tema I")):
                st.markdown(f"**Expectativa Institucional Oficial:**\n> {meta_tema.iloc[0]['expectativa']}")
                st.markdown("**Critérios de Avaliação:**")
                
                t_cols = ['id_criterio', 'dimensao', 'criterio']
                st.dataframe(
                    meta_tema[t_cols].rename(columns={
                        'id_criterio': 'ID',
                        'dimensao': 'Dimensão',
                        'criterio': 'Critério Institucional'
                    }),
                    hide_index=True,
                    use_container_width=True
                )

    # -------------------------------------------------------------
    # SEÇÃO D: NÍVEIS DE ATENDIMENTO
    # -------------------------------------------------------------
    with tab2:
        st.markdown("### Avaliação dos Níveis de Atendimento Institucional")
        
        st.markdown("""
        <div class="info-card">
            Os níveis de atendimento retratam a consonância entre o desempenho observado do docente e as expectativas do PDP 2025. 
            Utilizam-se exclusivamente os quatro rótulos oficiais: <strong>Não atende</strong>, <strong>Atende parcialmente</strong>, 
            <strong>Atende integralmente</strong> e <strong>Supera</strong>. Registros sem dados suficientes são preservados como <em>Pendente</em>.
        </div>
        """, unsafe_allow_html=True)

        if filtered_evals.empty:
            st.info("Nenhuma avaliação encontrada com os filtros selecionados.")
        else:
            col_e1, col_e2 = st.columns([1, 1])
            lvl_order = ["Atende integralmente", "Atende parcialmente", "Supera", "Não atende", "Pendente"]
            lvl_colors = {
                "Atende integralmente": "#10B981",
                "Atende parcialmente": "#F59E0B",
                "Supera": "#6366F1",
                "Não atende": "#EF4444",
                "Pendente": "#9CA3AF"
            }

            with col_e1:
                # Proporção por nível
                lvl_counts = filtered_evals['nivel_atendimento'].value_counts().reset_index()
                lvl_counts.columns = ['Nível de Atendimento', 'Quantidade']
                fig_lvl = px.pie(
                    lvl_counts,
                    names='Nível de Atendimento',
                    values='Quantidade',
                    color='Nível de Atendimento',
                    color_discrete_map=lvl_colors,
                    title="Proporção Geral dos Níveis de Atendimento"
                )
                fig_lvl.update_layout(template="plotly_white")
                st.plotly_chart(fig_lvl, use_container_width=True)

            with col_e2:
                # Distribuição por dimensão
                lvl_by_dim = filtered_evals.groupby(['dimensao', 'nivel_atendimento']).size().reset_index(name='qtd')
                fig_lvl_dim = px.bar(
                    lvl_by_dim,
                    x='dimensao',
                    y='qtd',
                    color='nivel_atendimento',
                    barmode='stack',
                    color_discrete_map=lvl_colors,
                    title="Níveis de Atendimento por Dimensão Pedagógica",
                    labels={'dimensao': 'Dimensão', 'qtd': 'Avaliações', 'nivel_atendimento': 'Nível'}
                )
                fig_lvl_dim.update_layout(template="plotly_white")
                st.plotly_chart(fig_lvl_dim, use_container_width=True)

            # Tabela resumo de frequências
            st.markdown("#### Frequência e Percentual por Nível de Atendimento")
            summary_table = filtered_evals.groupby('nivel_atendimento').agg(
                Quantidade=('registro_id', 'count')
            ).reset_index()
            summary_table['Proporção (%)'] = (summary_table['Quantidade'] / len(filtered_evals) * 100).round(2)
            st.dataframe(summary_table, hide_index=True, use_container_width=True)

    # -------------------------------------------------------------
    # SEÇÃO E: TABELA DETALHADA
    # -------------------------------------------------------------
    with tab3:
        st.markdown("### Registros Filtrados da Modalidade DOCENTE")
        st.markdown("Consulta interativa com capacidade de ordenação, pesquisa e rastreamento da base de dados original.")

        # Opção de exibição: avaliações normalizadas ou registros brutos
        view_mode = st.radio(
            "Modo de Visualização:",
            ["Visão Analítica por Avaliação Docente", "Visão dos Registros Originais Filtrados"],
            horizontal=True
        )

        if view_mode == "Visão Analítica por Avaliação Docente":
            st.dataframe(
                filtered_evals.rename(columns={
                    'registro_id': 'Linha Base',
                    'cursista': 'Nome do Cursista',
                    'componente': 'Componente Curricular',
                    'tema': 'Tema',
                    'dimensao': 'Dimensão',
                    'nivel_atendimento': 'Nível de Atendimento (IA)',
                    'situacao': 'Situação'
                }),
                hide_index=True,
                use_container_width=True
            )
        else:
            # Exibir colunas úteis dos registros originais da modalidade Docente
            display_cols = [
                df_docente.columns[0],   # Carimbo
                df_docente.columns[2],   # Nome
                df_docente.columns[34],  # Componente
                df_docente.columns[86],  # Tema
                df_docente.columns[82],  # IA T1 Plan
                df_docente.columns[84],  # IA T1 Prat
                df_docente.columns[78],  # IA T2 Plan
                df_docente.columns[80],  # IA T2 Prat
                df_docente.columns[58],  # Pontos fortes
                df_docente.columns[59]   # Pontos melhoria
            ]
            st.dataframe(
                df_docente[display_cols].fillna("-"),
                use_container_width=True
            )

        st.caption(f"Exibindo {len(filtered_evals)} avaliações correspondentes aos filtros ativos.")

if __name__ == '__main__':
    main()
