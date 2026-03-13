# Guide GitHub Release

## 1. Créer le repo

Exemple :

- nom du repo : `msa-video-tool`
- branche principale : `main`

## 2. Premier push

```bash
cd "/chemin/vers/ton/repo"
git init
git add .
git commit -m "Initial release 1.1.0"
git branch -M main
git remote add origin https://github.com/TON_USER/TON_REPO.git
git push -u origin main
```

## 3. Déclencher la première release

```bash
git tag v1.1.0
git push origin v1.1.0
```

## 4. URL du manifeste

Utilise cette forme :

```text
https://raw.githubusercontent.com/TON_USER/TON_REPO/main/update_manifest.json
```

## 5. Exemple de release suivante

```bash
git add videoracing_pipeline_v1_1.py update_manifest.json
git commit -m "Release 1.1.1"
git push origin main
git tag v1.1.1
git push origin v1.1.1
```

## 6. Vérification

Après le tag :

1. va dans `Actions`
2. attends la fin du workflow `Release Windows Exe`
3. va dans `Releases`
4. vérifie que l'exe est bien attaché
