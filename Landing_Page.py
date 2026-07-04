import os
import ssl
import certifi
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

# 1. Carichiamo le variabili d'ambiente (.env) e SSL
ssl_context = ssl.create_default_context(cafile=certifi.where())
load_dotenv()

# Importiamo il tuo WAF (Dogfooding!)
from scudo_waf import WafMiddleware

# IMPORTIAMO I NOSTRI DUE ROUTER (I "Maitre")
from app.routers import web, api

# 2. Inizializziamo l'applicazione
app = FastAPI(title="Scudo WAF", version="1.2")

# 3. Rendiamo accessibile la cartella "static" per CSS, Javascript e immagini
app.mount("/static", StaticFiles(directory="static"), name="static")

# 4. DOGFOODING: Aggiungiamo lo scudo WAF di test
MOCK_API_KEY_SCUDO = "sk_live_123456789"
app.add_middleware(WafMiddleware, api_key=MOCK_API_KEY_SCUDO)

# 5. HARDENING: Middleware per gli Header di sicurezza HTTP
@app.middleware("http")
async def aggiungi_sicurezza_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains"
    return response

# 6. ECCO IL VIGILE URBANO: Colleghiamo i due router all'app!
app.include_router(web.router)
app.include_router(api.router)