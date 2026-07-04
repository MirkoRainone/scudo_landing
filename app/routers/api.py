import os
import httpx
from enum import Enum
from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/api/v1", tags=["Waitlist API"])

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
WAITLIST_ENDPOINT = f"{SUPABASE_URL}/rest/v1/waitlist" if SUPABASE_URL else ""

# 1. Definiamo rigorosamente le uniche due scelte di piano ammesse
class PianoScelto(str, Enum):
    FREE = "free"
    PRO = "pro"

# 2. Aggiorniamo lo schema Pydantic includendo il piano
class IscrizioneForm(BaseModel):
    email: EmailStr
    piano_scelto: PianoScelto

# 3. Aggiorniamo la rotta per ricevere entrambi i parametri dal form HTML
@router.post("/iscriviti", response_class=HTMLResponse)
async def gestisci_iscrizione(
    email: str = Form(...), 
    piano_scelto: str = Form("free") # Default a free se mancasse
):
    try:
        # Validazione Pydantic ultra-sicura
        dati_validati = IscrizioneForm(email=email, piano_scelto=piano_scelto)
        
        if not SUPABASE_URL or not SUPABASE_KEY:
            return HTMLResponse("Errore: Variabili Supabase mancanti nel .env", status_code=500)
            
        headers_supabase = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json"
        }
        
        # Prepariamo il pacchetto dati per Supabase (inclusa la scelta!)
        payload = {
            "cliente_email": dati_validati.email,
            "piano_scelto": dati_validati.piano_scelto.value
        }
        
        async with httpx.AsyncClient() as client:
            risposta = await client.post(
                WAITLIST_ENDPOINT,
                json=payload,
                headers=headers_supabase
            )
            
            if risposta.status_code >= 400:
                print(f"Errore Supabase: {risposta.text}")
                return HTMLResponse("<h3>Errore interno al database.</h3>", status_code=500)

        # Risposta di successo con tema smeraldo
        return HTMLResponse(f"""
        <html><body style='background:#f8fafc; color:#0f172a; text-align:center; padding:100px; font-family:sans-serif;'>
            <div style='max-width:500px; margin:0 auto; background:white; padding:40px; border-radius:16px; border:1px solid #e2e8f0; box-shadow:0 20px 40px -15px rgba(0,0,0,0.05);'>
                <h2 style='color:#10b981; font-weight:800;'>🎉 Iscrizione Confermata!</h2>
                <p style='color:#64748b; margin-top:15px;'>Hai selezionato il <strong>Piano {dati_validati.piano_scelto.value.upper()}</strong>.<br>A breve riceverai la tua API Key e le istruzioni via mail.</p>
                <a href='/' style='background:#10b981; color:white; padding:12px 24px; text-decoration:none; border-radius:8px; display:inline-block; margin-top:20px; font-weight:bold;'>Torna alla Home</a>
            </div>
        </body></html>
        """)

    except Exception as e:
        print(f"Errore di validazione form: {e}")
        return HTMLResponse("<h3>Errore: Indirizzo email non valido o piano scorretto. 🛡️</h3>", status_code=400)