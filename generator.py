import string
import secrets
import sys
import os
import csv
from dotenv import load_dotenv

load_dotenv()

def check_env_vars():
    """Verifica e retorna todas as variáveis de ambiente necessárias com fallbacks e corrige extensões."""
    try:
        tamanho = int(os.getenv("PASSWORD_LENGTH", "8"))
        inicio = int(os.getenv("START_INDEX", "1001"))
    except ValueError:
        print("Erro: PASSWORD_LENGTH e START_INDEX devem ser números inteiros.")
        sys.exit(1)

    input_f = os.getenv("INPUT_FILE", "times") # Fallback sem extensão
    out_dir = os.getenv("OUTPUT_DIR", "output")
    out_txt = os.getenv("OUTPUT_TXT", "boca_config")
    out_csv_cred = os.getenv("OUTPUT_CSV_CREDENTIALS", "credenciais")
    out_csv_pres = os.getenv("OUTPUT_CSV_ATTENDANCE", "lista_presenca")

    # --- CORREÇÃO INTELIGENTE DE EXTENSÕES ---
    # Verifica a entrada
    if not input_f.endswith(('.txt', '.csv')): # Aceita .txt ou .csv se você fornecer, senão põe .txt
        input_f += '.txt'

    # Verifica as saídas
    if not out_txt.endswith('.txt'):
        out_txt += '.txt'
    
    if not out_csv_cred.endswith('.csv'):
        out_csv_cred += '.csv'
        
    if not out_csv_pres.endswith('.csv'):
        out_csv_pres += '.csv'

    return tamanho, inicio, input_f, out_dir, out_txt, out_csv_cred, out_csv_pres

def gerar_senha(tamanho):
    alfabeto = string.ascii_lowercase + string.digits
    return "".join(secrets.choice(alfabeto) for _ in range(tamanho))

def main():
    # 1. Carrega configurações
    tamanho_senha, user_index, in_file, out_dir, out_txt, out_csv_cred, out_csv_pres = check_env_vars()

    # 2. Valida arquivo de entrada
    if not os.path.exists(in_file):
        print(f"Erro: Arquivo de entrada '{in_file}' não encontrado.")
        sys.exit(1)

    # 3. Cria a pasta de output se ela não existir
    os.makedirs(out_dir, exist_ok=True)

    # 4. Monta os caminhos completos dos arquivos dentro da pasta output
    caminho_txt = os.path.join(out_dir, out_txt)
    caminho_csv_cred = os.path.join(out_dir, out_csv_cred)
    caminho_csv_pres = os.path.join(out_dir, out_csv_pres)

    try:
        # Abre o arquivo de entrada e os TRÊS arquivos de saída
        with open(in_file, 'r', encoding='utf-8') as f_in, \
             open(caminho_txt, 'w', encoding='utf-8') as f_txt, \
             open(caminho_csv_cred, 'w', encoding='utf-8', newline='') as f_csv_cred, \
             open(caminho_csv_pres, 'w', encoding='utf-8', newline='') as f_csv_pres:
            
            # Configura os gravadores de CSV
            writer_cred = csv.writer(f_csv_cred)
            writer_cred.writerow(['Nome', 'Usuario', 'Senha'])

            writer_pres = csv.writer(f_csv_pres)
            writer_pres.writerow(['Nome', 'Usuario', 'Presente'])

            f_txt.write("[user]\n")
            
            for linha in f_in:
                fullname = linha.strip()
                if not fullname:
                    continue

                username = f"team{user_index}"
                password = gerar_senha(tamanho_senha)

                # Escrita no arquivo TXT (Formato BOCA)
                f_txt.write(f"usernumber={user_index}\n")
                f_txt.write("usersitenumber=1\n")
                f_txt.write(f"username={username}\n")
                f_txt.write(f"userpassword={password}\n")
                f_txt.write("usertype=team\n")
                f_txt.write(f"userfullname={fullname}\n")
                f_txt.write(f"userdesc=Team{user_index}\n")
                f_txt.write("usermultilogin=t\n")
                f_txt.write("userenabled=t\n")
                f_txt.write("userchangepassword=f\n\n")

                # Escrita no CSV de Credenciais
                writer_cred.writerow([fullname, username, password])

                # Escrita no CSV de Presença (coluna 'Presente' em branco)
                writer_pres.writerow([fullname, username, ""])

                user_index += 1
        
        print(f"Sucesso! Arquivos gerados na pasta '{out_dir}':")
        print(f"- {out_txt}")
        print(f"- {out_csv_cred}")
        print(f"- {out_csv_pres}")

    except Exception as e:
        print(f"Erro durante o processamento: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()