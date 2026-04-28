[10:49 p. m., 27/4/2026] Marian: from flask import Flask, render_template_string, request
import requests
import os
import sys

app = Flask(_name_)

# Variables de entorno (obligatorias)
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")

# Si faltan, mostramos error en los logs y salimos
if not PHONE_NUMBER_ID or not ACCESS_TOKEN:
    print("ERROR: Faltan variables de entorno PHONE_NUMBER_ID o ACCESS_TOKEN")
    sys.exit(1)

# Lista de vecinos (solo tu número para prueba)
VECINOS = [
    "5492634613018",
]

HTML = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Timbre Vecinal</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: borde…
[11:07 p. m., 27/4/2026] Marian: from flask import Flask, render_template_string, request
import requests
import os

app = Flask(_name_)

# ==================================================
# DATOS DE WHATSAPP (COMPLETADOS CORRECTAMENTE)
# ==================================================
PHONE_NUMBER_ID = "1129592466895716"
ACCESS_TOKEN = "EAAZBhfdICW3wBRadZCeOQJLk24FLnEmvWYLZArOGT5FilVxnrUwaUOnNtv2APqSMhzzSlAzNX8aGwQ8ZChgKAT5pblcGGyhDbzXmr0MFOo9oPTdeRhEHcdwK1B8onjCszHbSEHCROy4kM9I3BD2IYMnHgdPqVnGTNO0eihu3qwzD0AcyJQFwCCOq92MAvatbZADsH0IU1T3ZAeb49BikZBSiD3zIv0BjMSfw5ZBo7jOUkP4hjCI0Tmx4JdXRT1NcnoUYDinRsgq8eQ5WVUe25wZDZD"

# ==================================================
# LISTA DE VECINOS (SOLO SU NÚMERO PARA PROBAR)
# ==================================================
VECINOS = ["5492634613018"]

# ==================================================
# PÁGINA WEB (HTML, CSS, JS) - SIN ERRORES
# ==================================================
HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Timbre Vecinal</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: linear-gradient(135deg, #075E54 0%, #128C7E 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: system-ui, sans-serif;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 48px;
            padding: 50px 40px;
            text-align: center;
            max-width: 450px;
            width: 100%;
        }
        h1 { color: #075E54; font-size: 32px; margin-bottom: 16px; }
        button {
            background-color: #25D366;
            color: white;
            border: none;
            padding: 22px 30px;
            font-size: 26px;
            font-weight: bold;
            border-radius: 80px;
            width: 100%;
            cursor: pointer;
            margin-top: 20px;
        }
        button:active { transform: scale(0.97); }
        .mensaje { margin-top: 20px; display: none; padding: 10px; border-radius: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔔 ¿ALGUIEN EN LA PUERTA?</h1>
        <button id="btn">📢 DAR AVISO</button>
        <div id="estado" class="mensaje"></div>
    </div>
    <script>
        document.getElementById('btn').onclick = async () => {
            const btn = document.getElementById('btn');
            const estado = document.getElementById('estado');
            btn.disabled = true;
            estado.style.display = 'block';
            estado.style.background = '#FFF3CD';
            estado.style.color = '#856404';
            estado.textContent = 'Enviando aviso...';
            try {
                const r = await fetch('/timbre');
                const d = await r.json();
                estado.textContent = d.mensaje;
                estado.style.background = r.ok ? '#D4EDDA' : '#F8D7DA';
                estado.style.color = r.ok ? '#155724' : '#721C24';
            } catch(e) {
                estado.textContent = 'Error de conexión';
                estado.style.background = '#F8D7DA';
            }
            setTimeout(() => { btn.disabled = false; }, 3000);
        };
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/timbre')
def timbre():
    url = f"https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    mensaje = "🔔 AVISO: Alguien está en la puerta"
    exitosos = 0
    for numero in VECINOS:
        data = {
            "messaging_product": "whatsapp",
            "to": numero,
            "type": "text",
            "text": {"body": mensaje}
        }
        try:
            r = requests.post(url, headers=headers, json=data, timeout=5)
            if r.status_code == 200:
                exitosos += 1
        except Exception as e:
            print(f"Error con {numero}: {e}")
    if exitosos == len(VECINOS):
        return {"mensaje": f"✅ Aviso enviado a {exitosos} vecino"}
    else:
        return {"mensaje": f"⚠️ Enviado a {exitosos} de {len(VECINOS)}"}, 500

# ==================================================
# ESTA LÍNEA ESTÁ CORRECTA: DOS GUIONES BAJOS ANTES Y DESPUÉS DE "name"
# ==================================================
if _name_ == '_main_':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
