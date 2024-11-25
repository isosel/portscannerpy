#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Port Scanner - Outil de scan de ports TCP/UDP
Auteur : Mickael Cherouise
Date : 2024-11-25
Description :
Ce script scanne des ports TCP ou UDP sur une cible spécifiée (nom d'hôte ou adresse IP).
L'utilisateur peut choisir :
- De scanner un seul port ou une plage de ports
- D'utiliser le protocole TCP ou UDP
Les résultats sont affichés et enregistrés dans un fichier texte.
"""

import pyfiglet
import argparse
import socket
from datetime import datetime
import threading
from tqdm import tqdm


# Affichage d'une bannière avec pyfiglet
ascii_banner = pyfiglet.figlet_format("PORT SCANNER")
print(ascii_banner)

# Métadonnées
__author__ = "Mickael Cherouise"
__version__ = "2.0"
__date__ = "2024-11-25"

# Gestion des arguments de ligne de commande
parser = argparse.ArgumentParser(description="Scanner de ports TCP/UDP.")
parser.add_argument("target", help="Nom d'hôte ou adresse IP de la cible.")
parser.add_argument("-sp", "--single-port", type=int, help="Scanner un seul port (ex: 80).")
parser.add_argument("-r", "--range", nargs=2, metavar=("START", "END"), type=int,
                    help="Scanner une plage de ports (ex: 1 100).")
parser.add_argument("-u", "--udp", action="store_true", help="Effectuer un scan UDP au lieu de TCP.")
parser.add_argument("-o", "--output", type=str, default="scan_results.txt",
                    help="Nom du fichier pour enregistrer les résultats (par défaut: scan_results.txt).")

args = parser.parse_args()

# Résolution du nom d'hôte ou de l'adresse IP
try:
    target_ip = socket.gethostbyname(args.target)
except socket.gaierror:
    print("Erreur : Nom d'hôte ou IP invalide.")
    exit(1)

# Déterminer la plage de ports à scanner
if args.single_port:
    ports_to_scan = [args.single_port]
elif args.range:
    start_port, end_port = args.range
    if start_port < 1 or end_port > 65535 or start_port > end_port:
        print("Erreur : Plage de ports invalide.")
        exit(1)
    ports_to_scan = range(start_port, end_port + 1)
else:
    print("Erreur : Vous devez spécifier un port unique (-sp) ou une plage de ports (-r).")
    exit(1)

# Informations initiales
print("-" * 50)
print(f"Scanning Target: {args.target} ({target_ip})")
print(f"Protocole : {'UDP' if args.udp else 'TCP'}")
print("Scanning started at:", str(datetime.now()))
print("-" * 50)

# Liste pour enregistrer les ports ouverts
open_ports = []
lock = threading.Lock()


# Fonction pour scanner un port TCP
def scan_tcp(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        if s.connect_ex((target_ip, port)) == 0:
            try:
                service = socket.getservbyport(port, "tcp")
            except:
                service = "Inconnu"
            with lock:
                open_ports.append((port, service, "TCP"))
        s.close()
    except Exception:
        pass


# Fonction pour scanner un port UDP
def scan_udp(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(1)
        s.sendto(b"Test UDP", (target_ip, port))  # Envoi d'un paquet test
        try:
            _, _ = s.recvfrom(1024)  # Attente d'une réponse
            with lock:
                open_ports.append((port, "Inconnu", "UDP"))
        except socket.timeout:
            pass  # Pas de réponse, port probablement fermé
        s.close()
    except Exception:
        pass


# Lancement du scan avec threads
threads = []
print("\nScan en cours...")
for port in tqdm(ports_to_scan, desc="Scanning ports"):
    if args.udp:
        thread = threading.Thread(target=scan_udp, args=(port,))
    else:
        thread = threading.Thread(target=scan_tcp, args=(port,))
    threads.append(thread)
    thread.start()

# Attendre que tous les threads soient terminés
for thread in threads:
    thread.join()

# Affichage des résultats
if open_ports:
    print("\nPorts ouverts :")
    for port, service, protocol in open_ports:
        print(f"- Port {port} ({protocol}) : {service}")
else:
    print("\nAucun port ouvert trouvé.")

# Enregistrer les résultats dans un fichier
with open(args.output, "w") as file:
    file.write(f"Scan de {args.target} ({target_ip}) réalisé le {datetime.now()}\n")
    file.write(f"Protocole : {'UDP' if args.udp else 'TCP'}\n")
    if open_ports:
        file.write("Ports ouverts :\n")
        for port, service, protocol in open_ports:
            file.write(f"- Port {port} ({protocol}) : {service}\n")
    else:
        file.write("Aucun port ouvert trouvé.\n")

print(f"\nScan terminé. Résultats enregistrés dans '{args.output}'.")
