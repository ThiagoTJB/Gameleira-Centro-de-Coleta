# Gameleira – Centro de Coleta

Aplicação web acadêmica para apoiar o registro e o acompanhamento de coletas de materiais recicláveis, com foco nas necessidades descritas na proposta do projeto.

## Funcionalidades desta versão
- Cadastro, consulta, edição e arquivamento de coletas.
- Registro de catador, material, peso, valor por quilo, local, rota, data e observações.
- Cálculo automático do valor da produção (peso × valor/kg).
- Acompanhamento da situação da coleta e do pagamento.
- Painel com indicadores e filtros de pesquisa.
- Visão agrupada das rotas informadas nos registros.
- Histórico de alterações e opção de exclusão permanente de registros arquivados.
- Interface responsiva, navegação por teclado, rótulos de formulário e link para pular ao conteúdo.

## Requisitos
- Python 3.10 ou superior
- pip

## Como executar no Windows
1. Extraia o arquivo ZIP.
2. Abra o terminal dentro da pasta do projeto.
3. Crie um ambiente virtual (opcional, mas recomendado):
   `python -m venv venv`
4. Ative-o: `venv\\Scripts\\activate`
5. Instale as dependências: `pip install -r requirements.txt`
6. Inicie: `python app.py`
7. Abra `http://127.0.0.1:5000` no navegador.

O banco `gameleira.db` é criado automaticamente na pasta do projeto. Faça cópias de segurança desse arquivo regularmente.

## Observações acadêmicas
Esta é uma versão funcional inicial para prototipação e testes. A organização de rotas é feita por agrupamento do nome informado no cadastro; não há mapa, GPS ou cálculo automático de percurso. A acessibilidade foi contemplada inicialmente com estrutura semântica, rótulos, foco visível e navegação por teclado, mas ainda precisa de avaliação com usuários, especialmente pessoas com deficiência visual. O controle de pagamento registra apenas o status e o valor calculado, não realiza transações financeiras.

Antes de apresentar como validado, realize testes reais com usuários e registre os resultados, problemas encontrados e melhorias aplicadas.
