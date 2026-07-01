#!/usr/bin/env python3
"""
Script de TESTE para verificar se o disparo está funcionando
Envia uma notificação de teste IMEDIATAMENTE
"""

import urllib.request
import urllib.error
import json
import datetime

# ============================================================
# CREDENCIAIS - VERIFIQUE ESTES VALORES
# ============================================================
from config import APP_ID, API_KEY


def log(mensagem):
    agora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    linha = f"[{agora}] {mensagem}"
    print(linha)


def enviar_teste():
    """Envia uma notificação de teste"""
    log("=" * 60)
    log("🧪 TESTE DE DISPARO - Rei das Castanhas")
    log("=" * 60)
    log(f"Data/Hora: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    log(f"App ID: {APP_ID}")
    log(f"API Key: {API_KEY[:20]}...{API_KEY[-10:]}")
    log("")

    url = "https://onesignal.com/api/v1/notifications"
    payload = {
        "app_id": APP_ID,
        "included_segments": ["All"],
        "headings": {"pt": "🧪 Teste de Disparo", "en": "📲 Test Push"},
        "contents": {
            "pt": "Se você recebeu esta notificação, o bot está funcionando! ✅",
            "en": "If you received this notification, the bot is working! ✅"
        },
    }

    log("📤 Enviando notificação de teste para OneSignal...")
    log(f"   URL: {url}")
    log(f"   Payload: {json.dumps(payload, ensure_ascii=False, indent=2)}")
    log("")

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data)
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Basic {API_KEY}")

    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            resultado = json.loads(response.read().decode("utf-8"))
            
            log("=" * 60)
            log("✅ SUCESSO!")
            log("=" * 60)
            log(f"Notificação ID: {resultado.get('id', 'N/A')}")
            log(f"Destinatários: {resultado.get('recipients', 0)}")
            log("")
            log("🎉 O bot ESTÁ FUNCIONANDO!")
            log("As notificações programadas deverão ser enviadas nos horários configurados.")
            log("")
            return True

    except urllib.error.HTTPError as e:
        erro_msg = e.read().decode('utf-8')
        log("=" * 60)
        log("❌ ERRO NA AUTENTICAÇÃO")
        log("=" * 60)
        log(f"Código HTTP: {e.code}")
        log(f"Mensagem de erro:")
        log(f"{erro_msg}")
        log("")
        log("🔧 POSSÍVEIS SOLUÇÕES:")
        log("   1. APP_ID está correto?")
        log("   2. API_KEY está válida e não expirou?")
        log("   3. A chave deve começar com 'os_v2_app_'")
        log("")
        log("📌 Verifique em: https://app.onesignal.com/")
        return False

    except urllib.error.URLError as e:
        log("=" * 60)
        log("❌ ERRO DE CONEXÃO")
        log("=" * 60)
        log(f"Erro: {str(e)}")
        log("")
        log("🔧 POSSÍVEIS SOLUÇÕES:")
        log("   1. Sua internet está funcionando?")
        log("   2. O firewall está bloqueando acesso a onesignal.com?")
        log("   3. Tente acessar https://onesignal.com no navegador")
        return False

    except Exception as e:
        log("=" * 60)
        log("❌ ERRO INESPERADO")
        log("=" * 60)
        log(f"Erro: {str(e)}")
        return False


if __name__ == "__main__":
    try:
        sucesso = enviar_teste()
        if sucesso:
            log("\n✅ Teste concluído com SUCESSO!")
        else:
            log("\n❌ Teste FALHOU - Revise os dados acima")
    except KeyboardInterrupt:
        log("\n⏹️ Teste cancelado.")
    except Exception as e:
        log(f"\n❌ Erro fatal: {str(e)}")
