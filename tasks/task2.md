TASK 2 — Desenvolver painel interativo em Python

2.1. Finalidade

Criar um painel interativo que permita explorar os critérios do PDP 2025 e suas classificações, utilizando exclusivamente os registros cuja modalidade seja DOCENTE.

O documento _DOC_PDP_2025.md ampara a análise dessa modalidade. Portanto, registros de outras modalidades não devem participar dos indicadores, gráficos, tabelas analíticas ou conclusões do painel.

A filtragem deve ocorrer na camada de dados, antes da geração dos indicadores e visualizações, e não apenas na interface.

2.2. Tecnologias

Utilize Python e priorize bibliotecas gratuitas e de código aberto.

Sugestão de stack:

Streamlit: interface web interativa;

Pandas: leitura, limpeza e transformação dos dados;

Plotly Express ou Plotly Graph Objects: gráficos interativos;

Pathlib: gerenciamento de caminhos;

Unittest ou Pytest: testes automatizados.

Antes de instalar dependências, verifique a estrutura existente do projeto e reaproveite as bibliotecas já disponíveis quando forem adequadas.

2.3. Estrutura do painel

Organize a interface em seções.

A. Visão geral

Apresente indicadores calculados exclusivamente a partir dos registros DOCENTE, conforme os campos efetivamente existentes:

Total de registros da modalidade;

Total de critérios distintos, quando identificáveis;

Quantidade de critérios por tema;

Quantidade de critérios por dimensão, como planejamento e prática, se identificável;

Quantidade de registros classificados e pendentes;

Distribuição dos níveis de atendimento, somente se houver evidências de desempenho e classificações válidas.

Não apresente uma quantidade de docentes como se fosse uma contagem de pessoas únicas sem identificar e validar o campo de identificação.

B. Filtros interativos

Disponibilize filtros para:

Tema do PDP;

Dimensão: planejamento ou prática, se disponível;

Categoria da Taxonomia de Bloom, se preenchida;

Nível de atendimento, se houver classificações válidas;

Situação do preenchimento;

Busca textual por critério ou expectativa.

Os filtros devem funcionar em conjunto e atualizar os indicadores, gráficos e tabelas de maneira consistente.

Não invente filtros para campos inexistentes. Adapte a interface ao esquema real do CSV.

C. Análise por tema

Apresente uma visualização que permita comparar a quantidade de critérios associados a cada tema do PDP 2025.

Quando houver dados suficientes, permita detalhar cada tema e consultar:

Título do tema;

Expectativa institucional;

Critério correspondente;

Dimensão de avaliação;

Categoria cognitiva identificada;

Situação do preenchimento.

Os textos institucionais devem preservar o sentido original do documento de referência.

D. Análise da Taxonomia de Bloom

Quando houver classificação cognitiva válida, apresente:

Distribuição dos critérios entre Lembrar, Compreender, Aplicar, Analisar, Avaliar e Criar;

Distribuição por tema;

Comparação entre planejamento e prática, quando aplicável;

Relação entre a categoria cognitiva e o texto do critério.

Utilize gráficos de barras ou outras visualizações adequadas.

Não apresente a distribuição como medida de qualidade docente, desempenho, mérito ou eficácia pedagógica. A Taxonomia de Bloom representa processos cognitivos, não níveis de desempenho profissional.

Não force uma ordenação de qualidade entre categorias nem conclua que mais critérios em Criar, por exemplo, representam uma formação melhor.

E. Análise dos níveis de atendimento

Esta seção só deve ser habilitada quando houver evidências de desempenho e classificações válidas.

Apresente, conforme os dados disponíveis:

Quantidade e proporção por nível de atendimento;

Distribuição por tema;

Distribuição por dimensão;

Comparações entre critérios, respeitando o contexto e a natureza de cada um.

Utilize exclusivamente os quatro rótulos oficiais:

Não atende

Atende parcialmente

Atende integralmente

