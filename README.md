# BandoAPI

BandoAPI é uma aplicação backend desenvolvida com **Python** e **FastAPI**, projetada para replicar funcionalidades principais do X (antigo Twitter). Este projeto é uma iniciativa voltada para aprendizado e prática de desenvolvimento backend, com foco em frameworks modernos, arquitetura orientada a recursos, e integração com bancos de dados.

## Funcionalidades

### Usuários
- **Cadastro de usuários**
  - Criar uma conta fornecendo dados básicos como e-mail e senha.
- **Autenticação e Autorização**
  - Sistema de login com geração de tokens JWT.
  - Middleware para verificação de tokens de acesso.
- **Consultar Perfil**
  - Endpoint para obter informações do usuário logado com base no token JWT.

### Postagens
- **Criar Postagens**
  - Endpoint para criar posts, incluindo a opção de criar respostas para outros posts.
- **Consultar Postagens de um Usuário**
  - Endpoint para listar todos os posts de um usuário específico.
- **Deletar Postagem**
  - Endpoint para marcar uma postagem como excluída (soft delete).

## Tecnologias Utilizadas

- **FastAPI**: Framework web moderno e performático.
- **SQLAlchemy**: ORM para interação com banco de dados.
- **PostgreSQL**: Banco de dados relacional.
- **Pydantic**: Validação e serialização de dados.
- **JWT (JSON Web Tokens)**: Autenticação baseada em tokens.

## Como Rodar o Projeto Localmente

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/gabrielcamurcab/bandoapi.git
   cd bandoapi
   ```

2. **Crie e ative um ambiente virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o banco de dados**:
   - Atualize o arquivo `.env` com as informações do seu banco de dados PostgreSQL.

5. **Inicie o servidor**:
   ```bash
   uvicorn main:app --reload
   ```

6. **Acesse a documentação**:
   - [Swagger UI](http://127.0.0.1:8000/docs)
   - [Redoc](http://127.0.0.1:8000/redoc)

## Próximos Passos

- Implementar sistema de curtidas e repostagens.
- Adicionar busca por posts.
- Melhorar tratamento de erros.
- Escrever testes automatizados.

## Contribuindo

Este projeto é open-source e contribuições são bem-vindas! Sinta-se à vontade para abrir issues, sugerir melhorias ou enviar pull requests.

---

Feito com ❤️ por Gabriel.