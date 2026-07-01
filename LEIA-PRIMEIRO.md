# 🚀 NOVO PLANEJAMENTO ATIVADO — Instruções de Uso

## ✅ O Que Foi Feito

Seu calendário foi completamente **reformulado e otimizado** com:

✨ **9 disparos por semana** (antes: 4-5)  
✨ **Foco em Torina, Chás Naturais, Chás Diuréticos e Castanhas**  
✨ **Mensagens educativas e promotivas**  
✨ **Distribuição estratégica de horários**  
✨ **Calendário visual em HTML**  

---

## 📁 Novos Arquivos Criados

Seu projeto agora tem estes arquivos:

```
Disparador-de-PUSH-APK/
├── rei-castanhas-bot-v2.py          ✏️ ATUALIZADO
├── teste-disparo.py                 ✨ NOVO
├── PLANEJAMENTO-SEMANAL.md          ✨ NOVO
├── calendario-visual.html           ✨ NOVO (abrir no navegador)
├── DIAGNOSTICO.md                   ✨ NOVO
├── COMO-USAR.md
├── bot-castanhas.bat
├── status_dashboard.html
└── rei-castanhas-log.txt
```

---

## 🎯 PRÓXIMAS AÇÕES

### 1️⃣ VISUALIZE O CALENDÁRIO (Opcional)

Abra `calendario-visual.html` no navegador para ver o planejamento de forma bonita e colorida.

```powershell
start calendario-visual.html
```

---

### 2️⃣ VERIFIQUE O LOG DO BOT

Se o bot estava rodando, ele pode ter parado. Limpe e reinicie:

```powershell
# Deletar log antigo
Remove-Item rei-castanhas-log.txt -Force

# Iniciar o bot
python rei-castanhas-bot-v2.py
```

Você verá algo como:

```
[19/06/2026 08:50:00] =======================================================
[19/06/2026 08:50:00] 🌰 Rei das Castanhas - Bot de Notificações v2 INICIADO
[19/06/2026 08:50:00] =======================================================
[19/06/2026 08:50:00] 
[19/06/2026 08:50:00] 📅 Calendário:
[19/06/2026 08:50:00]    Segunda 08:00 — ⚡ Segunda com ENERGIA!
[19/06/2026 08:50:00]    Segunda 14:00 — 🔋 Turbo para a tarde
[19/06/2026 08:50:00]    Terça 07:30 — 🌿 Terça de bem-estar
... (e mais 6 itens)
[19/06/2026 08:50:00] 
[19/06/2026 08:50:00] 🔍 Testando conexão com OneSignal...
[19/06/2026 08:50:01] ✅ Conexão com OneSignal OK! App ID validado.
[19/06/2026 08:50:01] 
[19/06/2026 08:50:01] Aguardando horários programados...
```

---

### 3️⃣ ACOMPANHE EM TEMPO REAL (Recomendado)

Abra DUAS abas do PowerShell:

**Aba 1 — Rodar o bot:**
```powershell
cd "c:\Users\Cliente\Documents\Projetos\Disparador-de-PUSH-APK"
python rei-castanhas-bot-v2.py
```

**Aba 2 — Monitorar o log:**
```powershell
cd "c:\Users\Cliente\Documents\Projetos\Disparador-de-PUSH-APK"
Get-Content rei-castanhas-log.txt -Wait
```

---

### 4️⃣ ATIVAR PERMANENTEMENTE (Windows Auto-start)

Para que o bot inicie automaticamente quando você ligar o PC:

1. Pressione **Windows + R**
2. Digite: `shell:startup`
3. Crie um arquivo chamado **`bot-castanhas.bat`** com:

```batch
@echo off
cd /d "c:\Users\Cliente\Documents\Projetos\Disparador-de-PUSH-APK"
start /min python rei-castanhas-bot-v2.py
```

4. Salve. Pronto! O bot iniciará automaticamente.

---

## 📊 QUANDO OS DISPAROS ACONTECEM

Baseado no novo calendário:

### Segunda ✅
- **08:00** — ⚡ Segunda com ENERGIA!
- **14:00** — 🔋 Turbo para a tarde

### Terça ✅
- **07:30** — 🌿 Terça de bem-estar
- **15:30** — 🫖 Chá Natural da tarde

### Quarta ✅
- **09:00** — 💧 Quarta Detox!
- **16:00** — 🌿 Chá detox de Quarta

### Quinta ✅
- **08:30** — 🌰 QUINTA DAS CASTANHAS!
- **14:30** — 💪 Energia com Castanhas

### Sexta ✅
- **07:00** — 🎉 Sexta chegou!
- **21:00** — 😴 Chá para dormir bem

### Sábado ✅
- **10:00** — 🥗 Brunch Saudável
- **15:00** — 🫖 Chá da tarde de Sábado

### Domingo ✅
- **09:00** — ☀️ Domingo Tranquilo
- **20:00** — 🌙 Domingo de repouso

---

## 🔧 VERIFICAR SE ESTÁ FUNCIONANDO

