import urllib.request
import urllib.error
import json
import datetime
import time
import sys
import os

# Forçar encoding UTF-8 no console do Windows
# Isso evita UnicodeEncodeError com emojis no cp1252
# Quando roda minimizado (startup), stdout pode ser None
if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    os.environ["PYTHONUTF8"] = "1"
    if sys.stdout is None or not hasattr(sys.stdout, "write"):
        sys.stdout = open(os.devnull, "w", encoding="utf-8")
    else:
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    if sys.stderr is None or not hasattr(sys.stderr, "write"):
        sys.stderr = open(os.devnull, "w", encoding="utf-8")
    else:
        try:
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

# ============================================================
# CONFIGURAÇÕES - Disparador de PUSH APK
# ============================================================
from config import APP_ID, API_KEY

# ============================================================
# CALENDARIO SEMANAL — SEMANA DA CASTANHA DO PARA
# 1 disparo por dia | 7 disparos por semana
# dia: 0=Segunda, 1=Terca, 2=Quarta, 3=Quinta, 4=Sexta, 5=Sabado, 6=Domingo
# ============================================================
CALENDARIO = [

    # SEGUNDA 08:00 — Selenio: o mineral da castanha do Para
    {
        "dia": 0,
        "horario": "08:00",
        "titulo": "🇧🇷 Semana da Castanha do Para!",
        "mensagem": "VOCE SABIA? A castanha do Para e o alimento MAIS RICO EM SELENIO do planeta! Apenas 1 unidade por dia ja fornece toda a dose diaria. Selenio protege contra cancer, fortalece a tireoide e combate o envelhecimento! 🌰💚"
    },

    # TERCA 08:00 — Dose certa
    {
        "dia": 1,
        "horario": "08:00",
        "titulo": "🌰 Qual a dose certa?",
        "mensagem": "CASTANHA DO PARA: a dose perfeita e 1 a 3 unidades por dia! Mais que isso pode ser excesso de selenio. Pouca quantidade, MAXIMO beneficio. Come 1 no cafe da manha e pronto! Simples, barato e poderoso! 💪✨"
    },

    # QUARTA 08:30 — Tireoide e saude hormonal
    {
        "dia": 2,
        "horario": "08:30",
        "titulo": "🦋 Castanha do Para e a Tireoide",
        "mensagem": "SUA TIREOIDE PRECISA DE SELENIO! A castanha do Para ajuda a regular hormonios T3 e T4, combate o hipotireoidismo e reduz inflamacao da glandula. 1 castanha por dia = tireoide funcionando bem. Cuide da sua saude hormonal! 🦋🌰"
    },

    # QUINTA 08:00 — Receita da semana
    {
        "dia": 3,
        "horario": "08:00",
        "titulo": "👨‍🍳 Receita: Leite de Castanha do Para!",
        "mensagem": "RECEITA FACIL: Deixe 10 castanhas do Para de molho por 8h. Bata com 500ml de agua. Coe com pano. PRONTO! Leite vegetal cremoso, rico em selenio e gordura boa. Sem lactose, sem conservante. Use em cafe, vitamina ou receitas! 🥛🌰"
    },

    # SEXTA 08:00 — Beleza e pele
    {
        "dia": 4,
        "horario": "08:00",
        "titulo": "✨ Castanha do Para e a Beleza!",
        "mensagem": "PELE BONITA? CASTANHA DO PARA! O selenio combate radicais livres (antienvelhecimento), fortalece unhas e cabelos, e da brilho natural a pele. Melhor que cosmetico caro! 1 castanhinha por dia = beleza de dentro pra fora! 💅🌰✨"
    },

    # SABADO 09:30 — Coracao e colesterol
    {
        "dia": 5,
        "horario": "09:30",
        "titulo": "❤️ Castanha do Para e o Coracao!",
        "mensagem": "CORACAO SAUDAVEL! A castanha do Para tem gorduras insaturadas que REDUZEM o colesterol ruim (LDL) e AUMENTAM o bom (HDL). Estudos mostram efeito em apenas 48h apos o consumo! Cuide do seu coracao com 1 castanha por dia! ❤️🌰"
    },

    # DOMINGO 09:00 — Imunidade e resumo
    {
        "dia": 6,
        "horario": "09:00",
        "titulo": "🛡️ Castanha do Para: Resumo!",
        "mensagem": "RESUMO DA SEMANA: 1 castanha do Para por dia = Selenio (antioxidante) + Tireoide regulada + Pele bonita + Coracao protegido + Imunidade forte. O alimento mais completo da Amazonia! Ja comeu a sua hoje? 🇧🇷🌰👑"
    },
]

# ============================================================
# DATAS ESPECIAIS
# ============================================================
DATAS_ESPECIAIS = {
    "12/06": {
        "titulo": "💚 Dia dos Namorados",
        "mensagem": "Presentes que fazem bem! Kit especial de castanhas premium — natural, saudável e delicioso. A melhor forma de cuidar de quem você ama 💑"
    },
    "25/12": {
        "titulo": "🎄 Feliz Natal!",
        "mensagem": "O Rei das Castanhas deseja um Natal repleto de saúde, alegria e sabor! Aproveite nossas cestas natalinas especiais 🌰🎁"
    },
    "01/01": {
        "titulo": "🎆 Feliz Ano Novo!",
        "mensagem": "Que este ano seja repleto de saúde e bem-estar! Comece com o pé direito — com produtos naturais do Rei das Castanhas 👑"
    },
    "12/10": {
        "titulo": "🎈 Dia das Crianças",
        "mensagem": "Petisco saudável para a criançada! Mix de frutas secas e castanhas — nutritivo, colorido e gostoso. Crianças adoram! 👧👦"
    },
}

