
# README

## Descrição

Automação em Python para extrair e tratar dados do banco de dados Oracle SQL, fazendo cruzamentos para preparar os dados para serem importados cada um para sua campanha específica via API da compainha telefonica da empresa. O marketing tem a necessidade de ter os dados salvos em CSV na rede da empresa, dividos em lotes de 10000 para cada especialidade. A cada mês que passa, os VOIPs alternam entra A e B, lógica que foi implementada com uma verificação se o mês é par ou ímpar. Essa tarefa mensal tem objetivo de preparar todos os VOIPs do mês para realizarem ligações robotizadas para atrair clientes antigos.

## Estrutura do Projeto

A estrutura do projeto é dividida nos seguintes módulos:

### 1. **src/main.py**
Este é o arquivo principal que executa as principais funções, como extrair, tratar e importar os dados via API.

### 2. **src/modules/config.py**
Carrega e verifica as variáveis de ambiente necessárias para a execução do projeto.

### 3. **src/modules/database.py**
Este módulo contém uma classe (Oracle) com todas as funções relacionadas ao banco de dados Oracle SQL. Dentro da classe temos algumas funções como:
- `__init__(self)`: Conecta ao banco de dados e abre o cursor para os comandos SQL.
- `close()`: Fecha conexão e o cursor do banco de dados.
- `extract_data(self, sql: str, params: dict = None) -> list:`: Função genérica para executar os comandos SQL e retornar os dados coletados.
- `database_insert(self, df: pd.DataFrame, table: str) -> None:`: Função genérica para inserir dados ao banco de dados.
- `sequence_voip_commands_sql(self) -> None:`: Função para executar uma sequencia de comandos SQL específicos.

### 4. **src/modules/process_data.py**
Este módulo contém funções para processar e tratar os dados extraídos do banco para importar via API. As principais funções são:
- `select_file() -> str:`: Função para permitir que o usuário escolha o arquivo a ser utilizado.
- `process_procon_to_df() -> pd.DataFrame`: Função específica para converter a planilha com os telefones do procon, para um dataFrame.
- `process_voip_ranking_paramns() -> dict`: Função específica para extrair o ranking de ligações das consultas completadas, para depois dar prioridades específicas para cada uma.
- `import_to_api(file_path: str, campaing_id: int) -> None`: Função para importar os dados corretos para a campanha correta via API.
- `save_csv(df_temp: pd.DataFrame, name: str, num: int) -> str`: Função para salvar os dados em arquivos CSV.
- `process_excel_and_send_api() -> None`: Função principal para utiliar as outras funções para processar todos os dados da planilha excel gerada no arquivo main, para dividi-los em lotes de 10000, agrupando por especialidade, salva-los em CSV e importa-los via API.

### 5. **src/modules/logger.py**
Gerencia a geração de logs para monitoramento e diagnóstico. Utiliza o módulo `logging` para registrar mensagens de erro, aviso e informações.

### 6. **src/queries_sql/sql_voips.py**
Este módulo contém todos comandos SQL usados no projeto, para fácil localização e manutenção.

## Variáveis de Ambiente

- `DB_NAME`=nome-do-banco
- `DB_USER`=usuario-do-banco
- `DB_PASSWORD`=senha-do-banco
- `X5_TOKEN`=chave-da-api.
- `X5_BASE_URL`=url-base-da-api.
