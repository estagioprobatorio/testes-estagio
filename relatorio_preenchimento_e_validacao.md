# Relatório de Preenchimento e Validação do PDP 2025 (TASK 1)

**Data de Execução:** 14/10/2026  
**Documentos de Referência:**
- `rules.md` (Regras de análise, hierarquia e classificação)
- `docs/_DOC_PDP_2025.md` (Fonte da verdade: temas, expectativas e critérios institucionais)
- `docs/_taxonomia_bloom.md` (Referencial de complexidade cognitiva)
- `data/arquivo_original.csv` (Cópia de segurança da base original)
- `data/arquivo_preenchido.csv` (Base resultante processada e validada)

---

## 1. Inventário e Estrutura dos Arquivos

1. **Arquivo Fonte:** `docs/Observações e feedbacks 2024 - Teste Análise IA Checklist.csv`
2. **Codificação:** UTF-8
3. **Delimitador:** Vírgula (`,`)
4. **Dimensões Originais:** 1.135 registros e 152 colunas.
5. **Modalidades Identificadas no Formulário Unificado:**
   - O formulário Google Forms abrigava perguntas condicionais para múltiplos segmentos: 1º e 2º Anos; Docentes, Equipe Gestora (EQG) e Técnicos (TEC); Temáticas 4, 5, 6 e 7.
   - Na extração fornecida, 1.132 registros pertencem à modalidade **Docentes** (2º Ano), concentrados na **Temática 5 - Referência Docente 4 - Ferramentas Educacionais**.
   - Três registros (linhas 685, 687 e 688) resultaram de quebras de linha/aspas não escapadas no formulário de origem, contendo dados nulos ou fragmentos sem atribuição de modalidade.

---

## 2. Identificação e Finalidade dos Campos a Preencher

Foram identificadas 4 colunas pendentes criadas especificamente para receber a classificação do nível de atendimento da IA:

| Índice | Nome Original da Coluna | Finalidade Analítica | Registros Preenchidos | Registros Pendentes / Vazios |
| :---: | :--- | :--- | :---: | :---: |
| **82** | `Descrição Nível IA Planejamento T1` | Nível de atendimento no **Planejamento do Tema I** | 865 | 270 |
| **84** | `Descrição Nível IA Planejamento T1.1` | Nível de atendimento na **Prática do Tema I** | 865 | 270 |
| **78** | `Descrição Nível IA Planejamento T2` | Nível de atendimento no **Planejamento do Tema II** | 265 | 870 |
| **80** | `Descrição Nível IA Planejamento T2.1` | Nível de atendimento na **Prática do Tema II** | 265 | 870 |

*Nota explicativa:*
- Os 270 registros pendentes no Tema I correspondem aos cursistas que optaram pelo Tema II (265 registros), aos dois docentes sem tema registrado por fragmentação de linha (linhas 684 e 686) e aos 3 registros não-docentes/vazios (linhas 685, 687 e 688).
- De forma análoga, os 870 registros pendentes no Tema II correspondem aos cursistas do Tema I (865 registros) mais os 5 registros pendentes.
- Nenhuma coluna fora do escopo ou sem finalidade comprovada foi preenchida, respeitando o princípio de conservação de dados.

---

## 3. Fundamentação e Critérios de Classificação

Conforme `rules.md` (item 5) e a calibração pedagógica da **Sugestão 1 (Faixas Percentuais Gradativas)**, foram utilizados **exclusivamente os quatro valores oficiais**:

1. **Não atende (0% a 25% dos critérios):**
   - Atribuído quando há cumprimento de no máximo 1 critério ($0$ ou $1$ critério cumprido de $7$ ou $6$), ou seleção isolada de `"O cursista não desenvolveu nenhum dos critérios relacionados à expectativa"`, ou comprovação em feedback de ausência de planejamento/vídeo sem prática docente (ex.: linhas 638 e 1128).
2. **Atende parcialmente (26% a 70% dos critérios):**
   - Atribuído quando foram atendidos de $2$ a $4$ critérios exigidos da respectiva dimensão, demonstrando atendimento preliminar ou intermediário, mas ainda com lacunas substanciais em relação ao conjunto da proposta.
