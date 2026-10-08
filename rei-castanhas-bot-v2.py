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
# CALENDARIO SEMANAL — VITRINE DO SITE (com links)
# 1 disparo por dia | 7 disparos por semana
# Cada push abre a pagina do produto/categoria no site ao ser tocado
# dia: 0=Segunda, 1=Terca, 2=Quarta, 3=Quinta, 4=Sexta, 5=Sabado, 6=Domingo
# ============================================================
SITE = "https://www.reidascastanhas.com.br"

def utm(caminho, campanha):
    return f"{SITE}/{caminho}?utm_source=push&utm_medium=onesignal&utm_campaign={campanha}"

CALENDARIO = [

    # SEGUNDA 08:00 — Castanha do Para Premium
    {
        "dia": 0,
        "horario": "08:00",
        "titulo": "🌰 Castanha do Para Premium!",
        "mensagem": "Comece a semana com o alimento mais rico em SELENIO do mundo! Nossa Castanha do Para media inteira e selecionada a dedo. 1 por dia ja faz diferenca. Toque e confira 👉",
        "link": utm("castanha-do-para-media-inteirapremium-rei-das-castanhas", "castanha_para")
    },

    # TERCA 08:00 — Mix Premium Nuts 1kg
    {
        "dia": 1,
        "horario": "08:00",
        "titulo": "🥜 Mix Premium Nuts 1kg",
        "mensagem": "Caju + Para + Amendoas + Nozes + Goji Berry + Uva Passa + Amendoim. TUDO num pacote so! Lanche saudavel pra semana inteira, no trabalho ou na academia. Toque e garanta o seu 👉",
        "link": utm("mix-premium-nuts-1kg-castanha-de-caju-castanha-do-para-amendoas-nozes-goji-berry-uva-passas-e-amendoim-2026-05-13-10-39-24", "mix_nuts")
    },

    # QUARTA 08:30 — Chas
    {
        "dia": 2,
        "horario": "08:30",
        "titulo": "🍵 Quarta do Cha!",
        "mensagem": "Detox, calmante, digestivo ou termogenico? Temos o cha certo pra cada momento do seu dia. Natural, sem conservantes e cheio de sabor. Toque e escolha o seu 👉",
        "link": utm("chas", "chas")
    },

    # QUINTA 08:00 — Graos e Sementes
    {
        "dia": 3,
        "horario": "08:00",
        "titulo": "🌱 Graos e Sementes",
        "mensagem": "Chia, linhaca, quinoa, aveia, gergelim... Pequenos no tamanho, GIGANTES em nutrientes! Fibra, omega-3 e proteina vegetal pra turbinar suas refeicoes. Toque e confira 👉",
        "link": utm("graos-e-sementes", "graos_sementes")
    },

    # SEXTA 08:00 — Amendoa com chocolate (sextou)
    {
        "dia": 4,
        "horario": "08:00",
        "titulo": "🍫 Sextou com Amendoa e Chocolate!",
        "mensagem": "Merece um docinho? Amendoa Premium coberta com chocolate: crocante, intensa e irresistivel. O mimo perfeito pro fim de semana, sem culpa! Toque e peca a sua 👉",
        "link": utm("amendoa-com-chocolate-premium-rei-das-castanhas", "amendoa_chocolate")
    },

    # SABADO 09:30 — Frutas Secas
    {
        "dia": 5,
        "horario": "09:30",
        "titulo": "🍑 Frutas Secas Importadas",
        "mensagem": "Damasco turco, figo turco, ameixa, banana passa, cupuacu... Doce natural da fruta, rico em fibras e energia. Perfeito pro cafe da manha de sabado! Toque e veja todas 👉",
        "link": utm("frutas-secas", "frutas_secas")
    },

    # DOMINGO 09:00 — Ofertas (Baixou)
    {
        "dia": 6,
        "horario": "09:00",
        "titulo": "🔥 BAIXOU! Ofertas da Semana",
        "mensagem": "Domingo e dia de abastecer a despensa! Separamos produtos com PRECO REDUZIDO no site. Castanhas, frutas secas, graos e muito mais. Corre que e por tempo limitado! 👉",
        "link": utm("baixou", "baixou")
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

def enviar_notificacao(titulo, mensagem, link=None):
    url = "https://onesignal.com/api/v1/notifications"
    payload = {
        "app_id": APP_ID,
        "included_segments": ["All"],
        "headings": {"pt": titulo, "en": titulo},
        "contents": {"pt": mensagem, "en": mensagem},
    }
    if link:
        payload["url"] = link  # ao tocar no push, abre a pagina do site
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
                    if enviar_notificacao(item["titulo"], item["mensagem"], item.get("link")):
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
