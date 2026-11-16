Gameleira – Centro de Coleta
Aplicação web acadêmica desenvolvida para apoiar o registro e o acompanhamento de coletas de materiais recicláveis.
Objetivo
Oferecer uma ferramenta simples para registrar coletas, acompanhar seu andamento, organizar registros por rota e consultar o histórico de alterações.
Funcionalidades implementadas

- Cadastro, consulta, edição e arquivamento de coletas.
- Registro de catador, material, peso, valor por quilo, local, rota, data e observações.
- Cálculo automático do valor total (peso × valor por quilo).
- Acompanhamento da situação da coleta e do pagamento.
- Painel com indicadores e filtros de pesquisa.
- Visualização de coletas agrupadas por rota informada.
- Histórico de alterações.
- Exclusão permanente de registros previamente arquivados.
Tecnologias
- Python
- Flask
- SQLite
- HTML
- CSS
Requisitos
- Python 3.10 ou superior
- pip
Como executar no Windows
Abra o terminal na pasta Centro-de-Coleta (a pasta que contém app.py) e execute:
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
Depois, acesse no navegador:
<http://127.0.0.1:5000>
O arquivo gameleira.db é utilizado para armazenar os dados. Faça uma cópia de segurança antes de substituir ou alterar o banco.
Documentação
Os documentos acadêmicos do projeto estão na pasta docs:
- Dicionario_de_Dados_Gameleira.md – descrição das tabelas e campos do banco.
- Diagramas_UML_Gameleira.md – diagramas de casos de uso, classes, sequência e atividades.
- Relatorio_de_Testes_e_Formulario_Gameleira.md – registro dos testes manuais realizados e formulário para avaliação externa.
- Manual_de_Utilizacao_Gameleira.md – instruções de utilização.
Limitações conhecidas
- As rotas são agrupadas pelo nome informado no cadastro; o sistema não utiliza GPS, mapas ou cálculo automático de trajetos.
- O status de pagamento é apenas um controle informativo; o sistema não realiza transações financeiras.
- A validação com cinco colegas ou profissionais deve ser realizada e documentada com respostas reais.
- A aplicação é um protótipo acadêmico executado localmente e não deve ser considerada pronta para uso em produção.
Observação sobre a arquitetura
A versão documentada utiliza Flask para tratar as rotas e a lógica da aplicação, templates HTML para as telas e SQLite para persistência. A separação completa em camadas MVC é uma melhoria arquitetural prevista, não uma funcionalidade que este README declara como já concluída.