Supera

Não transforme campos vazios em Não atende. Registros pendentes devem permanecer identificados como pendentes.

Não produza médias numéricas arbitrárias dos níveis de atendimento, nem índices compostos sem uma metodologia institucionalmente autorizada.

F. Tabela detalhada

Crie uma tabela interativa com os registros filtrados, permitindo:

Buscar texto;

Ordenar colunas;

Filtrar registros;

Consultar as classificações;

Visualizar critérios e expectativas;

Identificar campos pendentes.

A tabela deve exibir apenas as colunas úteis para análise, sem eliminar os demais campos do CSV original.

Inclua, quando possível, a identificação do registro para facilitar a rastreabilidade até a fonte.

2.4. Regras de filtragem da modalidade

Localize no CSV a coluna que identifica a modalidade e determine o valor correspondente a DOCENTE.

Implemente a filtragem de forma explícita e validada.

Requisitos obrigatórios:

Somente registros da modalidade DOCENTE podem compor o conjunto analítico.

Registros de outras modalidades devem ser excluídos antes dos cálculos.

Não misture modalidades em gráficos, tabelas de indicadores ou comparações.

Se a coluna de modalidade estiver ausente ou não puder ser identificada, interrompa a análise e apresente um erro explicativo.

Se não houver registros DOCENTE, mostre uma mensagem informativa e não gere indicadores artificiais.

Registre no painel que a análise está restrita à modalidade DOCENTE.

2.5. Interface e experiência de uso

Desenvolva uma interface organizada, responsiva e de leitura fácil.

Utilize:

Títulos objetivos;

Indicadores com definições claras;

Gráficos com legendas e eixos identificados;

Tabelas com cabeçalhos legíveis;

Mensagens para dados ausentes ou filtros sem resultados;

Separação visual entre critérios, classificação cognitiva e atendimento.

Não utilize gráficos meramente decorativos. Toda visualização deve responder a uma pergunta analítica clara.

Não exiba percentuais sem informar a base de cálculo ou sem deixar explícito qual conjunto de registros foi considerado.

2.6. Atualização dos dados

O painel deve ler o CSV como fonte de dados, evitando manter cópias manuais dos registros no código.

Quando o CSV for atualizado, o painel deverá refletir os novos dados após uma nova leitura ou atualização da aplicação.

Não modifique o CSV automaticamente durante a execução do painel. A atualização e a classificação dos dados devem ocorrer na TASK 1, separadamente da visualização.

2.7. Organização do código

Adapte a organização à estrutura já existente. Se não houver uma estrutura definida, utilize como referência:

projeto/
├── docs/
│   ├── _DOC_PDP_2025.md
│   └── _taxonomia_bloom.md
├── data/
│   ├── arquivo_original.csv
│   └── arquivo_preenchido.csv
├── src/
│   ├── data_loader.py
│   ├── data_validation.py
│   └── dashboard.py
├── tests/
│   ├── test_data_filtering.py
│   └── test_data_validation.py
├── requirements.txt
├── README.md
└── rules.md

Os nomes acima são ilustrativos. Antes de criar pastas ou mover arquivos, inspecione o repositório e preserve a organização já estabelecida.

Não duplique documentos ou bases sem necessidade. Os nomes definitivos dos arquivos de dados devem refletir os arquivos realmente existentes.

2.8. Testes obrigatórios

Implemente testes para verificar:

Leitura correta do CSV;

Identificação da coluna de modalidade;

Exclusão de registros que não sejam DOCENTE;

Ausência de mistura de modalidades nos indicadores;

Comportamento com CSV vazio;

Comportamento quando não existem registros DOCENTE;

Tratamento de campos vazios;

Validação dos níveis de atendimento;

Atualização dos resultados após alteração da base;

Consistência entre os registros filtrados e os valores exibidos nos gráficos.

Os testes devem utilizar dados de exemplo controlados e não alterar a base real.