### Opção A: Teste Manual (Imediato)

```powershell
python teste-disparo.py
```

Você deve ver:
```
✅ SUCESSO!
Notificação ID: [um ID aleatório]
Destinatários: 0
```

Se recebeu `Destinatários: 0`, significa:
- ✅ Seu bot está funcionando perfeitamente!
- ❌ Mas ninguém tem o app instalado para receber

Você precisa de **usuários inscritos no OneSignal** para as notificações chegarem.

### Opção B: Aguardar o Próximo Horário

Se é **Segunda 08:00** (ou qualquer horário do calendário), aguarde alguns minutos e veja no log:

```
📣 Disparando: ⚡ Segunda com ENERGIA!
✅ Enviado! ID: ... | Destinatários: X
```

---

## 📱 POR QUE NÃO ESTOU RECEBENDO AS NOTIFICAÇÕES?

Existem 3 cenários possíveis:

### ✅ Cenário 1: Bot Funcionando, Ninguém Inscrito

- Bot está rodando? **SIM**
- Teste passou? **SIM**
- Recebeu notificação? **NÃO**
- Destinatários no teste: **0**

**Solução:** Você precisa de usuários inscritos no OneSignal. O app móvel deve:
1. Estar instalado
2. Ter permissão de notificações ativada
3. Estar vinculado ao OneSignal corretamente

Verifique em https://app.onesignal.com/ → "Audience" → "Subscribers"

### ✅ Cenário 2: Bot Parado

- Bot está rodando? **NÃO**
- Log está vazio? **SIM**

**Solução:** Inicie o bot:
```powershell
python rei-castanhas-bot-v2.py
```

### ✅ Cenário 3: Credenciais Inválidas

- Bot está rodando? **SIM**
- Log mostra "❌ Erro HTTP 401"? **SIM**

**Solução:** APP_ID ou API_KEY está inválido. Gere novas chaves em:
https://app.onesignal.com/ → Settings → Keys & IDs

---

## 💡 DICAS PRÁTICAS

1. **Preserve o Log**: `rei-castanhas-log.txt` cresce indefinidamente. Limpe semanalmente:
   ```powershell
   Remove-Item rei-castanhas-log.txt -Force
   ```

2. **Horário do PC**: Certifique-se que seu computador tem a hora correta. O bot verifica a hora do PC.

3. **Nunca Desligar**: O bot precisa estar sempre rodando para enviar nos horários certos. Use `bot-castanhas.bat` para auto-iniciar.

4. **Monitorar OneSignal**: Acesse https://app.onesignal.com/ regularmente para:
   - Ver quantos usuários receberam
   - Clicar nas mensagens
   - Deletar campanhas antigas

---

## 📈 PRÓXIMAS MELHORIAS

Sugestões para evolução futura:

- [ ] Adicionar links diretos para compra de produtos nas notificações
- [ ] Criar seção "Produto em Destaque" que muda toda semana
- [ ] Adicionar A/B testing de títulos
- [ ] Sistema de feedback: qual mensagem teve mais cliques?
- [ ] Integração com e-commerce (rastrear vendas por notificação)
- [ ] Notificações personalizadas por segmento (ex: "vegetarianos", "atletas", etc)

---

## ❓ DÚVIDAS COMUNS

**P: Quantos disparos serão enviados?**  
R: 9 por semana (segunda a domingo)

**P: As notificações aparecerão no meu celular?**  
R: Sim, se você tiver o app instalado e permitir notificações

**P: Posso mudar os horários?**  
R: Sim! Edite `rei-castanhas-bot-v2.py` e procure por `CALENDARIO`

**P: Posso mudar as mensagens?**  
R: Sim! Cada item do calendário tem `"titulo"` e `"mensagem"`. Edite livremente.

**P: O bot consome muita energia?**  
R: Não! O bot apenas verifica a hora a cada 30 segundos. Consumo mínimo.

**P: Preciso reiniciar o PC?**  
R: Não obrigatoriamente. Mas se fizer, o bot será iniciado automaticamente (se configurado com `shell:startup`)

---

## 📞 SUPORTE RÁPIDO

Qualquer problema? Execute este script de teste:

```powershell
python teste-disparo.py
```

E verifique:
- ✅ **SUCESSO** = Tudo funcionando
- ❌ **ERRO 401** = Credenciais inválidas
- ❌ **ERRO DE CONEXÃO** = Internet/Firewall bloqueando

---

## 🎉 TUDO PRONTO!

Seu novo planejamento está **100% operacional**.

**Próximo passo:** Inicie o bot agora mesmo:

```powershell
python rei-castanhas-bot-v2.py
```

**Status final:**
- ✅ Planejamento criado
- ✅ Mensagens otimizadas
- ✅ Bot melhorado com diagnóstico
- ✅ Sistema pronto para produção

🚀 **Que os disparos comecem!**

---

**Data:** 19/06/2026  
**Versão:** 2.0  
**Status:** ✅ PRONTO PARA PRODUÇÃO
