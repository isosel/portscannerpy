# Port Scanner

## Description
**Port Scanner** est un outil basique pour scanner les ports TCP (par défaut) et UDP (option -u) d'une cible (nom d'hôte ou adresse IP).
Il permet de détecter les ports ouverts et d'identifier les services qui y sont associés quand c'est possible.

Ce script utilise les threads pour scanner plusieurs ports à la fois.

---

## Fonctionnalités

- Scanner un **port unique** (option -sp) ou une **plage de ports** (option -r).
- Support des protocoles **TCP** (par défaut) et **UDP** (option -u).
- Affichage des résultats avec une barre de progression (import tqdm).
- Enregistrement des résultats dans un fichier texte.
- Validation des arguments pour éviter les erreurs.

---

## Prérequis

- **Python 3.6+**
- Bibliothèques Python nécessaires :
  - `pyfiglet` : pour l'affichage d'une bannière ASCII.
  - `tqdm` : pour la barre de progression.

### Installation des dépendances

Utilisez `pip` pour installer les dépendances nécessaires :
```bash
pip install pyfiglet tqdm
```

---

## Utilisation

### Commande de base

```bash
python port_scanner.py <target> [options]
```
Exemples plus bas.

### Arguments

1. **Obligatoire :**
   - `<target>` : Le nom d'hôte ou directement l'adresse IP de la cible à scanner.

2. **Options :**
   - `-sp`, `--single-port` : Spécifie un port unique à scanner.
   - `-r`, `--range` : Spécifie une plage de ports à scanner (ex: `-r 1 100`).
   - `-u`, `--udp` : Effectue un scan UDP (TCP par défaut).
   - `-o`, `--output` : Nom du fichier pour enregistrer les résultats (`scan_results.txt` par défaut).

---

### Exemples

1. **Scanner un port unique :**
   ```bash
   python port_scanner.py example.com -sp 80
   ```

2. **Scanner une plage de ports :**
   ```bash
   python port_scanner.py example.com -r 1 100
   ```

3. **Scanner une plage de ports (UDP) :**
   ```bash
   python port_scanner.py example.com -r 50 100 -u
   ```

4. **Enregistrer les résultats dans un fichier personnalisé :**
   ```bash
   python port_scanner.py example.com -r 1 100 -o my_results.txt
   ```

---

## Résultats

Les résultats du scan incluent :
- Les ports ouverts.
- Les protocoles utilisés (TCP ou UDP).
- Les services associés, lorsque c'est disponibles.
- 

### Exemple de sortie console :
```
$ python main.py 127.0.0.1 -u -r 1 60000
 ____   ___  ____ _____   ____   ____    _    _   _ _   _ _____ ____
|  _ \ / _ \|  _ \_   _| / ___| / ___|  / \  | \ | | \ | | ____|  _ \
| |_) | | | | |_) || |   \___ \| |     / _ \ |  \| |  \| |  _| | |_) |
|  __/| |_| |  _ < | |    ___) | |___ / ___ \| |\  | |\  | |___|  _ <
|_|    \___/|_| \_\|_|   |____/ \____/_/   \_\_| \_|_| \_|_____|_| \_\


--------------------------------------------------
Scanning Target: 127.0.0.1 (127.0.0.1)
Protocole : UDP
Scanning started at: 2024-11-25 11:13:12.273872
--------------------------------------------------

Scan en cours...
Scanning ports: 100%|##########| 60000/60000 [00:12<00:00, 4683.04it/s]

Aucun port ouvert trouvé.

Scan terminé. Résultats enregistrés dans 'scan_results.txt'.

$ python main.py localhost -r 1 1000
 ____   ___  ____ _____   ____   ____    _    _   _ _   _ _____ ____
|  _ \ / _ \|  _ \_   _| / ___| / ___|  / \  | \ | | \ | | ____|  _ \
| |_) | | | | |_) || |   \___ \| |     / _ \ |  \| |  \| |  _| | |_) |
|  __/| |_| |  _ < | |    ___) | |___ / ___ \| |\  | |\  | |___|  _ <
|_|    \___/|_| \_\|_|   |____/ \____/_/   \_\_| \_|_| \_|_____|_| \_\


--------------------------------------------------
Scanning Target: localhost (127.0.0.1)
Protocole : TCP
Scanning started at: 2024-11-25 11:15:11.111768
--------------------------------------------------

Scan en cours...
Scanning ports: 100%|##########| 1000/1000 [00:00<00:00, 12922.97it/s]

Ports ouverts :
- Port 135 (TCP) : epmap
- Port 445 (TCP) : microsoft-ds

Scan terminé. Résultats enregistrés dans 'scan_results.txt'.


```

---


## Auteur

- **Nom :** Mickael Cherouise
- **Version :** 2.0
- **Date :** 2024-11-25

---

## Mot de la fin

J'ai fait ce programme surtout pour m'exercer aux threads. Ce programme est donc à utiliser dans un cadre éducatif uniquement. Scanner des ports comme avec "nmap" peut être considéré comme intrusif et interdit selon les pays... Renseignez vous donc.




