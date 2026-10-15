"""
Painel Interativo em Python - PDP (Adequação à Rubrica 2026)
Desenvolvido com Streamlit, Pandas e Plotly.
Apresenta os dados observados em 2025 adequados e justificados sob a ótica
da Rubrica Analítica do PDP 2026 (Referência Docente 4).
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
    get_rubrica_2026_metadata,
    get_docente_evaluations
)

# Configuração da página Streamlit
st.set_page_config(
    page_title="Painel PDP — Projeção Pedagógica na Rubrica 2026",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS profissional
st.markdown("""
<style>
    .main-header {
        font-size: 2.1rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.2rem;
    }
    .info-card {
        background-color: #EFF6FF;
        border-left: 5px solid #3B82F6;
        padding: 14px 18px;
        border-radius: 6px;
        margin-bottom: 18px;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    .rubric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 16px;
    }
    .metric-container {
        background: white;
        border-radius: 8px;
        padding: 12px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .badge-supera {
        background-color: #EEF2FF;
        color: #4338CA;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.85rem;
        border: 1px solid #C7D2FE;
    }
    .badge-integral {
        background-color: #ECFDF5;
        color: #065F46;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.85rem;
        border: 1px solid #A7F3D0;
    }
    .badge-parcial {
        background-color: #FFFBEB;
        color: #92400E;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.85rem;
        border: 1px solid #FDE68A;
    }
    .badge-nao {
        background-color: #FEF2F2;
        color: #991B1B;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.85rem;
        border: 1px solid #FECACA;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Cabeçalho Principal
    st.markdown('<div class="main-header">Painel Analítico PDP — Projeção Pedagógica na Rubrica 2026</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Reenquadramento formativo dos dados de 2025 à luz das Rubricas Analíticas do PDP 2026 (Referência Docente 4)</div>', 
        unsafe_allow_html=True
    )

    # Contexto e Escopo Obrigatório
    st.markdown("""
    <div class="info-card">
        <strong>📌 Contexto da Transição Pedagógica (2025 ➔ 2026):</strong><br>
        Em 2025, o acompanhamento foi registrado por meio de um checklist somatório de itens observados. 
        Para o ciclo de 2026 (<code>PDP_DOCENTES_Referência 04_2026.md</code>), a rede adota <strong>Rubricas Analíticas</strong> 
        focadas em dois eixos qualitativos essenciais: <strong>Critério 1 (Articulação Intencional)</strong> e 
        <strong>Critério 2 (Mediação e Uso Ativo pelos Estudantes)</strong>.<br>
        Este painel reinterpreta e classifica a base de 2025 através da régua qualitativa de 2026, 
        apresentando justificativas pedagógicas detalhadas para cada enquadramento. Operação restrita à modalidade 
        <strong>DOCENTE (2º Ano - Referência Docente 4)</strong>.
    </div>
    """, unsafe_allow_html=True)

    # Localização da base de dados
    base_dir = Path(__file__).resolve().parent.parent
    default_csv_path = base_dir / 'data' / 'arquivo_preenchido.csv'
    if not default_csv_path.exists():
        default_csv_path = base_dir / 'docs' / 'Observações e feedbacks 2024 - Teste Análise IA Checklist.csv'

    # Sidebar: Controles e Arquivo
    st.sidebar.header("⚙️ Configurações da Base")
    csv_input = st.sidebar.text_input(
        "Caminho da base de dados:",
        value=str(default_csv_path),
        help="Informe o caminho absoluto ou relativo para a base preenchida com a classificação 2026."
    )

    # Carregamento e filtragem estrita na camada de dados
    try:
        df_docente, err_msg = load_and_filter_docentes(csv_input)
    except Exception as e:
        st.error(f"❌ Erro crítico ao carregar dados: {e}")
        st.stop()

    if err_msg:
        st.warning(f"⚠️ {err_msg}")
        st.stop()

    # Extração de metadados e avaliações normalizadas
    df_meta_2025 = get_criteria_metadata()
    rubrica_2026 = get_rubrica_2026_metadata()
    df_evals = get_docente_evaluations(df_docente)

    # Sidebar: Filtros Interativos
    st.sidebar.markdown("---")
    st.sidebar.header("🔍 Filtros Interativos")

    # Filtro de Tema
    tema_options = ["Todos"] + sorted(list(df_evals['tema'].unique()))
    selected_tema = st.sidebar.selectbox("Tema de Implementação:", tema_options)

    # Filtro de Dimensão
    dim_options = ["Todas", "Planejamento", "Prática"]
    selected_dim = st.sidebar.selectbox("Dimensão Pedagógica:", dim_options)

    # Filtro de Nível de Atendimento
    nivel_options = ["Todos", "Atende integralmente", "Supera", "Atende parcialmente", "Não atende", "Pendente"]
    selected_nivel = st.sidebar.selectbox("Nível de Atendimento (2026):", nivel_options)

    # Filtro de Componente Curricular
    comp_list = sorted([c for c in df_evals['componente'].unique() if c != "Não informado"])
    comp_options = ["Todos"] + comp_list
    selected_comp = st.sidebar.selectbox("Componente Curricular:", comp_options)

    # Busca textual por nome do professor ou palavra-chave
    search_query = st.sidebar.text_input("Busca por Professor ou Palavra:", "").strip().lower()

    # Aplicação dos filtros sobre as avaliações
    filtered_evals = df_evals.copy()
    if selected_tema != "Todos":
        filtered_evals = filtered_evals[filtered_evals['tema'] == selected_tema]
    if selected_dim != "Todas":
        filtered_evals = filtered_evals[filtered_evals['dimensao'] == selected_dim]
    if selected_nivel != "Todos":
        filtered_evals = filtered_evals[filtered_evals['nivel_atendimento'] == selected_nivel]
    if selected_comp != "Todos":
        filtered_evals = filtered_evals[filtered_evals['componente'] == selected_comp]
    if search_query:
        filtered_evals = filtered_evals[
            filtered_evals['cursista'].str.lower().str.contains(search_query) |
            filtered_evals['justificativa_rubrica_2026'].str.lower().str.contains(search_query) |
            filtered_evals['pontos_fortes'].str.lower().str.contains(search_query)
        ]

    # -------------------------------------------------------------
    # INDICADORES PRINCIPAIS (KPIs)
    # -------------------------------------------------------------
    st.subheader("📊 Indicadores Gerais — Projeção na Rubrica 2026")
    
    total_docentes = len(df_docente)
    total_avaliacoes = len(filtered_evals)
    
    count_integral = len(filtered_evals[filtered_evals['nivel_atendimento'] == 'Atende integralmente'])
    count_supera = len(filtered_evals[filtered_evals['nivel_atendimento'] == 'Supera'])
    count_parcial = len(filtered_evals[filtered_evals['nivel_atendimento'] == 'Atende parcialmente'])
    count_nao = len(filtered_evals[filtered_evals['nivel_atendimento'] == 'Não atende'])

    pct_integral = (count_integral / total_avaliacoes * 100) if total_avaliacoes > 0 else 0
    pct_supera = (count_supera / total_avaliacoes * 100) if total_avaliacoes > 0 else 0
    pct_parcial = (count_parcial / total_avaliacoes * 100) if total_avaliacoes > 0 else 0
    pct_nao = (count_nao / total_avaliacoes * 100) if total_avaliacoes > 0 else 0

    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    kpi1.metric("Total Docentes (Amostra)", f"{total_docentes}")
    kpi2.metric("Atende Integralmente", f"{count_integral}", f"{pct_integral:.1f}%")
    kpi3.metric("Supera (Protagonismo)", f"{count_supera}", f"{pct_supera:.1f}%")
    kpi4.metric("Atende Parcialmente", f"{count_parcial}", f"{pct_parcial:.1f}%")
    kpi5.metric("Não Atende", f"{count_nao}", f"{pct_nao:.1f}%")

    # Cores padronizadas oficiais
    palette_colors = {
        "Atende integralmente": "#10B981",  # Verde esmeralda
        "Supera": "#6366F1",               # Índigo / Roxo moderno
        "Atende parcialmente": "#F59E0B",   # Âmbar / Laranja formativo
        "Não atende": "#EF4444",            # Vermelho
        "Pendente": "#9CA3AF"               # Cinza
    }

    # -------------------------------------------------------------
    # NAVEGAÇÃO EM ABAS
    # -------------------------------------------------------------
    tab1, tab2, tab3, tab4 = st.tabs([
        "🏛️ Matriz de Equiparação: PDP 2025 ➔ 2026",
        "📈 Panorama & Análise da Régua 2026",
        "🔍 Consulta & Justificativas Individuais",
        "📋 Dados Brutos & Rastreabilidade"
    ])

    # -------------------------------------------------------------
    # ABA 1: EQUIPARAÇÃO METODOLÓGICA (RUBRICAS 2026)
    # -------------------------------------------------------------
    with tab1:
        st.markdown("### 🏛️ Estrutura Analítica da Rubrica PDP 2026 (Referência Docente 4)")
        
        st.markdown("""
        No modelo original de 2025, a régua utilizava um checklist dicotômico (marcado/não marcado), 
        gerando distorções como professores caindo em 'Parcial' apenas pela ausência de um item formal, 
        mesmo com excelente prática mediadora.
        <br><br>
        A <strong>Rubrica do PDP 2026</strong> soluciona isso estruturando a avaliação em 
        <strong>Critérios Qualitativos de Desempenho</strong>:
        """, unsafe_allow_html=True)

        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            st.markdown(f"#### 🎯 {rubrica_2026['criterio_1']['titulo']}")
            st.caption(f"**Enunciado:** {rubrica_2026['criterio_1']['enunciado']}")
            st.markdown("""
            * **Não atende:** Não cumpre os requisitos mínimos do nível Atende Parcialmente.
            * **Atende parcialmente:** Utiliza o recurso/ferramenta, mas com função periférica ou meramente expositiva, sem interação direta dos estudantes.
            * **Atende integralmente:** Articula intencionalmente a tecnologia e o objetivo da aula, contribuindo diretamente para o desenvolvimento da habilidade essencial.
            * **Supera:** Cumpre todos os requisitos do Atende Integralmente **E** promove o uso ativo da tecnologia pelos estudantes em situações de produção, investigação, resolução de problemas ou colaboração.
            """)

        with col_c2:
            st.markdown(f"#### 🤝 {rubrica_2026['criterio_2']['titulo']}")
            st.caption(f"**Enunciado:** {rubrica_2026['criterio_2']['enunciado']}")
            st.markdown("""
            * **Não atende:** Não cumpre os requisitos mínimos do nível Atende Parcialmente.
            * **Atende parcialmente:** Mobiliza uso em momentos pontuais; condução excessivamente mecânica e passo a passo, limitando a autonomia discente.
            * **Atende integralmente:** Atua como mediador pedagógico, fornecendo orientações claras e possibilitando a exploração ativa do recurso ao longo da atividade.
            * **Supera:** Cumpre todos os requisitos do Atende Integralmente **E** organiza situações em que os estudantes utilizam a tecnologia com autonomia, protagonismo e tomada de decisão.
            """)

        st.markdown("---")
        st.markdown("### 🔄 Como os Itens de 2025 foram Transpostos para a Rubrica 2026")
        
        mapping_data = [
            {
                "Item Observado em 2025 (Checklist)": "Informa aos estudantes os objetivos de aprendizagem da proposta",
                "Dimensão": "Prática",
                "Critério na Rubrica 2026": "Critério 1: Articulação Intencional",
                "Papel Avaliativo": "Clareza de metas e contrato pedagógico"
            },
            {
                "Item Observado em 2025 (Checklist)": "Explica aos estudantes o porquê da aula voltada para recomposição",
                "Dimensão": "Prática",
                "Critério na Rubrica 2026": "Critério 1: Articulação Intencional",
                "Papel Avaliativo": "Intencionalidade pedagógica e engajamento"
            },
            {
                "Item Observado em 2025 (Checklist)": "Apresenta aos estudantes o recurso/ferramenta educacional digital",
                "Dimensão": "Prática",
                "Critério na Rubrica 2026": "Critério 1: Articulação Intencional",
                "Papel Avaliativo": "Apresentação e integração didática do apoio digital"
            },
            {
                "Item Observado em 2025 (Checklist)": "A aula corresponde à descrição das ações presentes no planejamento",
                "Dimensão": "Prática",
                "Critério na Rubrica 2026": "Critério 1: Articulação Intencional",
                "Papel Avaliativo": "Coerência didática plano-ação"
            },
            {
                "Item Observado em 2025 (Checklist)": "Evidencia-se o domínio do professor na utilização do recurso digital",
                "Dimensão": "Prática",
                "Critério na Rubrica 2026": "Critério 2: Mediação e Uso Ativo",
                "Papel Avaliativo": "Postura mediadora e segurança técnica"
            },
            {
                "Item Observado em 2025 (Checklist)": "Adapta a prática a possíveis imprevistos técnicos",
                "Dimensão": "Prática",
                "Critério na Rubrica 2026": "Critério 2: Mediação e Uso Ativo",
                "Papel Avaliativo": "Resiliência pedagógica e fluência didática"
            },
            {
                "Item Observado em 2025 (Checklist)": "Promove personalização do ensino a partir do trabalho com o recurso",
                "Dimensão": "Prática",
                "Critério na Rubrica 2026": "Critério 2 & Supera",
                "Papel Avaliativo": "Atendimento a diferentes ritmos e percursos discentes"
            },
            {
                "Item Observado em 2025 (Checklist)": "Menções a protagonismo, autonomia, boa prática nos pontos fortes",
                "Dimensão": "Prática / Feedback",
                "Critério na Rubrica 2026": "Nível Supera (Critérios 1 e 2)",
                "Papel Avaliativo": "Evidência explícita de protagonismo, produção e investigação discente"
            }
        ]
        st.dataframe(pd.DataFrame(mapping_data), hide_index=True, use_container_width=True)

    # -------------------------------------------------------------
    # ABA 2: PANORAMA & IMPACTO DA NOVA RÉGUA
    # -------------------------------------------------------------
    with tab2:
        st.markdown("### 📈 Panorama Analítico sob a Ótica da Rubrica 2026")
        
        g1, g2 = st.columns(2)
        with g1:
            lvl_counts = filtered_evals['nivel_atendimento'].value_counts().reset_index()
            lvl_counts.columns = ['Nível de Atendimento', 'Quantidade']
            fig_pie = px.pie(
                lvl_counts,
                names='Nível de Atendimento',
                values='Quantidade',
                color='Nível de Atendimento',
                color_discrete_map=palette_colors,
                hole=0.45,
                title="Distribuição Global dos Níveis de Atendimento (2026)"
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            fig_pie.update_layout(template="plotly_white", legend=dict(orientation="h", y=-0.1))
            st.plotly_chart(fig_pie, use_container_width=True)

        with g2:
            dim_dist = filtered_evals.groupby(['dimensao', 'nivel_atendimento']).size().reset_index(name='Quantidade')
            fig_bar = px.bar(
                dim_dist,
                x='dimensao',
                y='Quantidade',
                color='nivel_atendimento',
                barmode='group',
                color_discrete_map=palette_colors,
                title="Distribuição de Níveis: Planejamento vs. Prática",
                labels={'dimensao': 'Dimensão', 'nivel_atendimento': 'Nível 2026'}
            )
            fig_bar.update_layout(template="plotly_white", legend=dict(orientation="h", y=-0.2))
            st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("#### 🎓 Desempenho por Componente Curricular")
        comp_summary = filtered_evals[filtered_evals['componente'] != 'Não informado'].groupby(
            ['componente', 'nivel_atendimento']
        ).size().reset_index(name='Docentes')
        
        fig_comp = px.bar(
            comp_summary,
            x='componente',
            y='Docentes',
            color='nivel_atendimento',
            barmode='stack',
            color_discrete_map=palette_colors,
            title="Adesão aos Níveis da Rubrica por Disciplina",
            labels={'componente': 'Componente Curricular', 'Docentes': 'Avaliações'}
        )
        fig_comp.update_layout(template="plotly_white", xaxis_tickangle=-45)
        st.plotly_chart(fig_comp, use_container_width=True)

        st.markdown("#### 📋 Matriz Numérica Resumo")
        summary_pivot = pd.crosstab(
            filtered_evals['dimensao'],
            filtered_evals['nivel_atendimento'],
            margins=True,
            margins_name="Total"
        )
        st.dataframe(summary_pivot, use_container_width=True)

    # -------------------------------------------------------------
    # ABA 3: CONSULTA INDIVIDUAL & JUSTIFICATIVAS
    # -------------------------------------------------------------
    with tab3:
        st.markdown("### 🔍 Consulta Individualizada & Justificativas Pedagógicas")
        st.markdown("""
        Selecione qualquer professor abaixo para auditar suas evidências originais de 2025 e 
        verificar a fundamentação pedagógica do seu enquadramento na Rubrica 2026.
        """)

        # Seletor de Cursista
        unique_cursistas = sorted(list(filtered_evals['cursista'].unique()))
        if not unique_cursistas:
            st.warning("Nenhum cursista encontrado com os filtros selecionados.")
        else:
            selected_cursista = st.selectbox("Selecione um Professor:", unique_cursistas)
            
            c_data = filtered_evals[filtered_evals['cursista'] == selected_cursista]
            
            if not c_data.empty:
                comp_prof = c_data.iloc[0]['componente']
                tema_prof = c_data.iloc[0]['tema']
                
                st.markdown(f"#### 👤 {selected_cursista} | {comp_prof} ({tema_prof})")
                
                det1, det2 = st.columns(2)
                
                # Detalhe Planejamento
                c_plan = c_data[c_data['dimensao'] == 'Planejamento']
                with det1:
                    st.markdown("##### 📝 Dimensão Planejamento")
                    if not c_plan.empty:
                        lvl = c_plan.iloc[0]['nivel_atendimento']
                        badge_cls = "badge-integral" if lvl == "Atende integralmente" else ("badge-supera" if lvl == "Supera" else ("badge-parcial" if lvl == "Atende parcialmente" else "badge-nao"))
                        st.markdown(f"**Nível Atribuído:** <span class='{badge_cls}'>{lvl}</span>", unsafe_allow_html=True)
                        st.markdown(f"**Justificativa Pedagógica:**\n> {c_plan.iloc[0]['justificativa_rubrica_2026']}")
                    else:
                        st.info("Dado de planejamento indisponível.")

                # Detalhe Prática
                c_prat = c_data[c_data['dimensao'] == 'Prática']
                with det2:
                    st.markdown("##### 🎬 Dimensão Prática Docente (Rubrica 2026)")
                    if not c_prat.empty:
                        lvl = c_prat.iloc[0]['nivel_atendimento']
                        badge_cls = "badge-integral" if lvl == "Atende integralmente" else ("badge-supera" if lvl == "Supera" else ("badge-parcial" if lvl == "Atende parcialmente" else "badge-nao"))
                        st.markdown(f"**Nível Atribuído:** <span class='{badge_cls}'>{lvl}</span>", unsafe_allow_html=True)
                        st.markdown(f"**Justificativa Pedagógica:**\n> {c_prat.iloc[0]['justificativa_rubrica_2026']}")
                    else:
                        st.info("Dado de prática indisponível.")

                with st.expander("🔎 Ver Anotações do Observador Pedagógico (2025)", expanded=False):
                    st.markdown(f"**Pontos Fortes Registrados:**\n{c_data.iloc[0]['pontos_fortes'] or '_Nenhum ponto forte registrado._'}")
                    st.markdown(f"**Pontos de Melhoria Registrados:**\n{c_data.iloc[0]['pontos_melhoria'] or '_Nenhum ponto de melhoria registrado._'}")
                    if not c_prat.empty and c_prat.iloc[0]['evidencias_checklist_2025']:
                        st.markdown(f"**Itens Cumpridos no Checklist Original:**\n{c_prat.iloc[0]['evidencias_checklist_2025']}")

        st.markdown("---")
        st.markdown("#### 📋 Visão Analítica Completa com Justificativas")
        
        display_evals = filtered_evals[[
            'registro_id', 'cursista', 'componente', 'tema', 'dimensao', 
            'nivel_atendimento', 'justificativa_rubrica_2026'
        ]].rename(columns={
            'registro_id': 'Linha',
            'cursista': 'Professor(a)',
            'componente': 'Disciplina',
            'tema': 'Tema',
            'dimensao': 'Dimensão',
            'nivel_atendimento': 'Nível (Rubrica 2026)',
            'justificativa_rubrica_2026': 'Fundamentação Pedagógica'
        })
        st.dataframe(display_evals, hide_index=True, use_container_width=True)

    # -------------------------------------------------------------
    # ABA 4: DADOS BRUTOS & RASTREABILIDADE
    # -------------------------------------------------------------
    with tab4:
        st.markdown("### 📋 Rastreabilidade dos Registros Originais")
        st.markdown("Acesso completo à planilha com os registros dos docentes e colunas preenchidas pela classificação.")
        
        raw_cols = [
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
        st.dataframe(df_docente[raw_cols].fillna("-"), use_container_width=True)

        # Botão para download do CSV preenchido
        csv_bytes = df_docente.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar Base Docentes Processada (CSV)",
            data=csv_bytes,
            file_name="pdp_docentes_2025_rubrica_2026.csv",
            mime="text/csv"
        )

if __name__ == '__main__':
    main()