# ============================================================
# FUNÇÕES
# ============================================================

def enviar_notificacao(titulo, mensagem):
    url = "https://onesignal.com/api/v1/notifications"
    payload = {
        "app_id": APP_ID,
        "included_segments": ["All"],
        "headings": {"pt": titulo, "en": titulo},
        "contents": {"pt": mensagem, "en": mensagem},
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data)
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Basic {API_KEY}")
    
    log(f"📤 Enviando para OneSignal...")
    
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            result = json.loads(response.read().decode("utf-8"))
            recipients = result.get("recipients", 0)
            notif_id = result.get("id", "N/A")
            log(f"✅ Enviado! ID: {notif_id} | Destinatários: {recipients}")
            return True
    except urllib.error.HTTPError as e:
        erro_msg = e.read().decode('utf-8')
        log(f"❌ Erro HTTP {e.code}: {erro_msg}")
        log(f"⚠️  Verifique: APP_ID e API_KEY são válidos?")
        return False
    except urllib.error.URLError as e:
        log(f"❌ Erro de conexão: {str(e)}")
        log(f"⚠️  Verifique sua conexão com a internet")
        return False
    except Exception as e:
        log(f"❌ Erro inesperado: {str(e)}")
        return False


def log(mensagem):
    agora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    linha = f"[{agora}] {mensagem}"
    try:
        print(linha)
    except (UnicodeEncodeError, OSError):
        # Fallback: remove caracteres que o console não suporta
        try:
            print(linha.encode("ascii", errors="replace").decode("ascii"))
        except Exception:
            pass
    with open("rei-castanhas-log.txt", "a", encoding="utf-8") as f:
        f.write(linha + "\n")


def testar_conexao_onesignal():
    """Verifica se APP_ID e API_KEY sao validos SEM enviar notificacao"""
    log("🔍 Verificando credenciais OneSignal (sem disparar)...")
    url = f"https://onesignal.com/api/v1/apps/{APP_ID}"

    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Basic {API_KEY}")

    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            result = json.loads(response.read().decode("utf-8"))
            nome_app = result.get("name", "N/A")
            players = result.get("players", 0)
            log(f"✅ OneSignal OK! App: {nome_app} | Inscritos: {players}")
            return True
    except urllib.error.HTTPError as e:
        erro = e.read().decode('utf-8')
        log(f"❌ Erro na conexão: HTTP {e.code}")
        log(f"   {erro}")
        return False
    except Exception as e:
        log(f"❌ Erro: {str(e)}")
        return False


def verificar_data_especial():
    hoje = datetime.datetime.now().strftime("%d/%m")
    return DATAS_ESPECIAIS.get(hoje)


def deve_enviar_agora(item):
    agora = datetime.datetime.now()
    return item["dia"] == agora.weekday() and item["horario"] == agora.strftime("%H:%M")


def rodar_bot():
    log("=" * 55)
    log("🌰 Rei das Castanhas - Bot de Notificações v2 INICIADO")
    log("=" * 55)
    log(f"App ID: {APP_ID[:8]}...")
    log(f"Data/Hora atual: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    log("")
    
    # Testar conexão na inicialização (com retry para aguardar internet no boot)
    conexao_ok = False
    for tentativa in range(1, 11):
        if testar_conexao_onesignal():
            conexao_ok = True
            break
        else:
            if tentativa < 10:
                log(f"⏳ Tentativa {tentativa}/10 falhou. Aguardando 30s para internet ficar pronta...")
                time.sleep(30)
            else:
                log("⚠️  10 tentativas falharam. Continuando mesmo assim (tentará enviar nos horários)...")
    
    
    log("")
    log("📅 Calendário:")
    dias = {0: "Segunda", 1: "Terça", 2: "Quarta", 3: "Quinta", 4: "Sexta", 5: "Sábado", 6: "Domingo"}
    for item in CALENDARIO:
        log(f"   {dias[item['dia']]} {item['horario']} — {item['titulo']}")
    log("")
    log("Aguardando horários programados...\n")

    enviados = set()
    tentativas_falhadas = 0

    while True:
        try:
            agora = datetime.datetime.now()
            chave_minuto = agora.strftime("%d/%m/%Y %H:%M")

            # Datas especiais às 09:00
            if agora.strftime("%H:%M") == "09:00":
                chave_esp = f"especial_{agora.strftime('%d/%m')}"
                if chave_esp not in enviados:
                    data_especial = verificar_data_especial()
                    if data_especial:
                        log(f"📅 Data especial detectada: {agora.strftime('%d/%m')}")
                        if enviar_notificacao(data_especial["titulo"], data_especial["mensagem"]):
                            enviados.add(chave_esp)
                        else:
                            tentativas_falhadas += 1

            # Calendário semanal
            for i, item in enumerate(CALENDARIO):
                chave = f"{chave_minuto}_{i}"
                if chave not in enviados and deve_enviar_agora(item):
                    log(f"\n📣 Disparando: {item['titulo']}")
                    if enviar_notificacao(item["titulo"], item["mensagem"]):
                        enviados.add(chave)
                        tentativas_falhadas = 0  # Reset contador
                    else:
                        tentativas_falhadas += 1
                        if tentativas_falhadas >= 3:
                            log("⚠️  3 tentativas falharam. Verifique a conexão!")

            # Reset diário
            if agora.strftime("%H:%M") == "00:01":
                enviados = set()
                log("🔄 Novo dia — controle de envios resetado")

            time.sleep(30)
            
        except Exception as e:
            log(f"❌ Erro na loop principal: {str(e)}")
            time.sleep(30)


if __name__ == "__main__":
    try:
        rodar_bot()
    except KeyboardInterrupt:
        log("\n⏹️ Bot encerrado pelo usuário.")
