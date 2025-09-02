import subprocess
import html

def execute_command(command):
    try:
        output = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.STDOUT)
        return html.escape(output)
    except subprocess.CalledProcessError as e:
        return f"Erreur lors de l'exécution de la commande : {html.escape(e.output)}"

# Saisie de la cible
ip_or_hostnames = input(
    "Entrez les adresses IP, plages CIDR ou noms d'hôte du contrôleur de domaine (séparés par une virgule) : "
)

# Affichage des options d'outils disponibles
print("\nOptions d'outils de découverte des partages réseau :")
print("1. Nmap avec le script smb-enum-shares")
print("2. smbmap")
print("3. enum4linux")
print("4. Nmap avec le script smb2-security-mode.nse")
print("5. CrackMapExec (CME)")
print("6. Tous les outils précédents")
print("7. Arping 4ping")
print("8. Nmap avancé (-sV -Pn -n -O -vvv -g 0) sur les ports les plus intéressants")
print("9. Dmitry -p")
print("10. Tous les outils (full)")

option = input("Choisissez une option (1-10) : ")

# Traitement des IPs/hostnames
ip_list = []
for entry in ip_or_hostnames.split(","):
    entry = entry.strip()
    if entry:
        ip_list.append(entry)

# Ports optimisés pour la découverte Windows/AD
best_ports = (
    "53,88,135,137,138,139,389,445,464,593,636,3268,3269,3389,5985,5986,1433,3306,5432,8080,8000,8443"
)
# Explication rapide :
# 53   DNS
# 88   Kerberos
# 135  RPC
# 137-139 NetBIOS
# 389/636 LDAP/LDAPS
# 445  SMB
# 464  Kerberos kpasswd
# 593  RPC over HTTP
# 3268/3269 Global Catalog
# 3389 RDP
# 5985/5986 WinRM (PowerShell Remoting)
# 1433 MSSQL
# 3306 MySQL
# 5432 PostgreSQL
# 8080/8000/8443 Web apps/services

commands = []
if option == "1":
    for ip in ip_list:
        commands.append(f"nmap -p 445 --script smb-enum-shares {ip}")
elif option == "2":
    for ip in ip_list:
        commands.append(f"smbmap -H {ip}")
elif option == "3":
    for ip in ip_list:
        commands.append(f"enum4linux {ip}")
elif option == "4":
    for ip in ip_list:
        commands.append(f"nmap -p 445 --script smb2-security-mode.nse {ip}")
elif option == "5":
    for ip in ip_list:
        commands.append(f"crackmapexec smb {ip}")
elif option == "6":
    for ip in ip_list:
        commands.extend([
            f"nmap -p 445 --script smb-enum-shares {ip}",
            f"smbmap -H {ip}",
            f"enum4linux {ip}",
            f"nmap -p 445 --script smb2-security-mode.nse {ip}",
            f"crackmapexec smb {ip}"
        ])
elif option == "7":
    for ip in ip_list:
        commands.append(f"arping -c 4 {ip}")
elif option == "8":
    for ip in ip_list:
        commands.append(
            f"nmap -sV -Pn -n -O -vvv -g 0 {ip} -p{best_ports}"
        )
elif option == "9":
    for ip in ip_list:
        commands.append(
            f"dmitry -p {ip}"
        )

elif option == "10":
    for ip in ip_list:
        commands.extend([
            f"nmap -p 445 --script smb-enum-shares {ip}",
            f"smbmap -H {ip}",
            f"enum4linux {ip}",
            f"nmap -p 445 --script smb2-security-mode.nse {ip}",
            f"crackmapexec smb {ip}",
            f"nmap -sV -Pn -n -O -vvv -g 0 {ip} -p{best_ports}",
            f"arping -c 4 {ip}",
            f"dmitry -p {ip}"
        ])
else:
    print("Option invalide. Veuillez choisir une option valide.")
    exit()

# Exécution des commandes
output_html = ""
for command in commands:
    command_output = execute_command(command)
    output_html += f"<h3>Commande: {html.escape(command)}</h3>"
    output_html += f"<pre>{command_output}</pre>"
    output_html += "<hr>"

# Écriture dans le fichier HTML
with open("output.html", "w") as file:
    file.write(f"<html><body>{output_html}</body></html>")

print("\nLe fichier HTML de sortie a été généré : output.html")
