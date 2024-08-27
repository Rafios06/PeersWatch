import libtorrent as lt
import time
import argparse
import csv

def main(torrent_file_path, save_path, output_file, wait_time):
    # Lire et décoder le fichier .torrent
    with open(torrent_file_path, 'rb') as f:
        torrent_data = lt.bdecode(f.read())

    # Créer un objet torrent_info à partir des données décodées
    torrent_info_obj = lt.torrent_info(torrent_data)

    # Créer une session et ajouter le torrent
    ses = lt.session()
    params = {
        'save_path': save_path,  # Chemin où le fichier sera téléchargé
        'storage_mode': lt.storage_mode_t.storage_mode_sparse,
        'ti': torrent_info_obj
    }

    h = ses.add_torrent(params)

    # Attendre quelques instants pour que les pairs se connectent
    print("\nConnexion aux pairs...")
    time.sleep(wait_time)

    # Récupérer la liste des pairs connectés
    peers = h.get_peer_info()

    # Ouvrir un fichier CSV pour écrire les informations des pairs
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['IP', 'Upload (KB/s)', 'Download (KB/s)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for peer in peers:
            ip = peer.ip[0]
            upload_speed = peer.up_speed / 1000  # Convertir en KB/s
            download_speed = peer.down_speed / 1000  # Convertir en KB/s

            writer.writerow({
                'IP': ip,
                'Upload (KB/s)': upload_speed,
                'Download (KB/s)': download_speed
            })

            print(f"IP: {ip}")
            print(f"Vitesse d'upload: {upload_speed} KB/s")
            print(f"Vitesse de téléchargement: {download_speed} KB/s")
            print("---")

    # Arrêter le téléchargement après avoir récupéré les informations
    ses.remove_torrent(h)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Récupérer les informations des pairs d'un fichier torrent.")
    parser.add_argument("torrent_file", type=str, help="Chemin vers le fichier .torrent")
    parser.add_argument("--save-path", type=str, default="./", help="Chemin où le fichier sera téléchargé")
    parser.add_argument("--output-file", type=str, default="peers_info.csv", help="Fichier de sortie pour les informations des pairs")
    parser.add_argument("--wait-time", type=int, default=60, help="Temps d'attente pour la connexion aux pairs (en secondes)")

    args = parser.parse_args()
    main(args.torrent_file, args.save_path, args.output_file, args.wait_time)
