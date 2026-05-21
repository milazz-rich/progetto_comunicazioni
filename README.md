# Progetto Comunicazioni - Rilevamento Persone

Questa applicazione web, sviluppata con **Python + Dash + OpenCV + YOLO**, serve per **rilevare persone** in tre modalita:

- **Live**: usa la webcam del computer in tempo reale.
- **Video**: analizza un video caricato dall'utente.
- **Immagine**: analizza una singola immagine caricata.

Il modello mostra i box di rilevamento e il conteggio: **"Persone rilevate: N"**.

## Requisiti

- Python 3.10+ (consigliato 3.11/3.12)
- `pip`
- Webcam (solo per modalita Live)

## Installazione (step by step)

1. **Clona il progetto** (oppure scaricalo come ZIP):

```bash
git clone https://github.com/milazz-rich/progetto_comunicazioni.git
cd progetto_comunicazioni
```

2. **Crea un ambiente virtuale**:

```bash
python -m venv .venv
```

3. **Attiva l'ambiente virtuale**:

- Su **Windows (PowerShell)**:

```powershell
.\.venv\Scripts\Activate.ps1
```

- Su **Windows (CMD)**:

```cmd
.venv\Scripts\activate.bat
```

- Su **Linux/Mac**:

```bash
source .venv/bin/activate
```

4. **Installa le dipendenze**:

```bash
pip install -r requirements.txt
```

## Avvio del progetto

1. Assicurati di essere nella cartella del progetto e con ambiente virtuale attivo.
2. Avvia l'app:

```bash
python main.py
```

3. Apri il browser su:

```text
http://127.0.0.1:8050/
```

## Come usare l'app

1. Seleziona la modalita in alto:
   - `Live`
   - `Video`
   - `Immagine`
2. In modalita **Live** parte la lettura webcam e il rilevamento automatico.
3. In modalita **Video** carica un file video e attendi i frame elaborati.
4. In modalita **Immagine** carica una foto per vedere rilevamenti e conteggio.

## Struttura principale

- `main.py`: interfaccia Dash, gestione webcam/upload, rendering risultati.
- `yolo.py`: inferenza YOLO e disegno box + conteggio persone.
- `yolo26n.pt`: peso del modello YOLO usato dall'app.

## Note utili

- Il primo avvio puo richiedere qualche secondo in piu per il caricamento del modello.
- Se la webcam non viene rilevata, verifica che non sia gia usata da un'altra applicazione.
- Se hai problemi con dipendenze pesanti (es. `torch`), aggiorna `pip` e riprova:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```
