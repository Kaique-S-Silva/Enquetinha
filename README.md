# Enquetinha

Bot de Discord para criação de enquetes usando **Slash Commands** e **botões interativos**.

## Funcionalidades

- Criação de enquetes com o comando `/poll`
- Suporte de **2 a 5 opções** por enquete
- Votação através de botões (sem uso de reações)
- Cada usuário pode votar **apenas uma vez** por enquete
- Contagem de votos atualizada em tempo real na mensagem
- Confirmação de voto enviada de forma privada (ephemeral)

## Tecnologias

- [Python 3.14](https://www.python.org/)
- [discord.py](https://discordpy.readthedocs.io/)
- [uv](https://docs.astral.sh/uv/) — gerenciador de dependências e ambiente virtual
- [python-dotenv](https://pypi.org/project/python-dotenv/) — carregamento de variáveis de ambiente

## Pré-requisitos

- [uv](https://docs.astral.sh/uv/getting-started/installation/) instalado
- Uma aplicação/bot criado no [Discord Developer Portal](https://discord.com/developers/applications)

## Configuração

1. Clone o repositório:

   ```bash
   git clone https://github.com/Kaique-S-Silva/Enquetinha
   cd Enquetinha

   ```

2. Instale as dependências descritas em pyproject.toml

   ```toml
   [project]
   name = "enquetinha"
   version = "0.1.0"
   description = "Add your description here"
   readme = "README.md"
   requires-python = ">=3.14"
   dependencies = [
      "aiosqlite>=0.22.1",
      "discord-py>=2.7.1",
      "python-dotenv>=1.2.2",
   ]

   ```

3. Crie um arquivo `.env` na raiz do projeto com o token do seu bot:

   ```env
   TOKEN=seu_token_aqui
   ```

4. No [Discord Developer Portal](https://discord.com/developers/applications), gere um link de convite (OAuth2 URL Generator) com os escopos:

   - `bot`
   - `applications.commands`

   E as permissões de bot:

   - Enviar mensagens
   - Enviar mensagens em tópicos
   - Ver histórico de mensagens
   - Usar comandos de barra
   - Inserir links

5. Use o link gerado para adicionar o bot ao seu servidor.

## Executando o bot

```bash
python main.py
```

Se tudo estiver configurado corretamente, o terminal deve exibir:

```text
Logged as Enquetinha#XXXX
```

## Como usar

No servidor onde o bot foi adicionado, digite:

```text
/poll
```

Preencha a pergunta e as opções desejadas (mínimo 2, máximo 5). O bot enviará em embed com a seleção de escolhas. Escolha uma e o voto será contado. O tempo de timeout é contado em segundos, se não for dado, a enquete ficará infinitamente até algum administrador do servidor finaliza-lá manualmente.

## Estrutura do projeto

```text
Enquetinha/
├── data
│   ├── (banco de dados fica aqui)
├── docker-compose.yml
├── Dockerfile
├── main.py
├── project.md
├── pyproject.toml
├── README.md
├── src
│   ├── commands
│   │   ├── poll.py
│   ├── database
│   │   ├── connection.py
│   │   └── schema.sql
│   ├── utils
│   │   ├── embed.py
│   │   ├── formatting.py
│   └── views
│       ├── poll_view.py
│       ├── poll_view_select.py
└── uv.lock
```