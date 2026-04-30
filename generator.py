import string
import secrets
import sys
import os
from openpyxl import Workbook
from dotenv import load_dotenv

load_dotenv()

def check_boca_configs():
    """Lê, aplica fallbacks e valida as configurações específicas do BOCA."""
    site_number = os.getenv("BOCA_SITE_NUMBER", "1")
    user_type = os.getenv("BOCA_USER_TYPE", "team").lower()
    multi_login = os.getenv("BOCA_MULTI_LOGIN", "t").lower()
    enabled = os.getenv("BOCA_USER_ENABLED", "t").lower()
    change_pass = os.getenv("BOCA_CHANGE_PASSWORD", "f").lower()

    if not site_number.isdigit():
        print(f"Erro na env: BOCA_SITE_NUMBER deve ser um número inteiro (Atual: '{site_number}').")
        sys.exit(1)

    tipos_validos = ["team", "staff", "score", "judge", "admin", "site"]
    if user_type not in tipos_validos:
        print(f"Erro na env: BOCA_USER_TYPE '{user_type}' é inválido. Opções permitidas: {', '.join(tipos_validos)}.")
        sys.exit(1)

    booleanos_validos = ["t", "f"]
    if multi_login not in booleanos_validos:
        print(f"Erro na env: BOCA_MULTI_LOGIN '{multi_login}' é inválido. Opções permitidas: t, f.")
        sys.exit(1)

    if enabled not in booleanos_validos:
        print(f"Erro na env: BOCA_USER_ENABLED '{enabled}' é inválido. Opções permitidas: t, f.")
        sys.exit(1)

    if change_pass not in booleanos_validos:
        print(f"Erro na env: BOCA_CHANGE_PASSWORD '{change_pass}' é inválido. Opções permitidas: t, f.")
        sys.exit(1)

    return site_number, user_type, multi_login, enabled, change_pass

def check_env_vars():
    """Verifica e retorna todas as variáveis de ambiente de arquivo/geração com fallbacks."""
    try:
        tamanho = int(os.getenv("PASSWORD_LENGTH", "8"))
        inicio = int(os.getenv("START_INDEX", "1001"))
    except ValueError:
        print("Erro: PASSWORD_LENGTH e START_INDEX devem ser números inteiros.")
        sys.exit(1)

    input_f = os.getenv("INPUT_FILE", "times")
    out_dir = os.getenv("OUTPUT_DIR", "output")
    out_txt = os.getenv("OUTPUT_TXT", "boca_config")
    
    # Atualizado para buscar variáveis de Excel (XLSX)
    out_excel_cred = os.getenv("OUTPUT_EXCEL_CREDENTIALS", "credenciais")
    out_excel_pres = os.getenv("OUTPUT_EXCEL_ATTENDANCE", "lista_presenca")
    user_class = os.getenv("USER_CLASS", "Geral")

    if not input_f.endswith(('.txt', '.csv')):
        input_f += '.txt'
    if not out_txt.endswith('.txt'):
        out_txt += '.txt'
    
    # Correção de extensão para XLSX
    if not out_excel_cred.endswith('.xlsx'):
        out_excel_cred += '.xlsx'
    if not out_excel_pres.endswith('.xlsx'):
        out_excel_pres += '.xlsx'

    return tamanho, inicio, input_f, out_dir, out_txt, out_excel_cred, out_excel_pres, user_class

def gerar_senha(tamanho):
    alfabeto = string.ascii_lowercase + string.digits
    return "".join(secrets.choice(alfabeto) for _ in range(tamanho))

def main():
    print("\n\t[-] BOCA USERS GENERATOR - by João Guilherme\n\n\n")
    # 1. Carrega e valida configurações GERAIS
    tamanho_senha, user_index, in_file, out_dir, out_txt, out_excel_cred, out_excel_pres, user_class = check_env_vars()

    # 2. Carrega e valida configurações do BOCA
    boca_site, boca_type, boca_multilogin, boca_enabled, boca_changepass = check_boca_configs()

    # 3. Valida arquivo de entrada
    if not os.path.exists(in_file):
        print(f"Erro: Arquivo de entrada '{in_file}' não encontrado.")
        sys.exit(1)

    # 4. Cria a pasta de output se ela não existir
    os.makedirs(out_dir, exist_ok=True)

    # 5. Monta os caminhos completos
    caminho_txt = os.path.join(out_dir, out_txt)
    caminho_excel_cred = os.path.join(out_dir, out_excel_cred)
    caminho_excel_pres = os.path.join(out_dir, out_excel_pres)

    # 6. Inicializa as planilhas do Excel na memória
    wb_cred = Workbook()
    ws_cred = wb_cred.active
    ws_cred.title = "Credenciais"
    ws_cred.append(['Nome', 'Usuario', 'Senha', 'Turma']) # Cabeçalho

    wb_pres = Workbook()
    ws_pres = wb_pres.active
    ws_pres.title = "Lista de Presenca"
    ws_pres.append(['Nome', 'Usuario', 'Turma', 'Presente']) # Cabeçalho

    try:
        # Abre o arquivo de entrada e cria o de saída do BOCA (txt)
        with open(in_file, 'r', encoding='utf-8') as f_in, \
             open(caminho_txt, 'w', encoding='utf-8') as f_txt:
            
            # Cabeçalho global do BOCA
            f_txt.write("[user]\n")
            
            for linha in f_in:
                nome_original = linha.strip()
                if not nome_original:
                    continue

                username = f"{boca_type}{user_index}"
                fullname_formatado = f"{nome_original} ({username})"
                password = gerar_senha(tamanho_senha)

                # Escrita no arquivo TXT
                f_txt.write(f"usernumber={user_index}\n")
                f_txt.write(f"usersitenumber={boca_site}\n")
                f_txt.write(f"username={username}\n")
                f_txt.write(f"userpassword={password}\n")
                f_txt.write(f"usertype={boca_type}\n")
                f_txt.write(f"userfullname={fullname_formatado}\n")
                f_txt.write(f"userdesc={boca_type.capitalize()} {user_index}\n")
                f_txt.write(f"usermultilogin={boca_multilogin}\n")
                f_txt.write(f"userenabled={boca_enabled}\n")
                f_txt.write(f"userchangepassword={boca_changepass}\n\n")

                # Adiciona as linhas nas planilhas na memória
                ws_cred.append([fullname_formatado, username, password, user_class])
                ws_pres.append([fullname_formatado, username, user_class, ""])

                user_index += 1

        # 7. Salva as planilhas do Excel fisicamente na pasta de output
        wb_cred.save(caminho_excel_cred)
        wb_pres.save(caminho_excel_pres)
        
        print(f"Sucesso! Arquivos gerados na pasta '{out_dir}':")
        print(f"- {out_txt} (Config: Tipo '{boca_type}', Site '{boca_site}')")
        print(f"- {out_excel_cred}")
        print(f"- {out_excel_pres}")

    except Exception as e:
        print(f"Erro durante a gravação dos arquivos: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()