3. **Atende integralmente (71% a 99% ou 100% regular):**
   - Atribuído quando há cumprimento consistente da grande maioria ou da totalidade dos critérios ($5$ ou $6$ critérios cumpridos de $7$; ou $5$ critérios de $6$; ou $100\%$ sem evidência adicional de superação). Reconhece que contingências da aula (como ausência de imprevisto técnico a ser contornado) não anulam a qualidade do trabalho.
4. **Supera (100% + impacto qualitativo):**
   - Atribuído quando, além de atender a 100% dos critérios exigidos na dimensão, o registro possui evidência explícita e documentada no parecer do formador (campos de pontos fortes e reflexões) atestando superação de expectativas, indicação formal como "boa prática pedagógica", caráter inovador ou replicabilidade destacada.

---

## 4. Distribuição das Classificações Realizadas (Calibração Sugestão 1)

### Tema I (Recursos Educacionais Digitais — 865 avaliações)
- **Planejamento (T1):**
  - *Atende integralmente:* 851 (98,38%)
  - *Atende parcialmente:* 11 (1,27%)
  - *Supera:* 2 (0,23%)
  - *Não atende:* 1 (0,12%)
- **Prática Docente (T1):**
  - *Atende integralmente:* 833 (96,30%)
  - *Atende parcialmente:* 28 (3,24%)
  - *Supera:* 2 (0,23%)
  - *Não atende:* 2 (0,23%)

### Tema II (Ferramentas Educacionais — 265 avaliações)
- **Planejamento (T2):**
  - *Atende integralmente:* 250 (94,34%)
  - *Atende parcialmente:* 13 (4,91%)
  - *Supera:* 2 (0,75%)
  - *Não atende:* 0 (0,00%)
- **Prática Docente (T2):**
  - *Atende integralmente:* 251 (94,72%)
  - *Atende parcialmente:* 12 (4,53%)
  - *Supera:* 2 (0,75%)
  - *Não atende:* 0 (0,00%)

---

## 5. Mapeamento da Complexidade Cognitiva (Taxonomia de Bloom)

A Taxonomia de Bloom revisada (`_taxonomia_bloom.md`) foi aplicada para mapear o processo cognitivo de cada critério institucional de `_DOC_PDP_2025.md`:

