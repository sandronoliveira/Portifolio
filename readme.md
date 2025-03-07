# Portfolio de Sandron Oliveira Silva

Um site de portfólio moderno e minimalista desenvolvido em Python Flask.

## Funcionalidades

- Site com design minimalista e responsivo
- Seções para exibir projetos, competências, formação e certificados
- Sistema de administração com login para gerenciar o conteúdo
- Funcionalidade para adicionar e remover certificados
- Funcionalidade para adicionar e remover projetos

## Requisitos

- Python 3.9+
- Pip (gerenciador de pacotes do Python)

## Instalação

1. Clone este repositório ou faça o download dos arquivos

2. Crie um ambiente virtual (recomendado):
   ```
   python -m venv venv
   ```

3. Ative o ambiente virtual:
   - No Windows:
     ```
     venv\Scripts\activate
     ```
   - No macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

5. Execute o aplicativo:
   ```
   python app.py
   ```

6. Acesse o site em seu navegador:
   ```
   http://localhost:5000
   ```

## Configuração de Login

Por padrão, o sistema cria um usuário administrador com as seguintes credenciais:

- Usuário: `admin`
- Senha: `password`

**Importante**: Altere a senha padrão antes de colocar o site em produção!

Para alterar a senha, você pode editar diretamente no arquivo `app.py` na função `initialize_db()` ou executar o seguinte código Python:

```python
from app import app, db, User
with app.app_context():
    user = User.query.filter_by(username='admin').first()
    if user:
        user.set_password('sua_nova_senha')
        db.session.commit()
```

## Estrutura do Projeto

- `app.py` - Arquivo principal com rotas e configurações
- `static/` - Arquivos estáticos (CSS, JS, imagens)
- `templates/` - Templates HTML do site
- `portfolio.db` - Banco de dados SQLite

## Personalização

Você pode personalizar o site editando os seguintes arquivos:

- `static/css/styles.css` - Estilos do site
- `templates/*.html` - Estrutura das páginas
- `static/js/main.js` - Funcionalidades JavaScript

## Backup do Banco de Dados

O sistema utiliza SQLite para armazenar informações. É recomendado fazer backups regulares do arquivo `portfolio.db`.

## Implantação em Produção

Para implantar em um ambiente de produção, considere:

1. Usar um servidor WSGI como Gunicorn
2. Configurar um proxy reverso com Nginx ou Apache
3. Alterar a chave secreta para uma string segura
4. Desabilitar o modo de depuração

Exemplo de configuração para produção:

```python
app.config['SECRET_KEY'] = 'uma_chave_secreta_muito_longa_e_aleatoria'
app.config['DEBUG'] = False
```

## Licença

Este projeto é de uso pessoal. Todos os direitos reservados.
