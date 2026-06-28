import os
import ssl
import certifi
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, EmailStr
import httpx
from dotenv import load_dotenv
ssl_context = ssl.create_default_context(cafile=certifi.where())
# Carica le variabili d'ambiente dal file .env (Immagine 3)
load_dotenv()

# 1. Importazione corretta del tuo WAF (Immagine 1)
from scudo_waf import WafMiddleware

app = FastAPI()

# 2. La tua API Key di Scudo (Immagine 2)
MOCK_API_KEY_SCUDO = "sk_live_123456789"

# 3. Credenziali Supabase da variabili d'ambiente (Immagine 3)
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Endpoint della tabella waitlist (Assicurati di creare una tabella 'waitlist' su Supabase)
WAITLIST_ENDPOINT = f"{SUPABASE_URL}/rest/v1/waitlist" if SUPABASE_URL else ""

# 🧠 ATTIVAZIONE DOGFOODING (Scudo protegge Scudo usando la tua chiave)
app.add_middleware(WafMiddleware, api_key=MOCK_API_KEY_SCUDO)

class IscrizioneForm(BaseModel):
    email: EmailStr

@app.middleware("http")
async def aggiungi_sicurezza_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains"
    return response

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scudo WAF - Accesso Anticipato</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #0b0f19; color: #f3f4f6; font-family: sans-serif; }
        .hero { padding: 100px 0; text-align: center; }
        .badge-ai { background: linear-gradient(45deg, #3b82f6, #8b5cf6); color: white; padding: 5px 15px; border-radius: 20px; font-size: 0.9rem; }
        .code-box { background-color: #011627; border: 1px solid #1e293b; border-radius: 8px; padding: 20px; font-family: monospace; color: #addb67; text-align: left; }
    </style>
</head>
<body>
    <div class="container py-3 d-flex justify-content-between align-items-center">
        <h3 class="fw-bold text-white m-0">🛡️ Scudo WAF</h3>
        <span class="badge-ai">Protetto da Scudo AI v1.1.2</span>
    </div>
    <div class="container hero">
        <h1 class="display-4 fw-bold text-white mb-3">Il primo WAF con IA che si installa in 2 righe.</h1>
        <p class="lead text-secondary mb-5">Proteggi le tue app Python da SQL Injection, XSS e Prompt Injection. Zero configurazioni cloud complesse.</p>
        <div class="row justify-content-center">
            <div class="col-md-6 bg-dark p-4 rounded border border-secondary text-start">
                <h5 class="text-white mb-3">🚀 Ottieni un mese Pro gratuito al lancio</h5>
                <form action="/iscriviti" method="post">
                    <div class="mb-3">
                        <label class="form-label text-secondary">La tua Email Aziendale</label>
                        <input type="email" name="email" class="form-control bg-transparent text-white border-secondary" required placeholder="tu@azienda.com">
                    </div>
                    <button type="submit" class="btn btn-primary w-100 fw-bold" style="background-color: #3b82f6;">Richiedi Accesso Anticipato</button>
                </form>
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def mostra_landing():
    return HTML_TEMPLATE

@app.post("/iscriviti")
async def gestisci_iscrizione(email: str = Form(...)):
    try:
        dati_validati = IscrizioneForm(email=email)
        if not SUPABASE_URL or not SUPABASE_KEY:
            return HTMLResponse("Errore: Variabili Supabase mancanti. Hai creato il file .env?", status_code=500)
            
        headers_supabase = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient(verify=ssl_context) as client:
            # Salvataggio nella tabella waitlist
            risposta = await client.post(
                WAITLIST_ENDPOINT,
                json={"cliente_email": dati_validati.email},
                headers=headers_supabase
            )
            
            # Se la tabella waitlist non esiste o c'è un errore in Supabase
            if risposta.status_code >= 400:
                print(f"Errore Supabase: {risposta.text}")
                return HTMLResponse(content="<h3>Errore interno: impossibile salvare l'iscrizione.</h3>", status_code=500)

        return HTMLResponse(content="""
        <html><body style='background:#0b0f19; color:white; text-align:center; padding:100px; font-family:sans-serif;'>
        <h2>🎉 Ti sei iscritto con successo!</h2>
        <a href='/' style='color:#3b82f6;'>Torna al sito</a>
        </body></html>
        """)
    except Exception as e:
        print(f"Errore di validazione: {e}")
        return HTMLResponse(content="<h3>Errore: Input non valido. 🛡️</h3>", status_code=400)


