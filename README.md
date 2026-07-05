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
   git clone <url-do-repositorio>
   cd Enquetinha
   ```

2. Instale as dependências e crie o ambiente virtual automaticamente:

   ```bash
   uv sync
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
uv run main.py
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

Preencha a pergunta e as opções desejadas (mínimo 2, máximo 5). O bot enviará uma mensagem com um botão para cada opção — basta clicar para votar.

## Estrutura do projeto

```text
Enquetinha/
├── main.py                  # Inicialização do bot e carregamento das extensões
├── src/
│   └── commands/
│       └── poll.py          # Slash command /poll e lógica de votação
├── pyproject.toml           # Dependências do projeto
├── uv.lock                  # Versões travadas das dependências
├── .python-version          # Versão do Python utilizada
└── .env                     # Variáveis de ambiente (não versionado)
```

## Limitações conhecidas

- Os votos são armazenados apenas em memória: caso o bot seja reiniciado, os dados de enquetes em andamento são perdidos.
- Não há um mecanismo de encerramento automático ou manual das enquetes.

Essas limitações já estão mapeadas e sendo avaliadas para futuras atualizações. Veja a seção [Próximos passos](#próximos-passos).

## Próximos passos

- [ ] Persistência dos votos (ex: SQLite), evitando perda de dados em caso de reinício do bot
- [ ] Encerramento automático de enquetes por tempo (`timeout` na View)
- [ ] Comando para encerramento manual da enquete
- [ ] Views persistentes, para que botões de enquetes antigas continuem funcionando após reinícios do bot