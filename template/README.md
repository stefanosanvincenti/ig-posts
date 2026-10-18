# Grafiche Instagram/Facebook — @stefano_sanvincenti_seo

## Regola principale: ogni giorno una grafica DIVERSA
Il feed non deve sembrare fatto con lo stesso stampo. Ogni giorno si sceglie un layout di
`template/layouts/` adatto al contenuto e diverso dai giorni precedenti, con schemi e disegni
(frecce, assi, piramidi, mappe, finte interfacce), non solo titolo + elenco.

Regole di rotazione (controlla `posts/log.csv` prima di scegliere):
- layout del POST: mai uno usato negli ultimi 5 post;
- layout della STORY: mai quello usato ieri;
- palette: mai quella di ieri; alterna sfondi scuri e chiari/colorati (almeno 2 chiari a settimana);
- la story NON è il post rimpicciolito: è una grafica a sé, nata per il 9:16, che anticipa il post.
- dopo la pubblicazione aggiungi una riga a `posts/log.csv`.

Si possono (e devono, ogni tanto) modificare liberamente i layout: spostare blocchi, aggiungere un
disegno SVG pertinente al tema (scudo, lucchetto, grafico, server, lente, documento...), cambiare il
numero di elementi. Un layout nuovo creato per un post si salva in `template/layouts/` con un nome
chiaro e una riga di commento in testa che spiega a cosa serve.

## Layout POST (1080x1350)
| file | cosa è | quando usarlo |
|---|---|---|
| flow.html | schema a processo, 4 nodi con frecce a serpentina | procedure, "come funziona", percorsi |
| versus.html | due colonne Mito/Realtà con VS | sfatare miti, errori vs pratica giusta |
| bigstat.html | numero gigante + grafico a barre + fonte | dati, sanzioni, percentuali (solo dati verificati) |
| matrix.html | matrice 2x2 con punti | priorità, impatto/sforzo, rischio/probabilità |
| timeline.html | linea orizzontale con 4 tappe sopra/sotto | scadenze, piani 30/60/90 giorni |
| pyramid.html | piramide SVG a 4 livelli con note | gerarchie, fondamenta, livelli di difesa |
| chat.html | finta conversazione con un assistente AI e fonti | SEO for AI, come rispondono le AI |
| hub.html | mappa mentale: centro + 6 nodi | "6 fattori", ecosistemi, aree di un audit |
| poster.html | manifesto tipografico + illustrazione | un solo concetto forte, opinioni |
| checklist.html | foglio di quaderno con spunte disegnate | controlli pratici, "prima di..." |
| **network.html** ★ | schema di rete con firewall, VLAN, attacco bloccato, backup air gap | segmentazione, ransomware, zero trust, backup |
| **killchain.html** ★ | catena d'attacco a 6 scalini + scudi dove si spezza | come avviene un attacco, quali controlli NIS2 servono |
| **terminal.html** ★ | console/log di sicurezza con righe evidenziate e callout | SOC, monitoraggio, brute force, MFA, log (NIS2) |
| **anatomy.html** ★ | oggetto "anatomizzato" (es. mail di phishing) con 5 segnali numerati | phishing, frodi IBAN, smishing, red flag |
| **promo-geo.html** ★ | locandina servizio stile campagna: GEO gigante, chat AI in vetro, laptop con grafico, servizi, KPI, CTA sanvincenti.com | promozione di un servizio (GEO, NIS2, SEO tecnica): max 1 ogni 5 post |
| **riskmap.html** ★ | heat map del rischio 5x5 con pin | analisi del rischio NIS2, priorità |

★ = layout "WOW" tecnici. Fino a fine ottobre 2026 hanno la precedenza: almeno 3 post su 5 devono usarne uno.

I file in `template/variants/` sono post già usati: si possono riprendere come base, ma contano
come layout "lista" ai fini della rotazione.

## Layout STORY (1080x1920)
| file | cosa è |
|---|---|
| story-question.html | domanda gigante + freccia + anteprima del post inclinata (usa --img) |
| story-stat.html | un numero enorme preso dal post + contesto |
| story-quiz.html | "Vero o falso?" con due pulsanti disegnati |
| story-peek.html | frase gancio + post "attaccato" con lo scotch + bollino NUOVO (usa --img) |
| **story-alert.html** ★ | schermata d'allarme con triangolo luminoso e testo glitch (cyber/NIS2) |
| **story-promo.html** ★ | coppia di promo-geo: brand, sigla gigante, chat AI con "la tua azienda?", CTA |
| **story-terminal.html** ★ | console a tutto schermo che "digita" la domanda (temi tecnici) |
Zona sicura story: niente testo nei primi 250px e negli ultimi 300px.

