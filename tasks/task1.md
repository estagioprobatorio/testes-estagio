TASK: Preenchimento do CSV e desenvolvimento de painel interativo do PDP 2025

Objetivo geral

Analisar os arquivos disponíveis na pasta docs, preencher os campos pendentes do CSV conforme as regras definidas em rules.md e desenvolver um painel interativo em Python para explorar os dados da modalidade DOCENTE, respeitando os limites estabelecidos pelo documento _DOC_PDP_2025.md.

A implementação deve preservar os dados originais, garantir rastreabilidade das classificações e apresentar visualizações coerentes com as informações efetivamente disponíveis.

TASK 1 — Análise e preenchimento do CSV

1.1. Inspecionar os arquivos

Antes de iniciar, examine:

rules.md: regras obrigatórias de execução;

docs/_DOC_PDP_2025.md: fonte da verdade para os critérios e expectativas;

docs/_taxonomia_bloom.md: referencial para classificação da complexidade cognitiva;

O arquivo CSV existente: fonte dos registros a serem analisados.

Identifique o nome, o caminho, a codificação, o delimitador, os cabeçalhos e os campos pendentes do CSV.

Não presuma os nomes das colunas. Descubra-os por meio da inspeção do arquivo.

1.2. Identificar os campos a preencher

Analise a estrutura do CSV e determine quais colunas estão incompletas e qual é a finalidade de cada uma.

Preencha somente os campos previstos para a tarefa. Preserve os valores já existentes, salvo quando houver uma inconsistência comprovada e uma correção autorizada pelas regras.

Não preencha campos cuja finalidade não possa ser determinada com segurança.

1.3. Classificar os critérios

Para cada registro que corresponda a um critério do PDP 2025:

Localize o tema, a expectativa e o critério correspondente no _DOC_PDP_2025.md.

Determine a complexidade cognitiva predominante, quando houver campo para isso.

Utilize o _taxonomia_bloom.md como referencial interpretativo.

Identifique o nível de atendimento somente quando existirem evidências de desempenho suficientes.

Utilize exclusivamente os valores permitidos para o atendimento:

Não atende

Atende parcialmente

Atende integralmente

Supera

Não crie critérios, expectativas ou evidências que não estejam amparados pelos documentos.

Importante: a classificação cognitiva de um critério não determina automaticamente o nível de atendimento do docente. Se o CSV contiver somente critérios, sem evidências de desempenho, não atribua níveis de atendimento por inferência.

1.4. Preservar os dados

Não exclua registros.

Não altere identificadores.

Não modifique os cabeçalhos sem necessidade comprovada.

Preserve a ordem original dos registros.

Mantenha a codificação e o delimitador compatíveis com o arquivo original.

Não descarte colunas não utilizadas pelo painel.

Crie uma cópia de segurança antes de modificar o CSV.

Não substitua o arquivo original sem verificar a integridade do resultado.

1.5. Validar o resultado

Após o preenchimento:

Verifique a quantidade de linhas antes e depois.

Confirme que não houve perda de registros.

Verifique os valores permitidos nas colunas de classificação.

Identifique campos ainda vazios e explique por que não puderam ser preenchidos.

Verifique a correspondência entre os critérios do CSV e o documento de referência.

Registre eventuais ambiguidades e inconsistências.

Produza um relatório de execução com a quantidade de campos preenchidos, os campos mantidos pendentes e as validações realizadas.