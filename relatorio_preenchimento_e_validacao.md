# Relatório de Preenchimento, Validação e Adequação à Rubrica PDP 2026

**Data de Atualização:** 15/10/2026  
**Documentos de Referência:**
- `rules.md` (Diretrizes de análise, hierarquia e integridade de dados)
- `docs/_DOC_PDP_2025.md` (Base histórica: temas, expectativas e critérios originais de 2025)
- `docs/PDP_DOCENTES_Referência 04_2026.md` (Referencial pedagógico de rubricas analíticas para 2026)
- `data/arquivo_original.csv` (Cópia de segurança da base original)
- `data/arquivo_preenchido.csv` (Base resultante processada, classificada e validada)

---

## 1. Inventário e Estrutura dos Arquivos

1. **Arquivo Fonte:** `docs/Observações e feedbacks 2024 - Teste Análise IA Checklist.csv`
2. **Codificação:** UTF-8
3. **Delimitador:** Vírgula (`,`)
4. **Dimensões Originais:** 1.135 registros e 152 colunas.
5. **Modalidade Analisada:**
   - O formulário Google Forms abrigava múltiplos segmentos (1º e 2º Anos; Docentes, Equipe Gestora e Técnicos; Temáticas 4 a 7).
   - Na base fornecida, 1.130 registros pertencem à modalidade **Docentes** (2º Ano), concentrados na **Temática 5 - Referência Docente 4 - Ferramentas Educacionais**.
   - Três registros (linhas 685, 687 e 688) resultaram de quebras de linha/aspas não escapadas no formulário de origem, contendo dados nulos ou fragmentos sem atribuição de modalidade.

---

## 2. Identificação e Finalidade dos Campos Preenchidos

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
- Nenhuma coluna externa ou fora do escopo foi modificada, respeitando o princípio de conservação e integridade dos dados.

---

## 3. Adequação Metodológica: Transição do Checklist (2025) para a Rubrica Analítica (2026)

Em atendimento às solicitações pedagógicas da gestão:
1. **Remoção da Taxonomia de Bloom como Critério Avaliativo:** A taxonomia de Bloom foi desvinculada como régua de pontuação, evitando que o docente fosse penalizado por executar verbos operacionais essenciais (ex.: lembrar, compreender).
2. **Equiparação ao PDP 2026 (`PDP_DOCENTES_Referência 04_2026.md`):** O modelo somatório do checklist de 2025 foi traduzido para a arquitetura qualitativa da Rubrica de 2026, organizada em torno de dois grandes eixos para a observação da prática:
   - **Critério 1: Articulação Intencional** entre a habilidade essencial, os objetivos de aprendizagem e o recurso/ferramenta educacional digital.
   - **Critério 2: Mediação Pedagógica e Uso Ativo** da tecnologia pelos estudantes como apoio ao desenvolvimento da habilidade.

### Matriz de Transposição e Regras de Nível

Foram rigorosamente mantidos os quatro rótulos oficiais:

* **Não atende:**
  - *Fundamentação:* Não cumpre os requisitos mínimos do nível Parcial ($\le 1$ item assinalado no checklist original de 2025; ou comprovação em parecer de ausência de planejamento/vídeo sem aula).
* **Atende parcialmente:**
  - *Fundamentação:* O docente mobiliza a tecnologia, porém sua função pedagógica é periférica ou meramente expositiva ($C1 < 2$), ou a condução é excessivamente mecânica e passo a passo, sem autonomia discente e sem evidência de mediação ativa ($C2 = 0$).
* **Atende integralmente:**
  - *Fundamentação:* Articulação intencional consistente entre a habilidade e os recursos/ferramentas ($C1 \ge 2$) aliada à mediação efetiva na qual os estudantes exploram a tecnologia de forma integrada ao longo da atividade ($C2 \ge 1$).
* **Supera:**
  - *Fundamentação:* Cumpre integralmente todos os requisitos estruturantes de $C1$ e $C2$ E promove o uso ativo da tecnologia pelos estudantes em situações de produção, investigação, resolução de problemas ou autonomia/personalização, com parecer formal do observador atestando superação de expectativas ou indicação como boa prática.

---

## 4. Distribuição das Classificações Realizadas (Lente PDP 2026)

### Tema I (Recursos Educacionais Digitais — 865 docentes)
- **Planejamento (T1):**
  - *Atende integralmente:* 844 (97,57%)
  - *Atende parcialmente:* 19 (2,20%)
  - *Não atende:* 2 (0,23%)
  - *Supera:* 0 (0,00%)
- **Prática Docente (T1):**
  - *Atende integralmente:* 790 (91,33%)
  - *Supera (Protagonismo/Autonomia):* 60 (6,94%)
  - *Atende parcialmente:* 13 (1,50%)
  - *Não atende:* 2 (0,23%)

### Tema II (Ferramentas Educacionais — 265 docentes)
- **Planejamento (T2):**
  - *Atende integralmente:* 254 (95,85%)
  - *Atende parcialmente:* 11 (4,15%)
  - *Não atende:* 0 (0,00%)
  - *Supera:* 0 (0,00%)
- **Prática Docente (T2):**
  - *Atende integralmente:* 225 (84,91%)
  - *Supera (Protagonismo/Autonomia):* 32 (12,08%)
  - *Atende parcialmente:* 8 (3,02%)
  - *Não atende:* 0 (0,00%)

---

## 5. Comparativo: Impacto da Transição da Régua

| Dimensão da Avaliação | Modelo Checklist Original (2025) | Projeção na Rubrica Analítica (2026) | Ganho Pedagógico da Transição |
| :--- | :--- | :--- | :--- |
| **Atende Parcialmente** | Concentrava docentes que deixaram de cumprir um único detalhe formal periférico (ex.: ausência de imprevisto técnico). | Reduzido para casos com real uso periférico/mecânico da tecnologia ($\approx 1,5\%$ a $3\%$). | Elimina penalizações artificiais e foca o apoio formativo em quem realmente necessita. |
| **Atende Integralmente** | Exigia pontuação quase perfeita em todos os itens. | Reconhece a articulação intencional consistente e mediação ativa ($\approx 85\%$ a $91\%$). | Valida a prática real de sala de aula e a integração didática dos recursos. |
| **Supera** | Quase nulo ($< 0,5\%$) por travas aritméticas estritas. | Valoriza o protagonismo, autonomia discente e práticas recomendadas ($6,9\%$ a $12\%$). | Dá visibilidade a professores inovadores que estimulam produção e autoria discente. |

---

## 6. Resultados da Validação Automatizada de Dados

O módulo `src/data_validation.py` e a suíte `pytest` verificaram:
- **Total de linhas:** 1.135 no original / 1.135 no preenchido (Preservação estrita).
- **Total de colunas:** 152 no original / 152 no preenchido (Sem alterações de cabeçalho).
- **Vocabulário de Níveis:** 100% aderente aos quatro valores autorizados (`Não atende`, `Atende parcialmente`, `Atende integralmente`, `Supera`).
- **Colunas externas:** 100% inalteradas em relação ao original.
- **Suíte de Testes Automatizados:** 12/12 testes aprovados com sucesso.
- **Status da Validação:** **APROVADO (is_valid = True)**.
