from pathlib import Path
import datetime
import re
import webbrowser

LOG_PATH = Path("rei-castanhas-log.txt")
OUTPUT_PATH = Path("status_dashboard.html")

CALENDARIO = [
    {
        "dia": 0,
        "horario": "13:00",
        "titulo": "🥗 Dica da tarde",
        "mensagem": "Quer turbinar sua salada? Acrescente nozes ou castanhas picadas por cima! Elas adicionam crocância, proteína e gorduras boas que aumentam a absorção de vitaminas dos vegetais. Experimente hoje! 🥗",
    },
    {
        "dia": 1,
        "horario": "16:00",
        "titulo": "🥭 Lanche da tarde",
        "mensagem": "Hoje às 16h: um lanche tropical com mix de castanhas, frutas secas e pedacinhos de coco. Energético, saboroso e perfeito para a tarde! 🥭",
    },
    {
        "dia": 2,
        "horario": "08:00",
        "titulo": "☕ Bom dia! Dica de hoje",
        "mensagem": "Comece a quarta com energia! Chá de gengibre com mel aquece o corpo, melhora a digestão e fortalece a imunidade. Adicione um punhado de castanhas ao café da manhã para uma dose extra de disposição! 🌰",
    },
    {
        "dia": 4,
        "horario": "08:00",
        "titulo": "🎉 Sexta! Comemore com saúde",
        "mensagem": "Sexta-feira merece um café da manhã especial! Iogurte natural + granola + frutas secas + castanhas = o bowl perfeito para começar o fim de semana com disposição. Fácil, rápido e nutritivo! 🥣",
    },
    {
        "dia": 5,
        "horario": "13:00",
        "titulo": "🌿 Sabadou com saúde!",
        "mensagem": "Petisco de sábado sem culpa: tábua com castanhas variadas, frutas secas, amêndoas e nozes. Combina com reunião com amigos, filme em casa ou tarde em família. Natural, gostoso e cheio de nutrientes! 🧺",
    },
]

DATAS_ESPECIAIS = {
    "12/06": {
        "titulo": "💚 Dia dos Namorados",
        "mensagem": "Presentes que fazem bem! Kit especial de castanhas premium — natural, saudável e delicioso. A melhor forma de cuidar de quem você ama 💑",
    },
    "25/12": {
        "titulo": "🎄 Feliz Natal!",
        "mensagem": "O Rei das Castanhas deseja um Natal repleto de saúde, alegria e sabor! Aproveite nossas cestas natalinas especiais 🌰🎁",
    },
    "01/01": {
        "titulo": "🎆 Feliz Ano Novo!",
        "mensagem": "Que este ano seja repleto de saúde e bem-estar! Comece com o pé direito — com produtos naturais do Rei das Castanhas 👑",
    },
    "12/10": {
        "titulo": "🎈 Dia das Crianças",
        "mensagem": "Petisco saudável para a criançada! Mix de frutas secas e castanhas — nutritivo, colorido e gostoso. Crianças adoram! 👧👦",
    },
}

DIA_NOME = {0: "Segunda", 1: "Terça", 2: "Quarta", 3: "Quinta", 4: "Sexta", 5: "Sábado", 6: "Domingo"}


def parse_sent_titles():
    sent = set()
    if not LOG_PATH.exists():
        return sent
    last_title = None
    with LOG_PATH.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if "Disparando:" in line:
                parts = line.split("Disparando:", 1)
                if len(parts) > 1:
                    last_title = parts[1].strip()
            elif "Enviado!" in line and last_title:
                sent.add(last_title)
                last_title = None
    return sent


def build_today_status():
    hoje = datetime.date.today()
    agora = datetime.datetime.now()
    sent_titles = parse_sent_titles()
    status_items = []

    for item in CALENDARIO:
        if item["dia"] == hoje.weekday():
            status_items.append(item)

    today_key = hoje.strftime("%d/%m")
    if today_key in DATAS_ESPECIAIS:
        special = DATAS_ESPECIAIS[today_key].copy()
        special["dia"] = hoje.weekday()
        special["horario"] = "09:00"
        status_items.insert(0, special)

    result = []
    for item in status_items:
        scheduled_time = datetime.datetime.strptime(item["horario"], "%H:%M").time()
        scheduled_dt = datetime.datetime.combine(hoje, scheduled_time)
        title = item["titulo"]
        if title in sent_titles:
            status = "Enviado"
            badge = "success"
        elif agora <= scheduled_dt:
            status = "Pendente"
            badge = "warning"
        else:
            status = "Atrasado"
            badge = "danger"
        result.append(
            {
                "data": hoje.strftime("%d/%m/%Y"),
                "dia": DIA_NOME[item["dia"]],
                "horario": item["horario"],
                "titulo": title,
                "status": status,
                "badge": badge,
            }
        )
    return result