| Tema | Dimensão | Critério | Categoria de Bloom | Processo Cognitivo Predominante |
| :--- | :--- | :--- | :--- | :--- |
| **Tema I** | Planejamento | Descreve o objetivo da proposta pedagógica | **Compreender** | Explicar e estruturar o objetivo didático formativo |
| **Tema I** | Planejamento | Apresenta recurso digital oferecido pela secretaria | **Lembrar** | Identificar e selecionar recurso oficial |
| **Tema I** | Planejamento | Recurso selecionado do componente (caso tenha) | **Compreender** | Relacionar recurso ao componente curricular |
| **Tema I** | Planejamento | Apresenta habilidade prioritária do componente | **Analisar** | Diagnosticar e selecionar habilidade prioritária |
| **Tema I** | Planejamento | Explora recurso relacionando à recomposição | **Analisar** | Articular recursos digitais a lacunas de aprendizagem |
| **Tema I** | Planejamento | Descreve ações respondendo às questões do plano | **Criar** | Planejar sequência didática coerente e articulada |
| **Tema I** | Planejamento | Descreve resultados esperados com a implementação | **Avaliar** | Prever e avaliar indicadores de sucesso pedagógico |
| **Tema I** | Prática | Informa aos estudantes os objetivos de aprendizagem | **Compreender** | Compartilhar intenção didática com a turma |
| **Tema I** | Prática | Explica aos estudantes o porquê da recomposição | **Compreender** | Contextualizar e justificar o sentido da aprendizagem |
| **Tema I** | Prática | Apresenta o recurso digital a ser utilizado | **Compreender** | Demonstrar o funcionamento da ferramenta aos alunos |
| **Tema I** | Prática | Aula/atividade corresponde às ações planejadas | **Aplicar** | Implementar e executar o plano pedagógico previsto |
| **Tema I** | Prática | Evidencia domínio na utilização do recurso digital | **Aplicar** | Operar recursos com destreza prática |
| **Tema I** | Prática | Adapta a prática a possíveis imprevistos técnicos | **Avaliar** | Julgar situações emergentes e tomar decisões imediatas |
| **Tema I** | Prática | Promove personalização do ensino pelo recurso | **Criar** | Modular e estruturar percursos diferenciados |
| **Tema II** | Planejamento | Descreve o objetivo da proposta pedagógica | **Compreender** | Explicar e estruturar o objetivo didático |
| **Tema II** | Planejamento | Apresenta mais de uma ferramenta da secretaria | **Compreender** | Articular e selecionar ferramentas complementares |
| **Tema II** | Planejamento | Apresenta habilidade prioritária do componente | **Analisar** | Diagnosticar e selecionar habilidade de recomposição |
| **Tema II** | Planejamento | Explora ferramentas relacionando à recomposição | **Analisar** | Estabelecer conexões entre ferramentas e aprendizagem |
| **Tema II** | Planejamento | Descreve ações respondendo às questões do plano | **Criar** | Elaborar plano pedagógico detalhado e integrado |
| **Tema II** | Planejamento | Descreve resultados esperados com a implementação | **Avaliar** | Formular expectativas avaliativas fundamentadas |
| **Tema II** | Prática | Informa aos estudantes os objetivos de aprendizagem | **Compreender** | Comunicar e alinhar objetivos com a turma |
| **Tema II** | Prática | Explica aos estudantes o porquê da recomposição | **Compreender** | Explicar a relevância da recomposição |
| **Tema II** | Prática | Apresenta a(s) ferramenta(s) aos estudantes | **Compreender** | Ilustrar e orientar o uso das ferramentas |
| **Tema II** | Prática | Aula/atividade corresponde ao planejamento | **Aplicar** | Executar a proposta em conformidade com o plano |
| **Tema II** | Prática | Evidencia domínio na utilização da(s) ferramenta(s)| **Aplicar** | Demonstrar domínio técnico e operacional em sala |
| **Tema II** | Prática | Adapta a prática a possíveis imprevistos técnicos | **Avaliar** | Julgar criticamente e contornar imprevistos |
| **Tema II** | Prática | Promove personalização do ensino pelas ferramentas| **Criar** | Criar estratégias de diferenciação pedagógica |

---

## 6. Tratamento de Ambiguidades e Casos Especiais

1. **Seleções Contraditórias ("Marcar Tudo"):**
   - Foram identificados registros em que o formador marcou todos os critérios positivos e concomitantemente a caixa `"O cursista não desenvolveu nenhum dos critérios..."`.
   - O cruzamento com os campos textuais de *Pontos Fortes* e *Pontos de Melhoria* (ex.: linha 54: *"O Planejamento e a prática atendem todos os critérios solicitados"*) comprovou que se tratava de equívoco operacional de preenchimento da caixa inferior no Google Forms. Esses registros foram classificados com base no atendimento consistente comprovado às evidências.
2. **Critério Condicional no Tema I (`"caso tenha"`):**
   - No Tema I, o critério de componente é condicional, pois nem todas as disciplinas possuem plataforma própria da SEED. Nos casos em que todos os demais 6 critérios foram cumpridos, o registro foi classificado como *Atende integralmente*.
3. **Casos Incompletos / Sem Evidência:**
   - Docentes sem indicação de tema e sem checklist (linhas 684 e 686) permaneceram com campos de nível **vazios/pendentes**, conforme determinam os itens 5.5 e 10 das `rules.md`.

---

## 7. Resultados da Validação Automatizada

O módulo `src/data_validation.py` verificou:
- **Total de linhas:** 1.135 no original / 1.135 no preenchido (Sem perdas).
- **Total de colunas:** 152 no original / 152 no preenchido (Identidade total dos cabeçalhos).
- **Valores nas colunas de nível:** 100% aderentes ao vocabulário permitido.
- **Colunas externas:** 100% inalteradas em relação ao original.
- **Status da Validação:** **APROVADO (is_valid = True)**.
