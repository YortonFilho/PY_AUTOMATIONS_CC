import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
from jinja2 import Environment, FileSystemLoader
from modules.logger import get_logger
import os

# Configuração de logs
logger = get_logger()

# Configurações do servidor SMTP
smtp_server = os.getenv('SMTP_SERVER')
port = os.getenv('SMTP_PORT')
username = os.getenv('ZIMBRA_EMAIL')
password = os.getenv('ZIMBRA_EMAIL_PASSWORD')

def calculate_date() -> str:
    # Obtendo a data de hoje
    today = datetime.date.today()

    # O primeiro dia do mês atual
    first_day_current_month = today.replace(day=1)
    
    # O último dia do mês anterior
    last_day_previous_month = first_day_current_month - datetime.timedelta(days=1)
    
    # O primeiro dia do mês anterior
    first_day_previous_month = last_day_previous_month.replace(day=1)

    # Formatando as datas para o formato DD/MM/AAAA
    formatted_first_day = first_day_previous_month.strftime('%d/%m/%Y')
    formatted_last_day = last_day_previous_month.strftime('%d/%m/%Y')

    # Formatando a string com as datas
    formatted_date = f'{formatted_first_day} até {formatted_last_day}'

    return formatted_date

def send_email(to_email, subject, html_body, bcc_emails) -> None:
    """
    Função para enviar e-mail com html e cópias ocultas.

    :to_email: Endereço de email para onde será enviado.
    :subject: Assunto do email.
    :html_body: Variável com HTML.
    :bcc_emails: Uma lista de emails, que é inicializada vazia caso não receba nada.
    """

    # Configurando email
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = to_email
    msg['Subject'] = subject
    
    # Adicionando o corpo do e-mail no formato HTML
    msg.attach(MIMEText(html_body, 'html'))

    # Conectar ao servidor SMTP e enviar o e-mail
    try:
        with smtplib.SMTP_SSL(smtp_server, port) as server:
            server.login(username, password)
            server.sendmail(username, [to_email] + bcc_emails, msg.as_string())
            logger.info(f"Email enviado para {to_email}")

    except Exception as e:
        logger.error(f"Erro ao enviar email: {e}")
        raise e
    
def generate_email_body(user_data):
    """
    Função para carregar o template passando as variáveis do destinatário.

    :user_data: Dicionário com os dados do destinatário.
    """

    # Ajustando o caminho para o modelo HTML dentro de 'templates' na pasta pai
    try:
        env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), '..', '.templates')))

        # Carregando template
        template = env.get_template('email_template_NPS.html')
    except Exception as e:
        logger.error(f"Erro ao carregar o template: {e}")
        raise e
    
    date = calculate_date()

    # Renderizar o template com as variáveis extraídas do banco de dados
    html_body = template.render(
        doctor_name=user_data['MEDICO_P1'],
        reporting_date=date,
        quantity=user_data['QTD'],
        doctor_nps=user_data['NPS_MEDICO_AJUSTADO'],
        expected_doctor_nps=user_data['NPS_ESP_AJUSTADO']
    )
    
    return html_body

def send_emails_to_users(users_data, bcc_emails=[]) -> None:
    """
    Função para enviar emails para mais de um destinatário.

    :users_data: dataFrame com os dados dos destinatários.
    :bcc_emails: Lista de emails para cópias ocultas.
    """
    try:
        # Laço de repetição para enviar os emails
        for row in users_data.iterrows():

            # Gerando HTML do email
            html_body = generate_email_body(row[1])

            # Definindo o email do destinatário
            email = row[1]['E_MAIL'] #.strip(';')
            
            # Enviando email com os dados do destinátario
            send_email(to_email=email, bcc_emails=bcc_emails, html_body=html_body, subject='Nota do NPS')

    except Exception as e:
        logger.error(f"Erro ao enviar email para: {email}! {e}")
        raise e