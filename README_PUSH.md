# V1.1 GitHub Push

Ce dossier est prêt à servir de base pour publier la release `1.1.0` sur GitHub avec :

- build Windows automatique
- release GitHub automatique sur tag
- manifeste JSON pour la popup de mise à jour

## Fichiers importants

- `videoracing_pipeline_v1_1.py`
- `run_msa_video_tool_v1_1.sh`
- `.github/workflows/main.yml`
- `.github/workflows/release.yml`
- `update_manifest.json`
- `update_manifest.example.json`

`main.yml` et `release.yml` existent aussi à la racine du dossier uniquement pour être visibles facilement. Les fichiers réellement utilisés par GitHub Actions sont dans `.github/workflows/`.

## Mise en place GitHub

1. crée un repo GitHub public
2. copie le contenu de ce dossier à la racine du repo
3. pousse sur `main`

Le workflow `.github/workflows/main.yml` buildera l'exe Windows à chaque push.

## Première release

1. vérifie que `APP_VERSION` dans `videoracing_pipeline_v1_1.py` vaut bien `1.1.0`
2. pousse sur `main`
3. crée le tag Git :
   - `v1.1.0`
4. pousse le tag :
   - `git push origin v1.1.0`

Le workflow `.github/workflows/release.yml` va :

- builder l'exe Windows
- créer la GitHub Release
- attacher automatiquement :
  - `MSA-Video-Tool-1.1.0.exe`

## Popup de mise à jour

Le manifeste public doit rester accessible à une URL stable, par exemple :

- `https://raw.githubusercontent.com/TON_USER/TON_REPO/main/update_manifest.json`

Pense à remplacer `TON_USER` et `TON_REPO` dans :

- `update_manifest.json`
- `update_manifest.example.json`

Dans l'app, l'URL du manifeste se renseigne dans `Réglages > Système > URL manifeste`.

## Publication des versions suivantes

Exemple pour `1.1.1` :

1. change `APP_VERSION = "1.1.1"` dans `videoracing_pipeline_v1_1.py`
2. commit
3. push sur `main`
4. crée le tag :
   - `v1.1.1`
5. pousse le tag :
   - `git push origin v1.1.1`
6. mets à jour `update_manifest.json` :
   - `version: 1.1.1`
   - `download_url`: URL de la nouvelle release
   - `notes`
7. commit + push le manifeste

## Important

- le lien de mise à jour doit pointer vers une vraie GitHub Release, pas vers un artifact GitHub Actions
- le repo doit être public si les utilisateurs finaux ne se connectent pas à GitHub
- `update_manifest.json` doit rester à la même URL
- le traitement `.INSV` demandera toujours un SDK Insta360 configuré manuellement sur la machine finale
