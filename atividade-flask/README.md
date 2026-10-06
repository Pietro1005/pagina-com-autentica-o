# Atividade Flask - Autenticação e Hash

Projeto escolar de Flask com SQLite, autenticação, sessões e hash de senha.

## Funcionalidades

- Página pessoal pública
- Login
- Senha armazenada como SHA-256
- Sessão de usuário
- Página restrita de perfil
- Página restrita de projetos
- Conteúdo dinâmico vindo do SQLite
- Logout

## Credenciais fictícias

Usuário: `aluno_exemplo`

Senha: `Aula@1234`

## Como executar

```bash
pip install -r requirements.txt
python app.py
```

Depois abra no navegador:

`http://127.0.0.1:5000`

O banco `atividade_flask.db` é criado automaticamente na primeira execução.

> SHA-256 está sendo usado aqui apenas para fins didáticos, seguindo a atividade de hashes. Para sistemas reais, recomenda-se uma função própria para armazenamento de senhas, como Argon2id, scrypt ou PBKDF2.
