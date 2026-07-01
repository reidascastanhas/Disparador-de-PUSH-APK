# 🔍 Diagnóstico - Disparos Não Estão Sendo Enviados

## O Problema
O bot está rodando, mas as notificações não estão sendo entregues aos usuários.

---

## 🧪 PASSO 1 — Testar a Conexão Imediatamente

Execute o script de teste para verificar se a conexão com OneSignal funciona:

```powershell
python teste-disparo.py
```

### Possíveis resultados:

#### ✅ **SUCESSO** — "Notificação ID: ..."
- A conexão está OK!
- Verifique se você recebeu a notificação no seu aplicativo
- Se recebeu: O bot DEVE estar funcionando nos horários programados
- Se não recebeu: Problema pode estar no aplicativo, não no bot

#### ❌ **ERRO 401/403** — "Autenticação falhou"
- APP_ID ou API_KEY inválido
- **Solução**: Vá em https://app.onesignal.com/ e gere novas chaves

#### ❌ **ERRO DE CONEXÃO** — "Não consegui conectar"
- Sua internet ou firewall está bloqueando OneSignal
- **Solução**: Verifique se consegue acessar onesignal.com no navegador

#### ❌ **Nenhum erro, mas não recebeu a notificação**
- Problema pode estar no aplicativo móvel
- Verifique em OneSignal se "All" subscribers recebeu a mensagem

---

## 🔧 PASSO 2 — Verificar o Log

Veja o arquivo `rei-castanhas-log.txt`:

```powershell
Get-Content rei-castanhas-log.txt -Tail 50
```

Procure por:
- **✅ "Enviado!"** = Disparo funcionou
- **❌ "Erro HTTP"** = Problema de autenticação
- **❌ "Erro de conexão"** = Problema de internet
- **"Aguardando horários"** = Bot rodando, mas ainda não era hora de disparar

---

## 📋 PASSO 3 — Verificar o Calendário

Abra `rei-castanhas-bot-v2.py` e veja:

```python
CALENDARIO = [
    {
        "dia": 0,      # 0=Segunda, 1=Terça, 2=Quarta... 6=Domingo
        "horario": "13:00",
        "titulo": "...",
        "mensagem": "..."
    },
]
```

**O horário de seu computador coincide com um dos horários do calendário?**

Exemplos:
- Se é Segunda-feira 13:00 e tem `"dia": 0, "horario": "13:00"` → Deve disparar agora!
- Se é Terça-feira 15:00, mas não tem nada programado para Terça → Não dispara

---

## 🚀 PASSO 4 — Solução Rápida: Ligar o Bot

Se o teste passou, mas o bot não está enviando:

1. **Limpe o log**:
   ```powershell
   Remove-Item rei-castanhas-log.txt -Force
   ```

2. **Reinicie o bot**:
   ```powershell
   python rei-castanhas-bot-v2.py
   ```

3. **Aguarde o horário do próximo disparo** (confira o calendário)

4. **Acompanhe o log em tempo real**:
   ```powershell
   Get-Content rei-castanhas-log.txt -Wait
   ```

---

## 📱 PASSO 5 — Verificar no OneSignal

Acesse https://app.onesignal.com/

1. Vá para sua App
2. Procure por **"Messages"** ou **"Campaign"**
3. Procure pelos disparos recentes
4. Verifique o status: ✅ Enviado ou ❌ Falhou

---

## 🎯 Checklist de Resolução

- [ ] Executou `python teste-disparo.py`?
- [ ] Recebeu a notificação de teste?
- [ ] Verificou o `rei-castanhas-log.txt`?
- [ ] Confirmou que há itens no calendário para hoje?
- [ ] O bot está rodando agora?
- [ ] Aguardou o próximo horário programado?

---

## 💡 Dicas

- **Bot deve estar sempre rodando** — Use `bot-castanhas.bat` para iniciar na boot
- **Verifique o fuso horário** — O horário do PC está correto?
- **Log cresce muito?** — Delete periodicamente (script pode crescer indefinidamente)
- **Erro 429?** — Muito muitas requisições - OneSignal limitou sua cota

---

## ❌ Ainda não funciona?

Capture a saída do teste e envie o resultado de:

```powershell
python teste-disparo.py
```

Com essa informação, será possível diagnosticar o problema específico.
