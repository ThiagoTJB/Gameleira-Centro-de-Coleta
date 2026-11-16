# Gameleira – Centro de Coleta
## Manual de instalação e utilização

**Projeto acadêmico – PIT II**  
**Tecnologias:** Python 3.10+, Flask 3.1.3, SQLite, HTML e CSS  
**Ambiente de referência:** Windows 10

### 1. Apresentação
O Gameleira – Centro de Coleta é uma aplicação web acadêmica para registrar e acompanhar coletas de materiais recicláveis. O sistema permite controlar informações sobre catadores, materiais, peso, valores, locais, rotas, situação das coletas e pagamentos.

### 2. Requisitos
- Computador com Windows 10 e Python 3.10 ou superior instalado.
- `pip` disponível para instalar a dependência Flask.
- Navegador web atualizado.

### 3. Instalação e execução
1. Extraia o projeto e abra no Visual Studio Code a pasta **`Centro-de-Coleta`**, onde está o arquivo `app.py`.
2. Abra o terminal integrado nessa pasta.
3. Se necessário, crie o ambiente virtual com `python -m venv venv`.
4. Ative o ambiente virtual no PowerShell com `./venv/Scripts/Activate.ps1` (se o ambiente já estiver ativo, pule esta etapa).
5. Instale as dependências com `python -m pip install -r requirements.txt`.
6. Execute `python app.py`.
7. Acesse **http://127.0.0.1:5000** no navegador.

> Caso o terminal informe que não encontrou `app.py`, confirme se está na pasta `Centro-de-Coleta`, e não na pasta acima dela. O banco `gameleira.db` fica na mesma pasta do `app.py` e é criado automaticamente caso não exista.

### 4. Painel principal
A página inicial apresenta indicadores das coletas cadastradas, como quantidades por situação, peso concluído, valor das coletas concluídas e valores pendentes de pagamento. Nela também é possível consultar os registros ativos e usar pesquisa e filtros.

### 5. Cadastrar uma coleta
1. Na página inicial, localize o formulário de cadastro.
2. Informe o **catador**, o **material**, o **peso em kg**, o **valor por kg**, o **local** e a **data da coleta**.
3. Preencha, quando necessário, **rota** e **observações**.
4. Selecione a situação da coleta e a situação do pagamento.
5. Envie o formulário para salvar o registro.

O valor total é calculado pelo sistema multiplicando o peso pelo valor por quilograma. O peso precisa ser maior que zero e o valor por quilograma não pode ser negativo. Dados inválidos geram mensagem de erro.

### 6. Consultar, pesquisar e filtrar
No painel principal, use a pesquisa para localizar registros por catador, material, local ou rota. Use o filtro de situação para restringir a listagem e a opção de limpar para retornar à visualização sem filtros.

### 7. Editar uma coleta
Na lista de coletas, abra a opção de edição do registro desejado. Altere os campos necessários e salve. A aplicação atualiza o registro e adiciona um evento ao histórico.

### 8. Atualizar situação e pagamento
Na lista de coletas, utilize os controles correspondentes para mudar a situação para **Pendente**, **Em andamento** ou **Concluída**, e o pagamento para **Pendente** ou **Pago**. As mudanças são registradas no histórico.

> O sistema apenas registra a situação do pagamento; não processa pagamentos reais.

### 9. Consultar rotas
Acesse a página **Rotas** pelo menu. As coletas ativas são agrupadas conforme o nome da rota informado no cadastro. A página exibe resumos por rota. **Não há mapa, GPS nem cálculo automático de trajetos** nesta versão.

### 10. Consultar histórico
Abra a opção **Histórico** para visualizar os eventos registrados no sistema e os registros arquivados. Também é possível consultar o histórico de uma coleta específica.

### 11. Arquivar e excluir permanentemente
- **Arquivar:** retira a coleta da listagem de registros ativos, preservando seus dados e histórico.
- **Excluir permanentemente:** opção disponível para registros arquivados; remove a coleta e os eventos de histórico associados. Utilize com cuidado, pois não há recuperação automática dessa exclusão.

### 12. Encerrar a aplicação
No terminal onde o Flask está em execução, pressione **Ctrl+C**. Para utilizar novamente, ative o ambiente virtual se necessário, execute `python app.py` e abra o endereço local.

### 13. Cópia de segurança
Com a aplicação encerrada, faça uma cópia do arquivo `gameleira.db` para um local seguro. Esse arquivo contém os registros das coletas e do histórico. Evite substituir o banco por um arquivo vazio ao atualizar o projeto.

### 14. Limitações conhecidas
- Aplicação de demonstração acadêmica, executada localmente.
- Não possui autenticação de usuários na versão analisada.
- Não possui integração com mapas ou pagamentos financeiros.
- Recursos de acessibilidade e responsividade passaram por verificações iniciais, mas ainda necessitam de avaliação externa.
- O uso em ambiente público/produção exigiria revisão de segurança e configuração.

### 15. Solução de problemas
**Mensagem “can't open file ... app.py”:** abra o terminal na pasta correta, que contém `app.py`.  
**Mensagem “No module named flask”:** ative o ambiente virtual e execute `python -m pip install -r requirements.txt`.  
**Página não abre:** confirme se `python app.py` está em execução e se o navegador acessa `http://127.0.0.1:5000`.  
**Registros não aparecem:** verifique filtros e pesquisa e confira se os registros foram arquivados.