## Palette (sostituisci il blocco :root del layout)
| nome | tipo | :root |
|---|---|---|
| notte | scuro | --bg:#0C0818; --ink:#FFFFFF; --dim:#B9B3CC; --a1:#A855F7; --a2:#39E5FF; --line:#241C3A; |
| bosco | scuro | --bg:#08170F; --ink:#FFFFFF; --dim:#AFC7B8; --a1:#FFB020; --a2:#4ADE9C; --line:#1F3B2D; |
| lime | scuro | --bg:#0B1220; --ink:#FFFFFF; --dim:#A9B6CC; --a1:#C6F432; --a2:#FF5A4F; --line:#22314F; |
| oceano | scuro | --bg:#062C30; --ink:#FFFFFF; --dim:#A3C9C7; --a1:#FF8A5B; --a2:#7CF2E2; --line:#0F4549; |
| carta | chiaro | --bg:#F4EFE6; --ink:#16130F; --dim:#5E574C; --a1:#1E6BFF; --a2:#E4572E; --line:#DCD3C3; |
| ghiaccio | chiaro | --bg:#EEF4FA; --ink:#0B1B2E; --dim:#4A5B70; --a1:#0057FF; --a2:#00B3A4; --line:#D3DEEA; |
| lavanda | chiaro | --bg:#F2F0FF; --ink:#141026; --dim:#5D587A; --a1:#5B2EFF; --a2:#FF7A1A; --line:#DEDAF5; |
| giallo | colore | --bg:#FFD23F; --ink:#121212; --dim:#3D3A2E; --a1:#121212; --a2:#6B2BFF; --line:rgba(0,0,0,.15); |
| soc | scuro neon | --bg:#05070A; --ink:#FFFFFF; --dim:#8FA3B8; --a1:#39FF88; --a2:#2FD3FF; --line:#111A24; --bad:#FF3B5C; |
| allarme | scuro rosso | --bg:#0A0A0F; --ink:#FFFFFF; --dim:#9A9AB0; --a1:#FF2E4D; --a2:#3DFFA2; --line:#1C1C28; |
| menta | scuro neon | --bg:#040A09; --ink:#FFFFFF; --dim:#9DB3AC; --a1:#3DFFB8; --a2:#22C99A; --line:#0F2620; |
| corallo | colore | --bg:#FF5A4F; --ink:#1A0B0A; --dim:#4A1D1A; --a1:#FFFFFF; --a2:#1A0B0A; --line:rgba(0,0,0,.18); |
Nei layout chiari alcuni elementi usano #fff per le schede: va bene su carta/ghiaccio/lavanda.

## Render
    python3 template/render.py template/layouts/flow.html posts/AAAA-MM-GG.jpg
    python3 template/render.py template/layouts/story-question.html posts/AAAA-MM-GG-story.jpg --img posts/AAAA-MM-GG.jpg
Lavora su una copia del layout (es. /tmp/oggi.html), non modificare l'originale salvo migliorie.
render.py stampa AVVISO se un testo esce dalla pagina: correggi e rirenderizza. Poi controlla
SEMPRE l'immagine con Read: niente sovrapposizioni, frecce che puntano giuste, testi leggibili.

## Linea editoriale (da metà ottobre 2026)
- Taglio TECNICO e molto grafico: schemi veri (reti, catene d'attacco, log, flussi), dati e riferimenti normativi precisi, non frasi motivazionali.
- Mix: circa 4 post su 5 su NIS2 e cybersecurity (misure di base, incidenti, supply chain, governance, MFA, backup, segmentazione, phishing, log, vulnerabilità, ruoli e responsabilità), 1 su 5 SEO/SEO for AI tecnica.
- Effetto WOW: glow, griglie, icone SVG disegnate a mano nel layout, contrasti forti. Ogni grafica deve sembrare un'infografica fatta da un designer, non un template.

## Contenuti
- Solo fatti verificati; per numeri e date cita la fonte nella grafica o nella caption.
- NIS2: mai parlare di iscrizione nel 2026 con scadenza nel 2027.
- Nei mockup (chat ecc.) niente nomi o loghi di prodotti reali: "Assistente AI", domini di esempio generici.
