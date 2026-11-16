# Gameleira – Centro de Coleta

## Dicionário de Dados

**SGBD:** SQLite  
**Arquivo do banco:** `gameleira.db`

Este documento descreve as tabelas identificadas no banco de dados da versão analisada do Gameleira – Centro de Coleta.

## 1. Tabela `coletas`

Armazena os registros de materiais coletados, seus valores, localização, situação e informações de pagamento.

| Campo | Tipo | Obrigatório | Descrição |
| --- | --- | ---: | --- |
| `id` | INTEGER | Sim | Identificador único da coleta (chave primária autoincremental). |
| `catador` | TEXT | Sim | Nome do catador responsável pela coleta. |
| `material` | TEXT | Sim | Tipo de material coletado. |
| `peso_kg` | REAL | Sim | Peso do material em quilogramas. Deve ser maior que zero. |
| `valor_kg` | REAL | Sim | Valor atribuído por quilograma. Valor padrão: 0; não pode ser negativo na validação da aplicação. |
| `valor_total` | REAL | Sim | Valor total calculado a partir do peso multiplicado pelo valor por quilograma. |
| `local_coleta` | TEXT | Sim | Local onde o material foi coletado. |
| `rota` | TEXT | Não | Nome ou identificação da rota de coleta. |
| `data_coleta` | TEXT | Sim | Data em que a coleta foi realizada ou registrada para realização. |
| `status` | TEXT | Sim | Situação da coleta: Pendente, Em andamento ou Concluída. Padrão: Pendente. |
| `pagamento_status` | TEXT | Sim | Situação do pagamento: Pendente ou Pago. Padrão: Pendente. |
| `observacoes` | TEXT | Não | Informações complementares sobre a coleta. |
| `data_cadastro` | TEXT | Sim | Data e hora em que o registro foi cadastrado no sistema. |
| `ativo` | INTEGER | Sim | Indica se o registro está ativo (1) ou arquivado (0). Padrão: 1. |

## 2. Tabela `historico`

Armazena os eventos relacionados às coletas, permitindo consultar ações realizadas no sistema.

| Campo | Tipo | Obrigatório | Descrição |
| --- | --- | ---: | --- |
| `id` | INTEGER | Sim | Identificador único do evento (chave primária autoincremental). |
| `coleta_id` | INTEGER | Não | Identificador da coleta relacionada ao evento. |
| `acao` | TEXT | Sim | Tipo de ação realizada, como cadastro, edição, alteração de situação, pagamento ou arquivamento. |
| `descricao` | TEXT | Sim | Descrição textual do evento registrado. |
| `data_hora` | TEXT | Sim | Data e hora em que o evento ocorreu. |

## 3. Relacionamento entre as tabelas

Conceitualmente, uma coleta pode possuir vários registros de histórico. Cada evento de histórico está associado a uma coleta por meio do campo `historico.coleta_id`, que corresponde ao campo `coletas.id`.

**Relacionamento conceitual:** `coletas (1) —— (N) historico`

**Observação técnica:** na versão do banco analisada, `historico.coleta_id` está indexado, mas não foi declarada uma restrição de chave estrangeira (`FOREIGN KEY`) no esquema físico. Portanto, o relacionamento é utilizado pela aplicação, mas não é imposto pelo SQLite por uma chave estrangeira.

## 4. Regras de dados identificadas

- O identificador `id` é a chave primária de cada tabela.
- O peso da coleta deve ser maior que zero.
- O valor por quilograma não pode ser negativo.
- Os campos essenciais da coleta incluem catador, material, local e data.
- O valor total é calculado pela aplicação: `peso_kg × valor_kg`.
- O status da coleta utiliza os valores `Pendente`, `Em andamento` e `Concluída`.
- O pagamento utiliza os valores `Pendente` e `Pago`.
- O arquivamento é lógico: o registro permanece no banco e recebe `ativo = 0`.
- A exclusão permanente remove o registro arquivado e seus eventos de histórico associados.

## 5. Observação sobre o escopo

Este dicionário representa a estrutura encontrada no arquivo `gameleira.db` analisado. Ele não afirma a existência de tabelas ou funcionalidades que não estejam presentes nessa versão do banco.
