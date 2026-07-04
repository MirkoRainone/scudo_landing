import os
import httpx
from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, EmailStr

# 1. Creiamo il router per le API con un prefisso dedicato
router = APIRouter(prefix="/api/v1", tags=["Waitlist API"])

# Configurazione variabili Supabase
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
WAITLIST_ENDPOINT = f"{SUPABASE_URL}/rest/v1/waitlist" if SUPABASE_URL else ""

# Lo schema di controllo Pydantic
class IscrizioneForm(BaseModel):
    email: EmailStr

# 2. La rotta per gestire il form (l'indirizzo completo sarà /api/v1/iscriviti)
@router.post("/iscriviti", response_class=HTMLResponse)
async def gestisci_iscrizione(email: str = Form(...)):
    try:
        # Validazione Pydantic
        dati_validati = IscrizioneForm(email=email)
        
        if not SUPABASE_URL or not SUPABASE_KEY:
            return HTMLResponse("Errore: Variabili Supabase mancanti nel .env", status_code=500)
            
        headers_supabase = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json"
        }
        
        # Invio a Supabase (manteniamo per ora la tua logica originale)
        async with httpx.AsyncClient() as client:
            risposta = await client.post(
                WAITLIST_ENDPOINT,
                json={"cliente_email": dati_validati.email},
                headers=headers_supabase
            )
            
            if risposta.status_code >= 400:
                print(f"Errore Supabase: {risposta.text}")
                return HTMLResponse("<h3>Errore interno al database.</h3>", status_code=500)

        # Risposta di successo
        return HTMLResponse("""
        <html><body style='background:#f8fafc; color:#0f172a; text-align:center; padding:100px; font-family:sans-serif;'>
            <div style='max-width:500px; margin:0 auto; background:white; padding:40px; border-radius:16px; border:1px solid #e2e8f0;'>
                <h2 style='color:#10b981;'>🎉 Iscrizione confermata!</h2>
                <p style='color:#64748b;'>A breve implementeremo l'invio della tua API Key via mail.</p>
                <a href='/' style='background:#e11d48; color:white; padding:12px 24px; text-decoration:none; border-radius:8px; display:inline-block; margin-top:20px; font-weight:bold;'>Torna alla Home</a>
            </div>
        </body></html>
        """)

    except Exception as e:
        print(f"Errore: {e}")
        return HTMLResponse("<h3>Errore: Indirizzo email non valido. 🛡️</h3>", status_code=400)