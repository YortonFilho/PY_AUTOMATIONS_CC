import os
import oracledb
import pandas as pd
import datetime
from openpyxl.workbook import Workbook
from modules.logger import get_logger
from modules.config import DB_NAME, DB_PASSWORD, DB_USER

# Logger configuration
logger = get_logger()

def calculate_date() -> str:
    """
    Function to calculate the first day and of the last day previous month
    """
    # Getting todays date
    today = datetime.date.today()

    # The first day of the current month
    first_day_current_month = today.replace(day=1)

    # The last day of the previous month
    last_day_previous_month = first_day_current_month - datetime.timedelta(days=1)
    
    # The first day of the previuos month
    first_day_previous_month = last_day_previous_month.replace(day=1)

    # Formatting the dates to the 'DD/MM/AAAA'
    formatted_first_day = first_day_previous_month.strftime('%d/%m/%Y')
    formatted_last_day = last_day_previous_month.strftime('%d/%m/%Y')

    # Formatting the string with the dates
    formatted_date = f"'{formatted_first_day}' AND '{formatted_last_day}'"

    return formatted_date

def init_oracle_client() -> None:
    """
    Functon to initialize the Oracle Client
    """
    client_path = r"C:\instantclient_19_21"

    try:
        os.environ["PATH"] = client_path + ";" + os.environ.get("PATH", "")
        oracledb.init_oracle_client(lib_dir=client_path)
        logger.info(f"Cliente Oracle inicializado com sucesso usando o caminho: {client_path}")
    except Exception as e:
        logger.error(f"Erro ao inicializar o cliente Oracle: {e}")
        raise e

def database_connection():
    """
    Function to connect to the databse
    """
    init_oracle_client() # Initialize Oracle Client

    try:
        connection = oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_NAME)
        logger.info("Banco de dados conectado com sucesso!")
        return connection
    except oracledb.Error as e:
        logger.error(f"Falha ao tentar conexão com banco de dados! {e}")
        raise e

def database_extract() -> pd.DataFrame:
    """
    Function to extract data from the database and return it as a dataFrame
    """
    try:
        with database_connection() as connection:
            with connection.cursor() as cursor:
                formatted_date = calculate_date()

                # Query to extract data
                query = f"""
                    select

                        "DATA_AGENDA","HORA","TIPO_AGENDA","TIPO_ENCAIXE","NOME_MEDICO","MEDICO_EXECUTOR","FILIAL","IDADE","RE_CONSULTA","EXAME","PACIENTE","CONFIRMADO","ESPECIALIDADE","COD_PACIENTE","RESERVA","BLOQUEIO","TIPO_MED","QTD_TT"

                        from (

                        select trunc(d) data_agenda,
                            substr(af.hora_agenda,1,2)||':'||substr(af.hora_agenda,3,2) hora,
                            substr(f_tipo_agenda(f.cod_filial,m.cod_medico,d,af.hora_agenda),1,10) tipo_agenda,
                            substr(f_get_tipo_encaixe(af.cod_filial,af.cod_executor,trunc(d),af.hora_agenda),1,1) tipo_encaixe,
                            m.nome as nome_medico,
                            m.abreviatura medico_executor,
                            f.abrev filial,
                            null idade,
                            null re_consulta,
                            null exame,
                            null paciente,
                            null confirmado,
                            em.descricao especialidade,
                            null cod_paciente,
                            f_get_obs_agenda(f.cod_filial,m.cod_medico,d,af.hora_agenda) reserva,
                            f_agenda_motivo_look(f.cod_filial,af.cod_executor,d,af.hora_agenda) bloqueio,
                            --REPLACE(am.tipo_agenda, CHR(10), ' ') as tipo_med,       
                            replace(REPLACE(REPLACE(REPLACE(am.tipo_agenda, CHR(10), ' '), CHR(13), ' '), CHR(9), ' '), CHR(160), ' ') AS tipo_med,      
                            1 as qtd_tt
                        from (select trunc(sysdate) - 1500 + (ROWNUM -1) d
                            from dual connect by level <= 3000),
                            agenda_conf af,
                            filial f,
                            medico m,
                            agenda_medico am,
                            especialidade_medica em
                        where af.cod_filial = f.cod_filial
                        and af.cod_executor = m.cod_medico
                        and af.seq_conf = am.seq_agenda_med
                        and am.status = 'S'
                        and trunc(d) between trunc(am.data_ini) and trunc(am.data_fim)
                        and af.dia_semana = to_char(d,'D')
                        and (select count(1)
                            from agenda_horario ah
                            where ah.cod_filial = af.cod_filial
                            and ah.cod_executor = af.cod_executor
                            and ah.hora_agenda  = af.hora_agenda
                            and trunc(ah.data_agenda)  = trunc(d)) = 0
                        and m.cod_especialidade = em.cod_especialidade(+)
                        -- Primeira
                        and trunc(d) BETWEEN {formatted_date}
                        -- Lógica de data
                        and f.abrev in ('CC ALVORADA',
                        'CC ANDRADAS',
                        'CC ANDRADAS 1722',
                        'CC ASSIS ANTIGO',
                        'CC ASSIS BRASIL 3044',
                        'CC ASSIS BRASIL 3224',
                        'CC AZENHA',
                        'CC CACHOEIRINHA',
                        'CC CANOAS',
                        'CC DR FLORES 4 ANDAR',
                        'CC DR FLORES 7 ANDAR',
                        'CC GRAVATAI',
                        'CC DR FLORES 47',
                        'CC OTAVIO ROCHA',
                        'CC ONLINE')
                        and m.nome not in ('CENTRAL DE CONSULTAS MÉDICAS DOM FELICIANO','CENTRAL DE CONSULTAS ADM E COBRANCA')
                        
                        union all
                        select h.data_agenda,
                            substr(h.hora_agenda,1,2)||':'||substr(h.hora_agenda,3,2) hora,
                            h.tipo_agenda,
                            substr(f_get_tipo_encaixe(h.cod_filial,h.cod_executor,h.data_agenda,h.hora_agenda),1,1) tipo_encaixe,
                            m.nome as nome_medico,
                            m.abreviatura medico_executor,
                            f.abrev filial,
                            trunc(Months_between(sysdate,p.data_nascimento)/12) idade,
                            h.re_consulta,
                            e.descricao exame,
                            p.nome paciente,
                            h.confirmado,
                            em.descricao especialidade,
                            p.cod_paciente,
                            h.observacao reserva,
                            f_agenda_motivo_look(h.cod_filial,h.cod_executor,h.data_agenda,h.hora_agenda) bloqueio,
                            --REPLACE(get_tipo_med_age(h.cod_filial,h.cod_executor,h.data_agenda,h.hora_agenda), CHR(10), ' ') as tipo_med,
                            replace(REPLACE(REPLACE(REPLACE(get_tipo_med_age(h.cod_filial,h.cod_executor,h.data_agenda,h.hora_agenda), CHR(10), ' '), CHR(13), ' '), CHR(9), ' '), CHR(160), ' ') AS tipo_med,
                            1 as qtd_tt
                        from agenda_horario h,
                            agenda a,
                            filial f,
                            medico m,
                            especialidade_medica em,
                            exame e,
                            paciente p
                        where h.cod_filial = f.cod_filial
                        and h.cod_executor = m.cod_medico
                        -- Segunda
                        and trunc(h.data_agenda) BETWEEN {formatted_date}
                        -- Lógica de data
                        and h.cod_agenda = a.cod_agenda(+)
                        and h.cod_exame  = e.cod_exame(+)
                        and m.cod_especialidade = em.cod_especialidade(+)
                        and a.cod_paciente = p.cod_paciente(+)
                        and f.abrev in ('CC ALVORADA',
                        'CC ANDRADAS',
                        'CC ANDRADAS 1722',
                        'CC ASSIS ANTIGO',
                        'CC ASSIS BRASIL 3044',
                        'CC ASSIS BRASIL 3224',
                        'CC AZENHA',
                        'CC CACHOEIRINHA',
                        'CC CANOAS',
                        'CC DR FLORES 4 ANDAR',
                        'CC DR FLORES 7 ANDAR',
                        'CC GRAVATAI',
                        'CC OTAVIO ROCHA',
                        'CC DR FLORES 47',
                        'CC ONLINE')
                        and m.nome not in ('CENTRAL DE CONSULTAS MÉDICAS DOM FELICIANO','CENTRAL DE CONSULTAS ADM E COBRANCA')
                        
                        ) t
                        
                        --where t.tipo_med is null
                        
                        order by 1,2
                    """
                
                # Execute the query command
                cursor.execute(query)
                data = cursor.fetchall()
                
                # Check if there is data
                if not data:
                    logger.warning("Nenhum dado encontrado na consulta.")
                    raise
                
                # Colect columns name
                columns = [column[0] for column in cursor.description]
                df = pd.DataFrame(data, columns=columns)
                logger.info(f"Dados extraídos com sucesso. Total de {len(df)} registros.")
                return df
            
    except Exception as e:
        logger.error(f"Erro ao extrair dados: {e}")
        raise e
    
