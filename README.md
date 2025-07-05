[![Deploy](https://github.com/calangohc/ContribuaCalangoBot/actions/workflows/deploy.yml/badge.svg)](https://github.com/calangohc/ContribuaCalangoBot/actions/workflows/deploy.yml)
[![Lembrete](https://github.com/calangohc/ContribuaCalangoBot/actions/workflows/lembrete.yml/badge.svg)](https://github.com/calangohc/ContribuaCalangoBot/actions/workflows/lembrete.yml)

# [@ContibuaCalangoBot](https://t.me/ContribuaCalangoBot)

Bot do [@CalangoHC](https://t.me/CalangoHC) para que todos possam consultar o saldo bancário de nosso espaço.

## Configuração

Crie um arquivo chamado `calango.conf` com o seguinte conteúdo:

```
[BOT]
TOKEN=158700146:AAHOPReqqTR8V7FXysa8mJCbQACUWSTBog8

[APOIADORES]
ID=-1001278798768

[CALANGOHC]
ID=-1001062144093
```
Sendo:
* `BOT/TOKEN`: O token do bot, obtido falando-se com o [@BotFather](https://t.me/BotFather)
* `APOIADORES/ID`: Grupo das pessoas capazes de alterar o saldo do bot
* `CALANGOHC/ID`: Grupo comum do CalangoHC

Antes de iniciar o bot, verifique se o banco de dados e sua tabela já existem.
```
python criar_tabela.py
```

Para executar o bot, utilize:
```
python bot.py
```

## Contribua

Toda e qualquer contribuição é bem vinda! Issues, PRs ou simples trocas de idéias são excelentes. 

[Participe do grupo no Telegram](https://t.me/CalangoHC).
