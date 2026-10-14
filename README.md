# Painel Interativo PDP 2025 — Modalidade DOCENTE

Aplicação analítica e painel interativo desenvolvidos em Python (Streamlit) para exploração, acompanhamento e visualização dos dados do Plano de Desenvolvimento Profissional (PDP 2025) da SEED-PR, com foco estrito na modalidade **DOCENTE** (Referência Docente 4 - Ferramentas Educacionais).

---

## 📁 Estrutura do Projeto

```text
IA - teste/
├── docs/
│   ├── _DOC_PDP_2025.md                  # Documento oficial: fonte da verdade para critérios e expectativas
│   ├── _taxonomia_bloom.md               # Guia referencial da Taxonomia de Bloom revisada
│   └── Observações e feedbacks 2024 - Teste Análise IA Checklist.csv  # Base bruta original
├── data/
│   ├── arquivo_original.csv              # Cópia de segurança da base original preservada
│   └── arquivo_preenchido.csv            # Base processada com as classificações de IA
├── src/
│   ├── data_loader.py                    # Carregamento e filtragem estrita na camada de dados
│   ├── data_validation.py                # Módulo de validação de integridade e conformidade
│   ├── process_csv.py                    # Pipeline de análise e preenchimento dos critérios
│   └── dashboard.py                      # Painel interativo Streamlit
├── tests/
│   ├── test_data_filtering.py            # Testes de filtragem da modalidade DOCENTE e casos de borda
│   └── test_data_validation.py           # Testes de integridade, níveis autorizados e reatividade
├── tasks/
│   ├── task1.md                          # Diretrizes da TASK 1 (Análise e preenchimento)
│   ├── task2.md                          # Diretrizes da TASK 2 (Desenvolvimento do painel)
│   ├── task3.md                          # Entregáveis da TASK 3
│   └── task4.md                          # Critérios de aceitação da TASK 4
├── relatorio_preenchimento_e_validacao.md # Relatório técnico completo de preenchimento e validação
├── requirements.txt                      # Dependências do projeto
├── rules.md                              # Regras mandatórias e hierarquia de autoridade
└── README.md                             # Instruções de instalação, execução e uso
```

---

## 📌 Indicação do Caminho do CSV Utilizado

- **Caminho da base processada utilizada pelo painel:**  
  `data/arquivo_preenchido.csv`
- **Caminho da cópia de segurança da base original intacta:**  
  `data/arquivo_original.csv`

---

## 🚀 Instalação e Requisitos

### Pré-requisitos
- Python 3.10 ou superior
- Gerenciador de pacotes `pip`

### Instalação das dependências
No diretório raiz do projeto, instale os pacotes necessários:
```bash
pip install -r requirements.txt
```

---

## ⚙️ Execução

### 1. Reexecutar a Classificação e Preenchimento dos Dados (TASK 1)
Caso queira reprocessar a base de dados original a partir das regras:
```bash
python src/process_csv.py
```
Isso validará as dimensões, preencherá as colunas `Descrição Nível IA...` e gravará o resultado em `data/arquivo_preenchido.csv`.

### 2. Executar a Validação de Integridade
Para verificar a conformidade entre o arquivo original e o arquivo preenchido:
```bash
python src/data_validation.py
```

### 3. Iniciar o Painel Interativo Streamlit (TASK 2)
Para abrir o painel interativo no navegador:
```bash
python -m streamlit run src/dashboard.py
```
O painel será aberto automaticamente em `http://localhost:8501`.

---

## 🧪 Testes Automatizados

A suíte de testes contempla 12 testes unitários que cobrem filtragem de modalidades, tratamento de CSVs vazios ou ausentes, validação de níveis permitidos e atualização dinâmica.

Para executar os testes com `pytest`:
```bash
python -m pytest tests -v
```

Ou usando o módulo padrão `unittest`:
```bash
python -m unittest discover tests -v
```

---

## 📋 Regras de Negócio e Princípios Metodológicos

1. **Hierarquia de Autoridade (`rules.md`):**
   - O documento `_DOC_PDP_2025.md` é a fonte da verdade institucional.
   - O documento `_taxonomia_bloom.md` orienta exclusivamente a compreensão dos processos cognitivos dos critérios, sem constituir escala de avaliação de desempenho docente.
2. **Escopo Restrito à Modalidade DOCENTE:**
   - Apenas registros com a modalidade `Docentes` participam dos cálculos, gráficos e tabelas.
   - A filtragem ocorre na camada de dados (`data_loader.py`) antes de qualquer visualização.
3. **Níveis Oficiais Autorizados:**
   - Exclusivamente: `Não atende`, `Atende parcialmente`, `Atende integralmente` e `Supera`.
   - Registros sem evidências suficientes ou não avaliados permanecem identificados como `Pendente`, sem conversões arbitrárias.
