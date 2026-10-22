# Game Force — applications Windows, Mac et Android

Ce dossier contient le jeu et tout ce qu'il faut pour fabriquer **automatiquement sur GitHub** :

| Plateforme | Fichier obtenu | Outil |
|---|---|---|
| Windows | `GameForce-Setup-x.y.z-x64.exe` (installateur) | Electron |
| Mac | `GameForce-x.y.z-mac-arm64.dmg` (Apple Silicon) et `…-mac-x64.dmg` (Intel) | Electron |
| Android | `GameForce-android.apk` | Capacitor |
| Navigateur | installable depuis Chrome / Edge / Safari (« Installer l'application ») | PWA |

Aucun ordinateur Mac ni Android Studio n'est nécessaire : GitHub fabrique chaque fichier sur ses propres machines (Windows, Mac et Linux), gratuitement pour un dépôt public ou dans les quotas gratuits d'un dépôt privé.

## 1. Fabriquer les fichiers (une seule fois à mettre en place)

1. Crée un compte sur https://github.com puis un **nouveau dépôt** (par exemple `game-force`).
2. Envoie-y **tout le contenu de ce dossier**, y compris le dossier caché `.github` (sur le site : *Add file → Upload files*, glisse tous les fichiers ; ou avec Git : `git init && git add . && git commit -m "Game Force" && git push`).
3. Onglet **Actions** → *Construire les applications* → **Run workflow**. Compte environ 10 à 20 minutes.
4. Quand c'est vert, ouvre l'exécution et télécharge les fichiers dans **Artifacts** (`windows-exe`, `mac-dmg`, `android-apk`).

### Publier une version avec un lien de téléchargement
Crée une étiquette de version : sur GitHub, *Releases → Draft a new release → Choose a tag → `v1.0.0` → Publish*, ou en ligne de commande `git tag v1.0.0 && git push --tags`.
GitHub fabrique alors tout et publie les 4 fichiers dans **Releases**, avec le numéro de version `1.0.0` appliqué à chaque application.

## 2. Installer

**Windows** — double-clique sur `GameForce-Setup-….exe`. Comme l'application n'est pas signée numériquement, Windows affiche « Windows a protégé votre ordinateur » : clique sur *Informations complémentaires* puis *Exécuter quand même*.

**Mac** — ouvre le `.dmg`, glisse *Game Force* dans *Applications*. Choisis `arm64` pour les Mac récents (puce M1 à M4) et `x64` pour les Mac Intel. Au premier lancement : clic droit sur l'app → *Ouvrir* → *Ouvrir*. Si macOS dit que l'app est « endommagée », ouvre le Terminal et tape : `xattr -cr "/Applications/Game Force.app"`.

**Android** — copie le `.apk` sur le téléphone, ouvre-le et autorise « installer des applications inconnues » pour ton navigateur ou ton gestionnaire de fichiers. L'APK fourni est signé avec la clé de débogage : il s'installe sans problème, mais ne peut pas être publié sur le Play Store (voir plus bas).

**Navigateur (PWA)** — si tu héberges le dossier `www` sur un site en HTTPS (GitHub Pages par exemple), Chrome/Edge proposent *Installer Game Force*, et le jeu fonctionne ensuite hors connexion.

## 3. Sauvegarde de la progression
- Dans les applications Windows/Mac et Android, la progression est enregistrée **dans les données de l'application sur l'appareil** (et non dans un navigateur).
- Le bouton **💾 Sauvegarde** exporte un fichier `.json` : sur Android, il ouvre le menu de partage (Fichiers, Drive…) ; sur ordinateur, une fenêtre « Enregistrer sous ».
- Une désinstallation efface les données de l'application : exporte avant.

## 4. Réglages utiles
- **Nom / identifiant de l'application** : `package.json` (clé `build.appId`, `productName`) et `capacitor.config.json` (`appId`, `appName`). Garde le même `appId` partout. Choisis-le avant ta première publication : le changer plus tard crée une autre application.
- **Icône** : remplace `build/icon.png` (1024×1024), `assets/icon-only.png`, `assets/icon-foreground.png`, `assets/icon-background.png`, `assets/splash.png` et les images de `www/icons/`.
- **Jeu** : remplace `www/index.html` par la nouvelle version du jeu, puis relance la fabrication.
- **Textes légaux** : complète les passages entre crochets dans `www/cgu-confidentialite.html` (et dans la fenêtre CGU du jeu).

## 5. Pour aller plus loin (facultatif)
- **Windows sans avertissement** : certificat de signature de code (payant). **Mac sans avertissement** : compte Apple Developer (99 $/an) pour signer et notariser. Les fichiers fabriqués ici fonctionnent sans, avec les avertissements décrits plus haut.
- **Android signé / Play Store** : crée une clé (`keytool -genkey -v -keystore release.keystore -alias gameforce -keyalg RSA -keysize 2048 -validity 10000`), puis ajoute dans *Settings → Secrets and variables → Actions* : `ANDROID_KEYSTORE_BASE64` (le fichier encodé : `base64 -w0 release.keystore`), `ANDROID_KEYSTORE_PASSWORD`, `ANDROID_KEY_ALIAS`, `ANDROID_KEY_PASSWORD`. L'étape de signature s'active alors toute seule et ajoute `GameForce-android-signe.apk`. **Garde cette clé en lieu sûr** : sans elle, tu ne pourras plus mettre l'application à jour.

## 6. Tester sur ton ordinateur (facultatif)
Avec Node.js 20+ : `npm install`, puis `npm start` ouvre l'application de bureau. `npm run dist:win` / `dist:mac` fabrique l'installateur de **ton** système.