def build_upcoming_schedule(days=7):
    hoje = datetime.date.today()
    sent_titles = parse_sent_titles()
    events = []

    for delta in range(days):
        target = hoje + datetime.timedelta(days=delta)
        weekday = target.weekday()
        for item in CALENDARIO:
            if item["dia"] == weekday:
                title = item["titulo"]
                if delta == 0:
                    continue
                events.append(
                    {
                        "data": target.strftime("%d/%m/%Y"),
                        "dia": DIA_NOME[weekday],
                        "horario": item["horario"],
                        "titulo": title,
                        "status": "Agendado",
                        "badge": "info",
                    }
                )
        key = target.strftime("%d/%m")
        if key in DATAS_ESPECIAIS:
            title = DATAS_ESPECIAIS[key]["titulo"]
            events.insert(0, {
                "data": target.strftime("%d/%m/%Y"),
                "dia": DIA_NOME[weekday],
                "horario": "09:00",
                "titulo": title,
                "status": "Agendado",
                "badge": "info",
            })
    return events


def render_html(today_items, upcoming_items):
    updated = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    log_path = LOG_PATH.resolve()
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Status Disparador de PUSH APK</title>
<style>
body {{ font-family: Arial, sans-serif; background: #fafafa; color: #222; margin: 0; padding: 0; }}
.container {{ max-width: 980px; margin: 20px auto; padding: 20px; background: #fff; box-shadow: 0 0 18px rgba(0,0,0,.08); border-radius: 12px; }}
h1 {{ margin-top: 0; }}
.table {{ width: 100%; border-collapse: collapse; margin-top: 18px; }}
.table th, .table td {{ padding: 12px 10px; border-bottom: 1px solid #eee; text-align: left; }}
.table th {{ background: #f5f5f5; color: #333; }}
.badge {{ display: inline-block; padding: 4px 10px; border-radius: 999px; color: #fff; font-size: 0.9em; }}
.badge.success {{ background: #2d9c59; }}
.badge.warning {{ background: #f2994a; }}
.badge.danger {{ background: #eb5757; }}
.badge.info {{ background: #2f80ed; }}
.note {{ font-size: 0.95em; color: #555; margin-top: 10px; }}
.button {{ display: inline-block; margin-top: 16px; padding: 10px 16px; background: #2f80ed; color: #fff; text-decoration: none; border-radius: 8px; }}
</style>
</head>
<body>
<div class="container">
<h1>Status do Bot Disparador de PUSH APK</h1>
<p class="note">Última atualização: {updated}</p>
<p class="note">Arquivo de log: {log_path}</p>
<a class="button" href="javascript:location.reload();">Atualizar</a>
<h2>Envios de hoje</h2>
{render_table(today_items)}
<h2>Próximos envios</h2>
{render_table(upcoming_items)}
</div>
</body>
</html>"""
    return html


def render_table(items):
    if not items:
        return '<p class="note">Nenhum envio agendado para hoje.</p>'
    rows = [
        "<table class='table'><thead><tr><th>Data</th><th>Dia</th><th>Horário</th><th>Título</th><th>Status</th></tr></thead><tbody>"
    ]
    for item in items:
        rows.append(
            f"<tr><td>{item['data']}</td><td>{item['dia']}</td><td>{item['horario']}</td><td>{item['titulo']}</td><td><span class='badge {item['badge']}'>{item['status']}</span></td></tr>"
        )
    rows.append("</tbody></table>")
    return "\n".join(rows)


def main():
    today_items = build_today_status()
    upcoming_items = build_upcoming_schedule(days=7)
    html = render_html(today_items, upcoming_items)
    OUTPUT_PATH.write_text(html, encoding="utf-8")
    print(f"Painel gerado em: {OUTPUT_PATH.resolve()}")
    webbrowser.open(f"file://{OUTPUT_PATH.resolve()}")


if __name__ == "__main__":
    main()
