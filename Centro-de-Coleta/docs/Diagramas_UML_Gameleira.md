# Gameleira – Centro de Coleta
## Diagramas UML e Modelagem da Aplicação

**Projeto:** Gameleira – Centro de Coleta  
**Tecnologias identificadas:** Python, Flask, SQLite, HTML e CSS  
**Finalidade:** apoiar o registro e o acompanhamento de coletas de materiais recicláveis.

> Os diagramas abaixo representam as funcionalidades identificadas na versão atual do sistema. Eles documentam o comportamento existente, sem afirmar funcionalidades que ainda não foram implementadas.

---

## 1. Diagrama de casos de uso

```mermaid
flowchart LR
    U[Usuário do sistema]

    subgraph G[Gameleira – Centro de Coleta]
      UC1([Visualizar painel])
      UC2([Cadastrar coleta])
      UC3([Pesquisar e filtrar coletas])
      UC4([Editar coleta])
      UC5([Atualizar situação da coleta])
      UC6([Atualizar situação do pagamento])
      UC7([Consultar rotas])
      UC8([Consultar histórico])
      UC9([Arquivar coleta])
      UC10([Excluir coleta arquivada permanentemente])
    end

    U --> UC1
    U --> UC2
    U --> UC3
    U --> UC4
    U --> UC5
    U --> UC6
    U --> UC7
    U --> UC8
    U --> UC9
    U --> UC10
```

**Descrição:** o usuário interage com o sistema para registrar e acompanhar coletas, consultar rotas e histórico, atualizar situações e administrar registros arquivados.

---

## 2. Diagrama de classes / modelo de domínio

```mermaid
classDiagram
    class Coleta {
      +int id
      +string catador
      +string material
      +float peso_kg
      +float valor_kg
      +float valor_total
      +string local_coleta
      +string rota
      +string data_coleta
      +string status
      +string pagamento_status
      +string observacoes
      +string data_cadastro
      +int ativo
    }

    class Historico {
      +int id
      +int coleta_id
      +string acao
      +string descricao
      +string data_hora
    }

    Coleta "1" --> "0..*" Historico : possui eventos
```

**Descrição:** a classe `Coleta` representa os registros de materiais recebidos/coletados. A classe `Historico` representa os eventos registrados durante o ciclo de vida de uma coleta.

**Nota técnica:** o relacionamento é utilizado nas consultas da aplicação. Na estrutura física analisada, `historico.coleta_id` não possui restrição `FOREIGN KEY` declarada no SQLite.

---

## 3. Diagrama de sequência – cadastro de coleta

```mermaid
sequenceDiagram
    actor Usuario
    participant Tela as Interface HTML
    participant Flask as Aplicação Flask
    participant Validacao as Validação dos dados
    participant DB as Banco SQLite

    Usuario->>Tela: Preenche formulário de coleta
    Usuario->>Tela: Envia cadastro
    Tela->>Flask: POST /cadastrar
    Flask->>Validacao: dados_formulario(request.form)
    alt Dados inválidos
        Validacao-->>Flask: Retorna erro de validação
        Flask-->>Tela: Exibe mensagem e redireciona
    else Dados válidos
        Validacao-->>Flask: Dados validados e valor total calculado
        Flask->>DB: INSERT na tabela coletas
        DB-->>Flask: Retorna identificador da coleta
        Flask->>DB: INSERT do evento na tabela historico
        Flask->>DB: COMMIT
        Flask-->>Tela: Mensagem de sucesso e redirecionamento
        Tela-->>Usuario: Exibe painel atualizado
    end
```

**Descrição:** o cadastro começa no formulário, passa pela validação no backend e, se os dados forem válidos, grava a coleta e seu evento de cadastro no banco de dados.

---

## 4. Diagrama de atividade – ciclo de cadastro

```mermaid
flowchart TD
    A([Início]) --> B[Usuário abre formulário]
    B --> C[Preenche dados da coleta]
    C --> D[Envia formulário]
    D --> E[Aplicação valida campos]
    E --> F{Dados válidos?}
    F -- Não --> G[Exibe mensagem de erro]
    G --> C
    F -- Sim --> H[Calcula valor total]
    H --> I[Grava coleta no banco]
    I --> J[Registra evento no histórico]
    J --> K[Confirma transação]
    K --> L[Exibe mensagem de sucesso]
    L --> M([Fim])
```

---

## 5. Regras de negócio identificadas

1. O cadastro exige nome do catador, material, local e data da coleta.
2. O material deve pertencer às opções disponibilizadas pelo sistema.
3. O peso deve ser maior que zero.
4. O valor por quilograma não pode ser negativo.
5. O valor total é calculado pela aplicação multiplicando o peso pelo valor por quilograma.
6. A situação da coleta pode ser `Pendente`, `Em andamento` ou `Concluída`.
7. A situação do pagamento pode ser `Pendente` ou `Pago`.
8. O arquivamento altera o campo `ativo` para zero e preserva o registro no banco.
9. A exclusão permanente remove a coleta arquivada e os eventos de histórico associados.

---

## 6. Limites desta modelagem

- Os diagramas foram elaborados a partir das rotas, validações, consultas e tabelas identificadas na versão analisada.
- A interface atual é composta por páginas HTML renderizadas pelo Flask.
- O sistema utiliza SQLite para persistência dos dados.
- A modelagem não representa autenticação ou perfis de acesso, pois essas funcionalidades não foram identificadas na versão analisada.
- A organização MVC ainda é parcial na implementação atual; estes diagramas descrevem o domínio e os fluxos existentes, não uma refatoração já concluída.
