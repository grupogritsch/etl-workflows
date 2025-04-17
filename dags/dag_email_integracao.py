from datetime import datetime, timedelta
import imaplib
import email
import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.hooks.base import BaseHook

# Configurações padrão
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def download_email_attachments():
    # Obter credenciais do Airflow Connection
    try:
        conn = BaseHook.get_connection('imap_conn')
        IMAP_SERVER = conn.host
        IMAP_PORT = conn.port
        EMAIL_ACCOUNT = conn.login
        EMAIL_PASSWORD = conn.password
    except:
        # Fallback para variáveis hardcoded (apenas para desenvolvimento)
        IMAP_SERVER = 'imap.gritsch.com.br'
        IMAP_PORT = 993
        EMAIL_ACCOUNT = 'xml.ctb@gritsch.com.br'
        EMAIL_PASSWORD = 'RtNaXp38Xx'
    
    # Configurações
    DOWNLOAD_FOLDER = '/opt/airflow/datasets'
    PROCESSED_FOLDER = 'Processados'  # Nome da pasta para e-mails processados
    
    # Criar pasta de download se não existir
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)
    
    try:
        # Conectar ao servidor IMAP
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        mail.select('inbox')  # Selecionar a caixa de entrada

        # Verificar/Criar pasta de Processados
        status, folders = mail.list()
        if f'"{PROCESSED_FOLDER}"' not in str(folders):
            mail.create(PROCESSED_FOLDER)
            print(f"Pasta '{PROCESSED_FOLDER}' criada.")

        # Buscar e-mails não lidos
        status, messages = mail.search(None, '(UNSEEN)')
        if status != 'OK':
            print("Nenhum e-mail não lido encontrado.")
            mail.logout()
            return

        email_ids = messages[0].split()
        print(f"Encontrados {len(email_ids)} e-mails não lidos.")

        for email_id in email_ids:
            try:
                # Fetch do e-mail
                status, msg_data = mail.fetch(email_id, '(RFC822)')
                if status != 'OK':
                    print(f"Falha ao buscar e-mail ID {email_id}")
                    continue

                # Parse do e-mail
                raw_email = msg_data[0][1]
                email_message = email.message_from_bytes(raw_email)

                print(f"\nProcessando e-mail - Assunto: {email_message['Subject']}")
                print(f"De: {email_message['From']}")
                print(f"Data: {email_message['Date']}")

                has_attachments = False

                # Verificar anexos
                for part in email_message.walk():
                    if part.get_content_maintype() == 'multipart':
                        continue
                    if part.get('Content-Disposition') is None:
                        continue

                    filename = part.get_filename()
                    if filename:
                        has_attachments = True
                        filepath = os.path.join(DOWNLOAD_FOLDER, filename)
                        with open(filepath, 'wb') as f:
                            f.write(part.get_payload(decode=True))
                        print(f"Anexo salvo: {filepath}")

                # Mover e-mail para pasta de Processados
                mail.copy(email_id, PROCESSED_FOLDER)
                mail.store(email_id, '+FLAGS', '\\Deleted')
                print(f"E-mail movido para a pasta '{PROCESSED_FOLDER}'")

            except Exception as e:
                print(f"Erro ao processar e-mail ID {email_id}: {str(e)}")
                continue

        # Expurgar e-mails marcados para deleção e fechar conexão
        mail.expunge()
        mail.close()
        mail.logout()

    except Exception as e:
        print(f"Erro ao conectar/processar e-mails: {str(e)}")
        raise

# Definir a DAG
dag = DAG(
    'processar_emails_com_anexos',
    default_args=default_args,
    description='DAG para ler e-mails, baixar anexos e mover mensagens processadas',
    schedule_interval=timedelta(minutes=30),  # Executar a cada 30 minutos
    start_date=days_ago(1),
    catchup=False,
    tags=['email', 'imap', 'anexos'],
)

# Definir a tarefa
process_emails = PythonOperator(
    task_id='processar_emails_e_mover_anexos',
    python_callable=download_email_attachments,
    dag=dag,
)

process_emails