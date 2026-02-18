# Back End Engineering Project

API REST desenvolvida com FastAPI e SQLModel.

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

## 🚀 Instalação e Configuração

### 1. Instalar o projeto na máquina

#### Linux / macOS:
```bash
# Clone ou navegue até a pasta do projeto
cd back_end_eng

# Instale as dependências (após criar e ativar a venv - veja passo 2)
pip install -r requirements.txt
```

#### Windows (CMD):
```cmd
cd back_end_eng

REM Instale as dependências (após criar e ativar a venv - veja passo 2)
pip install -r requirements.txt
```

#### Windows (PowerShell):
```powershell
cd back_end_eng

# Instale as dependências (após criar e ativar a venv - veja passo 2)
pip install -r requirements.txt
```

---

### 2. Inicializar a .venv (Ambiente Virtual)

#### Linux / macOS:
```bash
# Criar o ambiente virtual
python3 -m venv .venv

# Ativar o ambiente virtual
source .venv/bin/activate
```

#### Windows (CMD):
```cmd
REM Criar o ambiente virtual
python -m venv .venv

REM Ativar o ambiente virtual
.venv\Scripts\activate
```

#### Windows (PowerShell):
```powershell
# Criar o ambiente virtual
python -m venv .venv

# Ativar o ambiente virtual
.\.venv\Scripts\Activate.ps1
```

**Nota para PowerShell:** Se aparecer erro de política de execução, execute como administrador:
```powershell
Set-ExecutionPolicy RemoteSigned
```
Depois feche e abra o PowerShell novamente.

---

### 3. Inicializar a FastAPI

#### Linux / macOS:
```bash
# Certifique-se de que a venv está ativada (deve aparecer (.venv) no prompt)
# Instale as dependências se ainda não instalou
pip install -r requirements.txt

# Inicie o servidor FastAPI
uvicorn main:app --reload
```

#### Windows (CMD):
```cmd
REM Certifique-se de que a venv está ativada (deve aparecer (.venv) no prompt)
REM Instale as dependências se ainda não instalou
pip install -r requirements.txt

REM Inicie o servidor FastAPI
uvicorn main:app --reload
```

#### Windows (PowerShell):
```powershell
# Certifique-se de que a venv está ativada (deve aparecer (.venv) no prompt)
# Instale as dependências se ainda não instalou
pip install -r requirements.txt

# Inicie o servidor FastAPI
uvicorn main:app --reload
```

---

## 🌐 Acessar a API

Após iniciar o servidor, a API estará disponível em:

- **API:** http://127.0.0.1:8000
- **Documentação interativa (Swagger UI):** http://127.0.0.1:8000/docs
- **Documentação alternativa (ReDoc):** http://127.0.0.1:8000/redoc

---

## 📝 Comandos Rápidos

### Sequência completa (Linux/macOS):
```bash
cd back_end_eng
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Sequência completa (Windows CMD):
```cmd
cd back_end_eng
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Sequência completa (Windows PowerShell):
```powershell
cd back_end_eng
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## ⚠️ Observações

- Sempre ative a `.venv` antes de instalar dependências ou executar o projeto
- O arquivo `database.db` será criado automaticamente na primeira execução
- Use `Ctrl+C` para parar o servidor FastAPI
