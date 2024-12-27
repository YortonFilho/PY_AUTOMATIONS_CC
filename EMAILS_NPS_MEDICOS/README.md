# README

## Descrição

Este repositório contém um projeto em Python utilizado para extrair dados de um banco de dados Oracle SQL, gerar e enviar e-mails personalizados com uma estrutura HTML e com os resultados de uma pesquisa de satisfação (NPS) para médicos.

Infelizmente tive que botar o template HTML no gitignore, pois tinha muitas informações da empresa, como endereços, contatos, etc...

## Estrutura do Projeto

O projeto é dividido em diversos módulos, cada um com responsabilidades específicas:

### 1. **main.py**
Este é o arquivo principal que integra as funções de extração de dados e envio de e-mails. Ele realiza os seguintes passos:
- Extrai dados dos médicos do banco de dados Oracle.
- Envia e-mails personalizados para os médicos com base nesses dados.

### 2. **modules/database.py**
Contém funções para conectar ao banco de dados Oracle e extrair os dados dos NPS dos médicos. As principais funções são:
- `database_connection()`: Conecta ao banco de dados Oracle.
- `database_extract_nps()`: Executa a consulta SQL para extrair os dados dos médicos e gera um DataFrame com as informações.

### 3. **modules/email_functions.py**
Responsável pelo envio de e-mails personalizados utilizando o servidor SMTP. Ele inclui:
- `calculate_date()`: Calcula o período do NPS com base nas datas do mês anterior.
- `send_email()`: Envia um e-mail com o corpo em HTML.
- `generate_email_body()`: Carrega um template HTML e preenche com os dados dos médicos.
- `send_emails_to_users()`: Envia e-mails para vários destinatários com base nos dados extraídos.

### 4. **modules/logger.py**
Gerencia a geração de logs para monitoramento e diagnóstico. Utiliza o módulo `logging` para registrar mensagens de erro, aviso e informações.

### 5. **modules/config.py**
Carrega e verifica as variáveis de ambiente necessárias para a execução do projeto. Essas variáveis incluem credenciais de conexão ao banco de dados e detalhes de configuração do servidor SMTP.

### 6. **templates/email_template_NPS.html**
Template HTML utilizado para gerar os e-mails personalizados, com informações sobre a pesquisa de satisfação (NPS) e os resultados dos médicos. O template utiliza o Jinja2 para preencher as variáveis dinâmicas.

## Requisitos

Antes de executar o script, é necessário garantir que as seguintes dependências estão instaladas:

- `oracledb`: para conectar ao banco de dados Oracle.
- `pandas`: para manipulação de dados em formato DataFrame.
- `smtplib`: para envio de e-mails.
- `jinja2`: para renderização de templates HTML.
- `python-dotenv`: para carregar variáveis de ambiente a partir de um arquivo `.env`.
- `os`: para manipulação de variáveis de ambiente.

Você pode instalar as dependências com o comando:

```bash
pip install -r requirements.txt
```

## Variáveis de ambiente

- `ZIMBRA_EMAIL`=seu-email@dominio.com
- `ZIMBRA_EMAIL_PASSWORD`=sua-senha
- `SMTP_SERVER`=servidor-smtp.com
- `SMTP_PORT`=porta-do-servidor
- `DB_NAME`=nome-do-banco
- `DB_USER`=usuario-do-banco
- `DB_PASSWORD`=senha-do-banco