def database_update(df):
    """
    Function to update the table in the database with data from the dataFrame

    :param df: DataFrame
    """
    with database_connection() as connection:
        with connection.cursor() as cursor:
            formatted_date = calculate_date()

            table = "DADOS_AGENDAS_MEDICAS"
            
            # Get columns of the table
            cursor.execute(f"SELECT COLUMN_NAME FROM ALL_TAB_COLUMNS WHERE TABLE_NAME = '{table}'")
            columns = [row[0] for row in cursor.fetchall()]
            num_columns = len(columns)

            # Order the columns of the dataFrame to match the table's columns
            df_filtered = df[columns] 

            # Check if the number of columns in the dataframe and table are equal
            if len(df_filtered.columns) != num_columns:
                raise logger.error(
                    f"Número de colunas no DataFrame ({len(df_filtered.columns)})" 
                    f"não corresponde ao número de colunas na tabela Oracle ({num_columns})."
                )

            # Prepare the query for inserting data
            placeholders = ', '.join([f':{col}' for col in columns])  # Using :column_name as placeholder
            insert_command = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"

            try:
                # Delete data in table
                cursor.execute(f"DELETE FROM {table} WHERE DATA_AGENDA BETWEEN {formatted_date}")
                logger.info(f"Dados da tabela deletados com sucesso!")

                # Insert new data
                for index, row in df_filtered.iterrows():
                    values = row.to_dict()  # Convert row to dictionary

                    try:
                        cursor.execute(insert_command, values)  # Pass dictionary for binding variables
                    except oracledb.Error as e:
                        logger.error(f"Erro ao inserir os seguintes dados: {values} ERRO: {e})")
                        connection.rollback() 
                        raise e

                connection.commit()
                logger.info(f"Todos os dados foram inseridos na tabela '{table}'!")

            except oracledb.Error as e:   
                logger.error(f"Erro ao deletar dados da tabela {table}: {e}")
                connection.rollback()
                raise e

# Test area
if __name__ == "__main__":
    data = database_extract()
