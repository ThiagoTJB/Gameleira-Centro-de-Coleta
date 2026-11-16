# Gameleira – Centro de Coleta
## Relatório de Testes Funcionais – Versão de Desenvolvimento

**Projeto:** Gameleira – Centro de Coleta  
**Tecnologias:** Python, Flask, SQLite, HTML e CSS  
**Tipo de teste registrado:** teste funcional manual  
**Ambiente informado:** Windows 10, execução local pelo Flask

## 1. Objetivo

Registrar os testes manuais realizados durante o desenvolvimento para verificar os principais fluxos do sistema: cadastro, edição, atualização de situação, pagamentos, histórico, rotas, pesquisa, validação e arquivamento de coletas.

## 2. Resultados dos testes realizados

Os resultados abaixo foram relatados pelo desenvolvedor durante a execução manual do sistema. Não representam testes automatizados nem avaliação independente de usuários externos.

| ID | Funcionalidade | Procedimento realizado | Resultado informado |
|---|---|---|---|
| T01 | Cadastro | Cadastrar coleta de teste com catador, material, peso, valor e localização. | Aprovado |
| T02 | Cálculo do valor | Conferir o cálculo do peso multiplicado pelo valor por kg. Exemplo: 10 kg × R$ 2,00 = R$ 20,00. | Aprovado |
| T03 | Atualização de situação | Alterar a situação da coleta para Concluída e conferir os indicadores. | Aprovado |
| T04 | Atualização de pagamento | Alterar pagamento para Pago e conferir o painel. | Aprovado |
| T05 | Histórico | Consultar os eventos de cadastro e alterações. | Aprovado |
| T06 | Edição | Alterar dados da coleta e conferir a atualização do valor total. | Aprovado |
| T07 | Arquivamento | Arquivar uma coleta e verificar sua exibição na área de arquivadas. | Aprovado |
| T08 | Rotas | Cadastrar coleta com rota e conferir a listagem agrupada por rota. | Aprovado |
| T09 | Pesquisa e filtros | Pesquisar registros e aplicar/remover filtros. | Aprovado |
| T10 | Validação de campos | Tentar enviar cadastro sem catador, com peso negativo e com peso igual a zero. | Aprovado: entradas inválidas bloqueadas |
| T11 | Navegação por teclado | Navegar pelos controles usando Tab e Enter. | Verificação manual inicial informada como satisfatória |
| T12 | Layout responsivo | Visualizar o layout em simulação de dispositivo móvel. | Verificação visual inicial informada como satisfatória |
| T13 | Exclusão permanente | Arquivar e excluir permanentemente um registro de teste, conferindo a remoção. | Aprovado |

## 3. Dados de teste utilizados

Foram utilizados registros fictícios para testar os fluxos, incluindo:

- João da Silva – Papel – 10 kg – R$ 2,00/kg – R$ 20,00 – Rota Centro.
- Maria Oliveira – Plástico – 5 kg – R$ 3,00/kg – Rota Centro.

O registro de João foi arquivado durante os testes. O registro de Maria foi utilizado para verificar a exibição da rota. Esses dados são exemplos de teste, não dados de produção.

## 4. Limitações e próximos testes

- Os testes descritos foram manuais e realizados pelo desenvolvedor.
- Não foi registrada execução de suíte automatizada.
- A navegação por teclado e a responsividade receberam apenas verificação inicial; não equivalem a uma auditoria completa de acessibilidade ou compatibilidade.
- A validação com cinco colegas de curso ou profissionais da área ainda precisa ser realizada e documentada.
- Sugestões, problemas e correções de avaliadores externos devem ser acrescentados após a coleta real das respostas.

## 5. Conclusão

Nos testes manuais informados, os principais fluxos operacionais do Gameleira apresentaram o comportamento esperado. A aplicação demonstrou capacidade de cadastrar, editar, consultar e acompanhar coletas, além de registrar eventos no histórico e validar campos obrigatórios e valores numéricos.

A validação externa com cinco pessoas permanece como atividade pendente. Portanto, este relatório registra os testes internos já realizados e não declara concluída a validação com usuários.

---

# Formulário de avaliação por usuário

**Instrução:** compartilhar este formulário com cinco colegas de curso ou profissionais da área. Cada pessoa deve testar o sistema e preencher uma resposta individual. Não preencher respostas em nome dos participantes.

## Identificação do avaliador

- Nome (opcional): __________________________________
- Perfil: ( ) Estudante  ( ) Profissional de TI  ( ) Outro
- Data do teste: ____/____/________

## Tarefas para testar

Marque o resultado observado em cada tarefa:

| Tarefa | Conseguiu | Não conseguiu | Não testou |
|---|:---:|:---:|:---:|
| Acessar o painel principal | ( ) | ( ) | ( ) |
| Cadastrar uma coleta | ( ) | ( ) | ( ) |
| Pesquisar uma coleta | ( ) | ( ) | ( ) |
| Editar uma coleta | ( ) | ( ) | ( ) |
| Atualizar situação e pagamento | ( ) | ( ) | ( ) |
| Consultar rotas | ( ) | ( ) | ( ) |
| Consultar histórico | ( ) | ( ) | ( ) |
| Arquivar uma coleta de teste | ( ) | ( ) | ( ) |

## Avaliação e sugestões

1. O sistema foi fácil de entender e utilizar?
   __________________________________________________

2. Encontrou algum erro? Descreva o procedimento e o que aconteceu.
   __________________________________________________

3. O que poderia ser melhorado?
   __________________________________________________

4. Teve dificuldade para encontrar alguma função?
   __________________________________________________

5. Anexe uma captura de tela caso tenha encontrado erro (quando possível).

**Observação:** após receber as cinco avaliações, consolidar os resultados, registrar sugestões relevantes e descrever quais melhorias foram incorporadas ou justificadamente não foram implementadas.
