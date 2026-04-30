# 🚀 Gerador de Usuários para BOCA

Script em Python para criação automatizada de usuários em lote para o sistema BOCA, gerando:

* 📄 Arquivo `.txt` de configuração de usuários compatível com BOCA
* 📊 Planilha Excel com credenciais
* 📊 Planilha Excel para lista de presença

---

## 📦 Funcionalidades

* Geração automática de usernames sequenciais
* Criação de senhas seguras aleatórias
* Exportação em múltiplos formatos
* Configuração flexível via `.env`
* Validação automática de parâmetros

---

## 🛠️ Requisitos

* Python 3.8+

Instale as dependências:

```bash
pip install -r requirements.txt
```

**requirements.txt**

```
python-dotenv
openpyxl
```

---

## ⚙️ Configuração

### 1. Criar arquivo `.env`

Copie o arquivo de exemplo:

```bash
cp .env.example .env
```

Edite conforme necessário:

```env
# ==========================================
# Configurações Gerais e de Arquivos
# ==========================================

PASSWORD_LENGTH=8
START_INDEX=1001
USER_CLASS=Turma 1
INPUT_FILE=users.txt
OUTPUT_DIR=output
OUTPUT_TXT=boca_users.txt
OUTPUT_EXCEL_CREDENTIALS=credenciais.xlsx
OUTPUT_EXCEL_ATTENDANCE=lista_presenca.xlsx

# ==========================================
# Configurações BOCA
# ==========================================

BOCA_SITE_NUMBER=1
BOCA_USER_TYPE=team
BOCA_MULTI_LOGIN=t
BOCA_USER_ENABLED=t
BOCA_CHANGE_PASSWORD=f
```

---

## 📥 Arquivo de Entrada

Crie o arquivo definido em `INPUT_FILE` (ex: `users.txt`):

```
João Silva
Maria Souza
Equipe Alpha
Equipe Beta
```

**Regras:**

* Um nome por linha
* Linhas vazias são ignoradas

---

## ▶️ Como Executar

```bash
python generator.py
```

---

## 📤 Saída Gerada

Os arquivos serão criados na pasta definida em `OUTPUT_DIR`:

```
output/
├── boca_users.txt
├── credenciais.xlsx
└── lista_presenca.xlsx
```

---

## 📄 Arquivo BOCA (`boca_users.txt`)

Formato gerado:

```
[user]
usernumber=1001
usersitenumber=1
username=team1001
userpassword=abc123xy
usertype=team
userfullname=João Silva (team1001)
userdesc=Team 1001
usermultilogin=t
userenabled=t
userchangepassword=f
```

---

## 📊 Planilha de Credenciais

| Nome                  | Usuario  | Senha    | Turma   |
| --------------------- | -------- | -------- | ------- |
| João Silva (team1001) | team1001 | abc123xy | Turma 1 |

---

## 📊 Planilha de Presença

| Nome                  | Usuario  | Turma   | Presente |
| --------------------- | -------- | ------- | -------- |
| João Silva (team1001) | team1001 | Turma 1 |          |

---

## 🔐 Como Funciona

### Geração de Senhas

* Utiliza `secrets` (seguro criptograficamente)
* Caracteres: `a-z` + `0-9`
* Tamanho definido por `PASSWORD_LENGTH`

---

### Geração de Usuários

Formato:

```
{BOCA_USER_TYPE}{START_INDEX}
```

Exemplo:

```
team1001
team1002
team1003
```

---

### Fluxo do Script

1. Cria arquivos base automaticamente (se não existirem)
2. Carrega variáveis do `.env`
3. Valida configurações
4. Lê o arquivo de entrada
5. Para cada linha:

   * Gera username
   * Gera senha
   * Escreve no arquivo BOCA
   * Adiciona nas planilhas
6. Salva os arquivos na pasta de saída

---

## ⚠️ Validações Importantes

* `PASSWORD_LENGTH` e `START_INDEX` devem ser números inteiros
* `BOCA_SITE_NUMBER` deve ser inteiro
* `BOCA_USER_TYPE` deve ser um dos:

  ```
  team | staff | score | judge | admin | site
  ```
* Flags booleanas aceitam apenas:

  ```
  t | f
  ```

---

## ❌ Possíveis Erros

### Arquivo de entrada não encontrado

```
Erro: Arquivo de entrada 'users.txt' não encontrado
```

➡️ Solução: criar o arquivo corretamente

---

### Dependências ausentes

```
Dependências ausentes detectadas
```

➡️ Solução:

```bash
pip install -r requirements.txt
```

---

### Erro na configuração `.env`

Exemplo:

```
Erro: PASSWORD_LENGTH deve ser número inteiro
```

➡️ Solução: corrigir valores inválidos

---

## 💡 Dicas

* Você pode usar `.csv` como entrada também
* O script corrige automaticamente extensões ausentes
* Ideal para competições, escolas e eventos

---

## 🧩 Estrutura do Projeto

```
.
├── generator.py
├── .env
├── .env.example
├── requirements.txt
├── users.txt
└── output/
```

---

## ✅ Resultado

Com poucos passos, você gera:

* Usuários prontos para importação no BOCA
* Planilha de credenciais organizada
* Lista de presença pronta para uso

---

Feito para automatizar e evitar trabalho manual em massa 🚀
