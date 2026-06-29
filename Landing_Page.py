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

# 🎨 NUOVA VETRINA SAAS
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scudo WAF - Next-Gen Python Security</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
    <style>
        body { background-color: #0b0f19; color: #f3f4f6; font-family: 'Inter', sans-serif; overflow-x: hidden; }
        .navbar-brand { font-weight: 800; letter-spacing: -0.5px; }
        .badge-ai { background: linear-gradient(45deg, #3b82f6, #8b5cf6); color: white; padding: 6px 16px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);}
        .hero { padding: 80px 0 60px; }
        .text-gradient { background: linear-gradient(45deg, #60a5fa, #c084fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        
        /* Finto Terminale Mac/Linux */
        .terminal-box { background-color: #011627; border: 1px solid #1e293b; border-radius: 12px; box-shadow: 0 15px 35px rgba(0,0,0,0.6); overflow: hidden; }
        .terminal-header { background-color: #1e293b; padding: 12px 15px; display: flex; gap: 8px; align-items: center;}
        .dot { width: 12px; height: 12px; border-radius: 50%; }
        .dot-red { background-color: #ff5f56; }
        .dot-yellow { background-color: #ffbd2e; }
        .dot-green { background-color: #27c93f; }
        .terminal-body { padding: 20px; font-family: 'Courier New', Courier, monospace; font-size: 0.95rem; color: #a6accd; text-align: left; line-height: 1.6;}
        .cmd-prompt::before { content: "root@server:~# "; color: #3b82f6; }
        .cmd-text { color: #addb67; }
        
        /* Card Vantaggi */
        .feature-card { background: rgba(30, 41, 59, 0.4); border: 1px solid #1e293b; border-radius: 12px; padding: 30px; transition: all 0.3s ease; height: 100%;}
        .feature-card:hover { transform: translateY(-5px); border-color: #3b82f6; background: rgba(30, 41, 59, 0.8); }
        .feature-icon { font-size: 2.2rem; color: #60a5fa; margin-bottom: 20px; display: inline-block;}
        
        /* Form e Bottoni */
        .btn-primary-gradient { background: linear-gradient(45deg, #2563eb, #7c3aed); border: none; transition: opacity 0.3s; }
        .btn-primary-gradient:hover { opacity: 0.9; transform: scale(1.02); }
        .input-email:focus { box-shadow: 0 0 0 0.25rem rgba(59, 130, 246, 0.25); border-color: #3b82f6; }
    </style>
</head>
<body>
    <nav class="navbar navbar-dark pt-4 mb-4">
        <div class="container d-flex justify-content-between align-items-center">
            <a class="navbar-brand text-white fs-4" href="#">🛡️ Scudo<span class="text-primary">WAF</span></a>
            <span class="badge-ai">v1.1.2 Online</span>
        </div>
    </nav>

    <div class="container hero">
        <div class="row align-items-center mb-5">
            <div class="col-lg-6 text-start mb-5 mb-lg-0 pe-lg-5">
                <h1 class="display-4 fw-bold text-white mb-4">L'unico WAF AI che si installa in <span class="text-gradient">2 righe di codice.</span></h1>
                <p class="lead text-secondary mb-5">Proteggi le tue app Python da XSS, SQL Injection e attacchi Zero-Day senza impazzire con le regole cloud. L'Intelligenza Artificiale fa il lavoro sporco per te.</p>
                
                <div class="bg-dark p-4 rounded border border-secondary shadow-lg">
                    <h6 class="text-white mb-3 fw-bold">🚀 Mettiti in lista per l'accesso anticipato</h6>
                    <form action="/iscriviti" method="post" class="d-flex flex-column flex-sm-row gap-2">
                        <input type="text" name="email" class="form-control input-email bg-transparent text-white border-secondary" required placeholder="sviluppatore@azienda.com">
                        <button type="submit" class="btn btn-primary-gradient fw-bold px-4 text-white text-nowrap">Richiedi API Key</button>
                    </form>
                </div>
            </div>

            <div class="col-lg-6">
                <div class="terminal-box">
                    <div class="terminal-header">
                        <div class="dot dot-red"></div>
                        <div class="dot dot-yellow"></div>
                        <div class="dot dot-green"></div>
                    </div>
                    <div class="terminal-body">
                        <div class="cmd-prompt"><span class="cmd-text">pip install scudo-waf</span></div>
                        <div class="text-secondary mt-3"># Proteggi la tua app FastAPI all'istante</div>
                        <div><span style="color: #c792ea;">from</span> scudo_waf <span style="color: #c792ea;">import</span> WafMiddleware</div>
                        <div class="mt-2">app.add_middleware(WafMiddleware, api_key=<span style="color: #ecc48d;">"sk_live_83b..."</span>)</div>
                        <br>
                        <div style="color: #82aaff;">[INFO] Inizializzazione Rete Neurale... OK</div>
                        <div style="color: #27c93f;">[SEC] WAF Attivo. I tuoi endpoint sono un bunker.</div>
                    </div>
                </div>
            </div>
        </div>

        <div class="row mt-5 pt-5 text-start g-4 border-top border-secondary">
            <div class="col-md-4">
                <div class="feature-card">
                    <i class="bi bi-robot feature-icon"></i>
                    <h4 class="text-white fw-bold">Motore AI Nativo</h4>
                    <p class="text-secondary mb-0">Dimentica le Regex. Il nostro modello comprende l'intento malevolo del payload, bloccando minacce moderne come la Prompt Injection.</p>
                </div>
            </div>
            <div class="col-md-4">
                <div class="feature-card">
                    <i class="bi bi-lightning-charge feature-icon"></i>
                    <h4 class="text-white fw-bold">Fail-Open Sicuro</h4>
                    <p class="text-secondary mb-0">L'analisi asincrona avviene in millisecondi. Se l'IA va in timeout, il traffico passa: non bloccheremo mai i tuoi clienti reali.</p>
                </div>
            </div>
            <div class="col-md-4">
                <div class="feature-card">
                    <i class="bi bi-shield-check feature-icon"></i>
                    <h4 class="text-white fw-bold">Difesa in Profondità</h4>
                    <p class="text-secondary mb-0">Blocca la spazzatura al cancello. Lascia che Pydantic e le tue logiche di business gestiscano solo il traffico genuino e pulito.</p>
                </div>
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
        <p style='color:#a6accd;'>Ti contatteremo presto con la tua API Key.</p>
        <a href='/' style='color:#3b82f6; text-decoration:none; font-weight:bold;'>Torna alla Home</a>
        </body></html>
        """)
    except Exception as e:
        print(f"Errore di validazione: {e}")
        return HTMLResponse(content="<h3>Errore: Input non valido. 🛡️</h3>", status_code=400)