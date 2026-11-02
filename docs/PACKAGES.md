```xml
<OtusPackageManifest schemaVersion="1" type="language">
    <Id>io.github.samugallo06.otus_lang_it</Id>
    <Name>Italian Language Pack</Name>
    <Version>1.0.0</Version>
    <Description>Pacchetto di traduzioni in italiano per Otus Browser</Description>
    <Authors>
        <Author>Samuele Gallicani</Author>
    </Authors>
    <License>GPL 3.0</License>
    <Meta lang_code="it_IT" />
    <Files>
        <File src="index.html" dest="index.html" sha256="1" /> <!-- IGNORE -->
        <File src="js/app.js" dest="js/app.js" sha256="1" /> <!-- IGNORE -->
        <Directory src="css" dest="css" sha256="1" />
    </Files>
</OtusPackageManifest>
```

## App locali

Un'applicazione HTML può essere installata con `type="app"` e aperta in una
nuova scheda del browser dichiarando `runtime="self"` e un `entrypoint`
relativo alla directory del pacchetto:

```xml
<OtusPackageManifest schemaVersion="1" type="app">
    <Id>io.github.samugallo06.otus_pdf_reader</Id>
    <Name>Otus PDF Reader</Name>
    <Version>1.0.0</Version>
    <Description>Lettore PDF per Otus Browser</Description>
    <Authors>
        <Author>Samuele Gallicani</Author>
    </Authors>
    <License>GPL-3.0</License>
    <Meta runtime="self" entrypoint="index.html" />
    <Files>
        <File src="index.html" dest="index.html" sha256="..." />
    </Files>
</OtusPackageManifest>
```

Il file indicato da `entrypoint` deve essere incluso nel pacchetto e non può
essere un percorso assoluto o contenere `..`. Dopo l'installazione l'app viene
registrata in `apps.xml` e la finestra del gestore pacchetti mostra il pulsante
`Open`.

# Costruire un pacchetto

Per costruire un pacchetto è necessario creare un file `manifest.otus` nella radice della directory del pacchetto. Il file deve essere un documento XML valido e deve contenere gli attributi:

- `schemaVersion`: la versione dello schema del manifesto. Attualmente deve essere `1`.
- `type`: il tipo di pacchetto. Può essere `language` per i pacchetti di lingua o `app` per le applicazioni locali.

```xml
<OtusPackageManifest schemaVersion="1" type="language">
```

Nella lista dei file, è possibile includere file e directory. le directory, per garantire il controllo di integrità, è in formato compresso (gzip) con tar. Nell'attributo `sha256` va indicato l'hash SHA-256 del file o della directory compressa. Per le directory, il file compresso deve avere estensione `.tar.gz`. Esse verranno estratte nella directory di destinazione indicata da `dest` durante l'installazione del pacchetto.

Da notare che sia i file di destinazione, che le directory di destinazione sono percorsi relativi alla cartella di installazione del pacchetto. Non è possibile utilizzare percorsi assoluti o contenere `..` per motivi di sicurezza. I percorsi di installazione dei pacchetti sono predefiniti e non possono essere modificati.

Il seguente script stampa a terminale il tag `<File>` per ogni file e directory nella cartella corrente, calcolando l'hash SHA-256 e comprimendo le directory in formato tar.gz:

```bash
echo "<Files>"
#!/bin/bash

# Evita problemi di expansione globale se la cartella è vuota
shopt -s nullglob

for item in *; do
    # Verifica che l'elemento esista (per evitare errori con nullglob)
    [ -e "$item" ] || continue

    if [ -d "$item" ]; then
        # Rimuove lo slash finale in modo sicuro
        dir="${item%/}"

        # Comprime la directory quotando tutte le variabili
        tar -czvf "$dir.tar.gz" "$dir" >/dev/null

        # Stampa il tag Directory
        echo "<Directory src=\"$dir.tar.gz\" dest=\"$dir\" sha256=\"$(sha256sum "$dir.tar.gz" | cut -d' ' -f1)\" />"

    elif [ -f "$item" ]; then
        # Ignora gli archivi .tar.gz generati durante l'esecuzione
        if [[ "$item" == *.tar.gz ]]; then
            continue
        fi

        # Stampa il tag File
        echo "<File src=\"$item\" sha256=\"$(sha256sum "$item" | cut -d' ' -f1)\" />"
    fi
done
echo "</Files>"
```
