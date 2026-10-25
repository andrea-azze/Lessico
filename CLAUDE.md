# Lessico — istruzioni per Claude Code

Questo file spiega com'è fatta l'app e come lavorare con Andrea (il proprietario). Leggilo per intero prima di toccare qualcosa.
Storico delle versioni precedenti: `docs/riassunto-sessione-precedente.md`.

## Come lavorare con Andrea
- Parla in **italiano**, semplice, senza gergo tecnico non necessario. Andrea non è uno sviluppatore: spiega cosa hai cambiato in poche righe.
- Fai le modifiche direttamente nel repository, **committa e fai push su `main`**: GitHub Pages ripubblica da solo in 1-2 minuti. Non chiedergli di caricare file a mano.
- Una modifica alla volta; se ti chiede più cose, falle in commit separati con messaggi chiari in italiano.
- Prima di dire "fatto", **provala** (vedi "Come testare").
- Nel messaggio finale ricorda sempre le cose che deve fare lui sul telefono, se ce ne sono (es. rifare l'icona dalla Home, vedi sotto).
- Il design/stile verrà rivisto più avanti: non cambiarlo senza che lo chieda.

## Cos'è
**Lessico**: app personale per allenare il vocabolario italiano ↔ inglese, pensata per iPhone (Safari / app web dalla Home). Mostra una parola, rispondi scrivendo o **a voce**, l'app corregge.

- App online: https://andrea-azze.github.io/Lessico/
- Repository: https://github.com/andrea-azze/Lessico (pubblico), account `andrea-azze`
- Hosting: **GitHub Pages**, servito dalla radice del ramo `main`. Nessun build, nessun server, nessun database.
- Decisione presa: **niente Vercel/Supabase** per ora. Si valuta solo se un giorno servirà sincronizzare i progressi su più dispositivi. Il microfono funziona solo su `https` vero aperto in Safari (non dentro l'app Claude né da file locale), quindi non spostare l'app altrove senza `https`.

## Struttura del repository
```
index.html              TUTTA l'app: HTML + CSS + JS + le 2.551 parole (array WORDS)
manifest.webmanifest    nome, colori e icone per "Aggiungi alla Home"
icons/                  apple-touch-icon.png (180), icon-192.png, icon-512.png
tools/make_icons.py     rigenera le icone (Pillow): libro con bandiera inglese
docs/                   documentazione storica
CLAUDE.md               questo file
```
Regola: l'app resta **un solo `index.html`** senza dipendenze. Unica risorsa esterna: due font Google Fonts (se mancano vale il font di sistema). Il file si chiama esattamente `index.html`.

## Vocabolario (`WORDS` in index.html, riga unica molto lunga)
2.551 voci: A2 1.068 · B1 1.054 · Business 633 · Automotive 191 (Business e Automotive si sovrappongono ad A2/B1).
Formato: `["italiano","inglese","livello","sottocategoria","dominio","livello_dominio"]`
- livello `A2`/`B1`; sottocategoria `V` verbi, `N` nomi, `J` aggettivi, `X` extra (locuzioni, frasi); dominio `BUS`/`AUT`/vuoto.
- più traduzioni giuste separate da `/` (es. `"do/make"`), tutte accettate.
- il testo tra parentesi distingue i significati (`sentire (udire)`) ed è ignorato nella correzione.
- L'identità di una parola (chiave di salvataggio) è `italiano|prima traduzione inglese`. **Se cambi quei due campi di una parola esistente, Andrea perde stelle/cancellazioni su di essa**: avvisalo o evitalo.
- Per modificare l'array usa uno script (la riga è enorme): non rigenerarla a mano.

## Funzioni dell'app
- **Home**: categoria scelta, pulsante Inizia. **Barra**: menu, categoria, direzione IT→EN / EN→IT.
- **Allenamento**: parola, campo risposta, **Correggi**, **Avanti**, **Salva** (stella), **Cancella**, **Rispondi a voce**.
- **Menu**: Tutte; tendine A2, B1, Business, Automotive (con "Tutto…" e sottocategorie); **★ Salvate** (le parole importanti da ripassare più spesso); "Recupera parole cancellate"; sezione **Dati** con **Esporta** e **Importa**.
- **Salva**: segna la parola come importante (nel codice è `starred`, chiave di stato `star`, categoria `STAR`; nell'interfaccia si chiama "Salvata/Salvate" — in passato "Ricorda"). Le salvate restano anche nelle categorie normali.
- **Cancella**: la parola va nell'elenco delle cancellate (`deleted`), non esce più nei mazzi, si recupera da "Recupera parole cancellate" (una per una, per gruppo, tutte). Toast "Annulla" dopo ogni azione.
- **Correzione** (`norm`, `judge`): ignora maiuscole, accenti, punteggiatura, articoli, "to" davanti ai verbi, testo tra parentesi; accetta sinonimi anche di altre voci con lo stesso termine; un errore di una lettera su parole ≥5 lettere vale "giusto, occhio all'ortografia". "Correggi" a campo vuoto mostra la soluzione (da ripassare); "Avanti" senza correggere conta come saputa.
- Tema chiaro/scuro automatico.

### Voce
Riconoscimento vocale del browser (`SpeechRecognition`); ascolta in inglese per IT→EN e in italiano per EN→IT. Prima di ascoltare apre il microfono "pieno" (`getUserMedia`): **ora funziona anche con le cuffie Bluetooth** (verificato da Andrea), non toccare quella parte.
- Risposta giusta → verde, poi passa da sola alla successiva dopo ~1,5 s. Sbagliata → rosso con la soluzione.
- **«ok»** (okay, avanti, next, vai): avanti. 
- **«cancella»** (anche delete, elimina, togli, remove e varianti sentite male come "cancel a", "can sell a"): cancella la parola.
- **«salva»** (anche save, ricorda, remember, segna e varianti come "silva"): aggiunge a Salvate, non la toglie mai; si resta sulla parola, poi «ok».
- I comandi si capiscono in italiano e inglese in entrambe le direzioni (`isDel`, `isSave`, `isOk`). Se il microfono sente male un comando, aggiungi la variante lì. Un comando non scatta se la frase è una risposta giusta alla parola (es. «save» per "salvare").
- Tiene lo schermo acceso mentre ascolta (Wake Lock).

### Dati: Esporta / Importa
- **Esporta**: file `lessico-dati-AAAA-MM-GG.json` (su iPhone si apre il foglio di condivisione per salvarlo in File; altrove scarica). Contenuto: `{app:"lessico", version:1, exportedAt, deleted:[chiavi], star:[chiavi], dir, cat}`.
- **Importa**: sceglie un file; **unisce** (non toglie nulla di ciò che c'è già), ignora chiavi sconosciute, ripristina direzione e categoria, mostra quante parole importate e permette "Annulla". Rifiuta file che non sono di Lessico.
- Serve perché l'**app web sulla Home ha una memoria separata da Safari**, e rifare l'icona cancella quella dell'icona vecchia.

### Salvataggio
`localStorage`, chiave `lessico.v1` (`{deleted, star, dir, cat, t}`). Esiste anche un ramo per quando l'app gira come artefatto Claude (`window.claude` db): sul sito normale è inattivo, lascialo.

## Icona e installazione su iPhone
`index.html` punta a `icons/apple-touch-icon.png` (180×180) e al manifest. iPhone legge l'icona **solo quando si aggiunge l'app alla Home**: se la cambi, Andrea deve **esportare i dati dall'icona vecchia → eliminarla → Safari → Condividi → Aggiungi alla schermata Home (interruttore "Apri come app web" attivo) → Importare i dati**. Ricordaglielo ogni volta che tocchi icona, nome o manifest. Per cambiare l'icona modifica `tools/make_icons.py`, rigenera, committa i PNG.
Se Safari mostra ancora la versione vecchia dell'app: chiudere dal multitasking e riaprire (cache).

## Come testare
Nessun build. Verifica:
1. `node --check` sul contenuto dello `<script>` (estrailo in un file temporaneo).
2. Apri `index.html` con Playwright/Chromium e prova le funzioni a mano (`onHeard('salva',true)`, `exportData()`, ecc.). Il microfono vero non si può provare in cloud: dillo ad Andrea e fagli provare sul telefono.
3. Controlla che non ci siano errori in console.

## Accesso di Claude Code al repository (da fare una volta sola)
Andrea vuole dare accesso a **tutti** i suoi repository GitHub in un colpo solo, per non rifare l'operazione a ogni nuovo progetto. I passaggi (verifica le voci sull'interfaccia attuale, i nomi possono cambiare):
1. In Claude Code (web/desktop) collega GitHub dalle impostazioni dei connettori/integrazioni e autorizza l'app GitHub di Claude.
2. Su GitHub apri **Settings → Applications → Installed GitHub Apps** (github.com/settings/installations), scegli l'app di Claude → **Configure**.
3. Alla voce **Repository access** scegli **All repositories** (invece di "Only select repositories") → **Save**. Così anche i repository futuri sono inclusi.
4. Per fare push serve il permesso di scrittura sui contenuti ("Contents: Read and write"); se Claude Code non riesce a pushare, controlla questo permesso nella stessa pagina.
5. In Claude Code, seleziona il repository `andrea-azze/Lessico` e lavora sul ramo `main` (o su un ramo e poi merge, se preferisce rivedere prima).
Se manca l'accesso, dillo ad Andrea in modo semplice e guidalo su questi passaggi; non chiedergli mai password o token in chat.

## Cose aperte / idee
- Provare sul campo i comandi vocali «salva» e «cancella»; annotare le parole che il riconoscimento sbaglia sempre.
- Revisione di stile e disegno (Andrea la farà più avanti).
- Eventuale ampliamento del vocabolario, una categoria alla volta.
- Idea mai realizzata: modalità "mani libere a tempo" che avanza da sola.
- Eventuale sincronizzazione cloud (Vercel + Supabase): solo se Andrea lo chiede.
