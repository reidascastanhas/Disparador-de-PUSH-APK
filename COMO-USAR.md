# Disparador de PUSH APK — Bot de Notificações

## O que o bot faz
Envia push notifications automáticas para seus clientes conforme este calendário:

| Dia | Horário | Mensagem |
|-----|---------|----------|
| Segunda | 08:00 | 🌰 Dica da Semana (educativa) |
| Quarta | 12:00 | 🍵 Receita Fácil |
| Sexta | 19:00 | 🌿 Fim de Semana Saudável |
| Domingo | 10:00 | ☕ Domingo com Saúde |

Além disso envia mensagens especiais em datas como Dia dos Namorados, Natal e Ano Novo.

---

## Como instalar e rodar

### PASSO 1 — Instale o Python
Acesse https://www.python.org/downloads/ e baixe o Python 3.
Na instalação, marque "Add Python to PATH".

### PASSO 2 — Salve o arquivo
Coloque o arquivo rei-castanhas-bot.py em uma pasta, por exemplo:
C:\BotCastanhas\

### PASSO 3 — Rode o bot
Abra o PowerShell, navegue até a pasta e rode:
```
cd C:\BotCastanhas
python rei-castanhas-bot.py
```

### PASSO 4 — Deixe rodando em background
Para rodar sem ficar com a janela aberta, use:
```
start /min python rei-castanhas-bot.py
```

---

## Como rodar automaticamente ao ligar o PC

1. Pressione Windows + R e digite: shell:startup
2. Crie um arquivo chamado "bot-castanhas.bat" com o conteúdo:
   start /min python C:\BotCastanhas\rei-castanhas-bot.py
3. Salve. Agora o bot inicia sozinho quando você ligar o computador!

---

## Como personalizar as mensagens

Abra o arquivo rei-castanhas-bot.py no Bloco de Notas e edite a seção CALENDARIO.
Cada item tem:
- dia: 0=Segunda, 1=Terça, 2=Quarta... 6=Domingo
- horario: "HH:MM"
- titulo: título da notificação
- mensagem: texto completo

---

## Acompanhar o que foi enviado
O bot gera um arquivo rei-castanhas-log.txt na mesma pasta.
Abra ele para ver o histórico de todos os envios.

