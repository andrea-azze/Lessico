# Lessico — riassunto del progetto

*Documento di passaggio: contiene tutto quello che serve per continuare il lavoro sull'app da un altro account Claude. Da allegare a una chat nuova insieme al file `index.html`.*

---

## 1. Cos'è

**Lessico** è un'app personale per allenare il vocabolario italiano ↔ inglese, pensata per l'iPhone. Mostra una parola, scrivi o dici la traduzione, l'app ti dice se è giusta.

È fatta da **un solo file**: `index.html`. Dentro c'è tutto: le 2.551 parole, la grafica e il funzionamento. Non servono altri file, database o programmi. L'unica cosa esterna sono due caratteri tipografici scaricati da Google Fonts (se mancano, l'app funziona lo stesso con i caratteri di sistema).

---

## 2. Dove si trova

| Cosa | Dove |
|---|---|
| App online | https://andrea-azze.github.io/Lessico/ |
| Repository GitHub | https://github.com/andrea-azze/Lessico (pubblico) |
| Account GitHub | `andrea-azze` |
| File da modificare | `index.html` nel repository |

Il sito è servito da **GitHub Pages**: GitHub prende il file `index.html` del repository e lo pubblica come pagina web, gratis.

**Perché GitHub e non solo Claude:** su iPhone il microfono funziona solo da un indirizzo `https` vero aperto in Safari. Dentro l'app Claude o aprendo il file dall'app File, il riconoscimento vocale non funziona.

---

## 3. Come si aggiorna l'app

1. Ottieni il nuovo `index.html` (da Claude: scheda del file → Condividi → Salva in File).
2. In Safari apri **github.com/andrea-azze/Lessico** e accedi.
3. **Add file → Upload files** → scegli il file. Sostituisce da solo quello vecchio.
4. In fondo alla pagina: **Commit changes**.
5. Dopo 1-2 minuti riapri l'app. Se vedi ancora la versione vecchia, chiudila dal multitasking e riaprila.

Attenzioni:
- Il file deve chiamarsi **esattamente `index.html`**. Se l'iPhone lo salva come "index 2.html", va rinominato prima di caricarlo.
- Nella lista dei repository di GitHub il filtro `contributed-by:@me` può nascondere Lessico: toglierlo o andare direttamente all'indirizzo sopra.
- Non serve riscaricare l'icona sul telefono: punta al sito e si aggiorna da sola.

---

## 4. Installazione sull'iPhone

Safari → apri il sito → **Condividi → Aggiungi alla schermata Home** → interruttore **"Apri come app web" attivo** → Aggiungi.

- Con "app web" attivo si apre a schermo intero e i dati (stelle, parole cancellate) non vengono cancellati se non la usi per giorni.
- L'app web ha una memoria separata da Safari: i progressi fatti in Safari non passano all'icona, e viceversa.

---

## 5. Il vocabolario

**2.551 parole**, divise così:

| Sezione | Parole | Dettaglio |
|---|---|---|
| A2 | 1.068 | Verbi 284 · Nomi 392 · Aggettivi 147 · Extra 245 |
| B1 | 1.054 | Verbi 285 · Nomi 336 · Aggettivi 174 · Extra 259 |
| Business | 633 | A2 116 · B1 517 (incluso lessico di contabilità e contratti) |
| Automotive | 191 | A2 53 · B1 138 (incluso guida autonoma, lidar, omologazione) |

Le sezioni Business e Automotive si sovrappongono ad A2/B1: una parola business di livello B1 compare sia in B1 sia in Business.

**Extra** = locuzioni di tempo, luogo e frasi quotidiane (*entro le sei, tra cinque minuti, in fondo a, a quanto pare, ho fame*).

**Formato di ogni voce nel codice** (array `WORDS`):
`["italiano", "inglese", "livello", "sottocategoria", "dominio", "livello_dominio"]`
- livello: `A2` o `B1`
- sottocategoria: `V` verbi, `N` nomi, `J` aggettivi, `X` extra
- dominio: `BUS`, `AUT` o vuoto
- più traduzioni giuste si separano con `/` (es. `"do/make"`), e sono tutte accettate
- le parentesi servono a distinguere i significati e vengono ignorate nella correzione: `sentire (udire)`, `paese (nazione)`, `borsa (lavoro)`

---

## 6. Cosa fa l'app

**Schermate**
- **Home**: titolo, categoria scelta con il numero di parole, pulsante **Inizia**.
- **Barra in alto**: menu (sinistra), categoria (centro), direzione **IT → EN / EN → IT** (destra).
- **Allenamento**: barra di avanzamento, contatore, punteggio, parola grande, livello e categoria, campo risposta, pulsanti **Correggi**, **Avanti**, **Salva** (stella), **Cancella**. In basso **Rispondi a voce**.
- **Menu**: *Tutte*, poi **tendine apribili e chiudibili** per A2, B1, Business, Automotive (con dentro "Tutto…" e le sottocategorie); la tendina in uso ha il titolo in blu. Poi **★ Salvate** e **Recupera parole cancellate**.
- **Recupera parole**: le parole cancellate divise per sezione e sottocategoria; si recuperano una per una, a gruppi o tutte. Messaggio con "Annulla" dopo ogni cancellazione o recupero.
- Tema chiaro/scuro automatico.

**Correzione**
- Ignora maiuscole, accenti, punteggiatura, articoli (the/a/an, il/lo/la…), "to" davanti ai verbi, testo tra parentesi.
- Accetta tutti i sinonimi, anche quelli presenti in altre voci con lo stesso termine.
- Un errore di una lettera su parole di almeno 5 lettere vale come giusto con l'avviso "occhio all'ortografia".
- **Correggi** a campo vuoto mostra la soluzione e conta la parola come da ripassare.
- **Avanti** senza correggere conta la parola come saputa.

**Voce** (riconoscimento vocale del browser)
- Ascolta in inglese quando la direzione è IT → EN, in italiano quando è EN → IT.
- Risposta giusta: verde, poi passa da sola alla parola dopo.
- Risposta sbagliata: rosso con la soluzione; si dice **"ok"** (o okay, avanti, next, vai) per andare avanti.
- **"cancella"** (anche delete, elimina, togli, remove e varianti sentite male) toglie la parola dal mazzo e la mette tra le cancellate (recuperabili).
- **"salva"** (anche save, ricorda, remember, segna) aggiunge la parola alla categoria **★ Salvate**, senza toglierla mai se è già lì; si resta sulla parola, poi "ok" per andare avanti. I comandi vengono capiti in italiano e in inglese a prescindere dalla direzione.
- Tiene lo schermo acceso durante l'ascolto.
- Prima di ascoltare apre il microfono "pieno", per provare a usare il microfono delle cuffie Bluetooth.

**Salvataggio**: sul telefono (`localStorage`); quando gira come artefatto Claude salva anche una copia lì.

---

## 7. Problemi noti

- **Cuffie Bluetooth**: verificato dall'utente, ora il microfono funziona anche con le cuffie.
- Se il microfono non funziona come app web dalla Home, provare in Safari; se lì funziona, rifare l'icona con "Apri come app web" spento.

---

## 8. Cose ancora aperte

- Provare sul campo i comandi vocali «salva» e «cancella» e segnalare le parole sentite male.
- Usare l'app e annotare cosa togliere o aggiungere.
- Segnalare parole che il riconoscimento vocale sbaglia sempre, per accettare anche la variante sentita.
- Eventuale ampliamento del vocabolario, una categoria alla volta.
- Idea mai realizzata: modalità "mani libere a tempo" che avanza da sola.

---

## 9. Come ripartire nel nuovo account

Apri una chat nuova, allega **`index.html`** e questo documento, e scrivi per esempio:

> "Questa è la mia app Lessico, il riassunto spiega com'è fatta. Voglio continuare a modificarla. Dopo ogni modifica dammi il nuovo index.html da caricare su GitHub."
