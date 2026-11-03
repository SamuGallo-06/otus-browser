# Otus Packages

Otus Browser can install packages with the `.otuspkg` extension. A package is
a ZIP archive containing a `manifest.otus` file at its root and the resources
declared by the manifest.

The package manager records installed packages in `packages.xml` and, for
applications, also maintains the `apps.xml` registry. Files are installed in
the user's data directory:

| Type | Installation directory |
| --- | --- |
| `language` | `Languages/<lang_code>` |
| `theme` | `Themes/<id>` |
| `homepage` | `HomePages/<id>` |
| other types, including `app` | `Packages/<id>` |

The actual paths depend on the system and Otus settings.

## Manifest

The manifest is an XML document with an `OtusPackageManifest` root element. It
requires the `schemaVersion` and `type` attributes. The currently supported
schema version is `1`.

The main metadata fields are:

- `Id`: unique package identifier;
- `Name`: displayed name;
- `Version`: package version;
- `Description`: description;
- `License`: license;
- `Authors`: one or more `Author` elements;
- `Meta`: metadata specific to the package type;
- `icon`: name of an image file in the package root (optional).

Minimal example:

```xml
<OtusPackageManifest schemaVersion="1" type="language">
    <Id>io.github.samugallo06.otus_lang_it</Id>
    <Name>Italian Language Pack</Name>
    <Version>1.0.0</Version>
    <Description>Italian translations for Otus Browser</Description>
    <Authors>
        <Author>Samuele Gallicani</Author>
    </Authors>
    <License>GPL-3.0</License>
    <Meta lang_code="it_IT" />
    <icon>otus-pkg-default.png</icon>
    <Files>
        <File src="translations/otus_browser_it_IT.qm"
              dest="otus_browser_it_IT.qm"
              sha256="HASH_SHA256" />
    </Files>
</OtusPackageManifest>
```

`src` is relative to the root of the `.otuspkg` archive; `dest` is relative to
the installation directory. To prevent overwrites or access outside the
package directory, use only safe relative paths: do not use absolute paths,
`..`, or Windows separators (`\`). The entrypoint of an app and the members of
directory archives are checked by the package manager using these rules.

## Language packages

A language package uses `type="language"` and must declare `lang_code` in
`Meta`. The value must match the locale code used by Qt, such as `it_IT`.

Translations are detected automatically when the installed directory contains
a file named:

```text
otus_browser_<lang_code>.qm
```

Example:

```xml
<OtusPackageManifest schemaVersion="1" type="language">
    <Id>io.github.samugallo06.otus_lang_it</Id>
    <Name>Italian Language Pack</Name>
    <Version>1.0.0</Version>
    <Description>Italian translations for Otus Browser</Description>
    <Authors><Author>Samuele Gallicani</Author></Authors>
    <License>GPL-3.0</License>
    <Meta lang_code="it_IT" />
    <Files>
        <File src="otus_browser_it_IT.qm"
              dest="otus_browser_it_IT.qm"
              sha256="HASH_SHA256" />
    </Files>
</OtusPackageManifest>
```

## Local applications

An HTML application uses `type="app"` and is opened in a new browser tab. It
must declare:

- `runtime="self"` in `Meta`;
- `entrypoint`, relative to the application directory.

The entrypoint must be included in the package, must be a file, and cannot be
absolute or contain `..`.

```xml
<OtusPackageManifest schemaVersion="1" type="app">
    <Id>io.github.samugallo06.otus_pdf_reader</Id>
    <Name>Otus PDF Reader</Name>
    <Version>1.0.0</Version>
    <Description>PDF reader for Otus Browser</Description>
    <Authors><Author>Samuele Gallicani</Author></Authors>
    <License>GPL-3.0</License>
    <Meta runtime="self" entrypoint="index.html" />
    <Files>
        <File src="index.html" dest="index.html" sha256="HASH_SHA256" />
        <Directory src="assets.tar.gz" dest="assets" sha256="HASH_SHA256" />
    </Files>
</OtusPackageManifest>
```

After installation, the application is registered in `apps.xml`. It can be
opened with a double-click in the package manager.

## Files and directories

Resources are declared inside `Files`:

```xml
<File src="js/app.js" dest="js/app.js" sha256="HASH_SHA256" />
<Directory src="css.tar.gz" dest="css" sha256="HASH_SHA256" />
```

- `File` is copied to the specified destination.
- `Directory` must point to a tar archive, normally gzip-compressed
  (`.tar.gz`), which is extracted to the specified destination.
- `sha256` is the SHA-256 hash of the source file or tar archive.

The package manager currently verifies the hash of `File` entries. The
`sha256` value of `Directory` entries is part of the manifest format, but is
not yet checked during installation. It should nevertheless be filled in
correctly so that the manifest is complete and ready for future checks.
Tar archives cannot contain symbolic links, hard links, or paths that escape
the destination directory.

## Building a package

1. Create a working directory.
2. Place `manifest.otus` at its root.
3. Add the resources declared by the manifest.
4. Calculate the SHA-256 hashes.
5. Compress the directory contents into a ZIP archive with the `.otuspkg`
   extension, keeping `manifest.otus` at the archive root.

The following Bash script can be run from the package directory to create
directory archives and print the XML elements. It excludes `.tar.gz` archives
already generated and always includes `dest`, which is required for every
element:

```bash
#!/usr/bin/env bash
set -euo pipefail
shopt -s nullglob

echo "<Files>"
for item in *; do
    [[ -e "$item" ]] || continue
    [[ "$item" == "manifest.otus" || "$item" == *.tar.gz ]] && continue

    if [[ -d "$item" ]]; then
        tar -czf "$item.tar.gz" "$item"
        hash=$(sha256sum "$item.tar.gz" | cut -d' ' -f1)
        printf '    <Directory src="%s" dest="%s" sha256="%s" />\n' \
            "$item.tar.gz" "$item" "$hash"
    elif [[ -f "$item" ]]; then
        hash=$(sha256sum "$item" | cut -d' ' -f1)
        printf '    <File src="%s" dest="%s" sha256="%s" />\n' \
            "$item" "$item" "$hash"
    fi
done
echo "</Files>"
```

Update the manifest after running the script by inserting the generated
`<Files>` block. Finally, create the package:

```bash
zip -r otus-example.otuspkg manifest.otus index.html js/ css.tar.gz
```

Do not place the manifest inside a subdirectory of the archive.

## Installation, updates, and removal

In the package manager, choose **Install Package** and select an `.otuspkg`
file. The package is extracted to a temporary directory, the manifest is
read, file hashes are checked, and resources are copied or extracted to the
package installation directory.

To remove a package, select it in the list and choose **Uninstall Package**.
Otus removes the registered directory and the corresponding registry entries.
Reinstalling a package with the same identifier depends on the registry
contents: to replace an installed version, uninstall the existing version
first.

Errors in the ZIP file, a missing or invalid manifest, missing files,
mismatched hashes, and unsafe tar archives stop the installation and are
reported by the package manager.
