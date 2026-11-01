"""
Filtre le dataset Steam Reviews (716MB) pour ne garder que les jeux Resident Evil.
Résultat : un CSV beaucoup plus petit, facile à charger dans Power BI.

Usage :
    1. Installe pandas si besoin :  pip install pandas
    2. Mets ce script dans le même dossier que le CSV dézippé (ex: dataset.csv)
    3. Modifie INPUT_FILE ci-dessous avec le nom exact de ton fichier
    4. Lance :  python filter_resident_evil_reviews.py
"""

import pandas as pd

# ----- À adapter -----
INPUT_FILE = "dataset.csv"          # nom exact du CSV téléchargé (716MB)
OUTPUT_FILE = "resident_evil_reviews.csv"
CHUNK_SIZE = 200_000                 # nb de lignes lues à la fois (évite de saturer la RAM)
# ----------------------

# Mots-clés pour repérer tous les jeux de la franchise
# (couvre les remakes, extensions, spin-offs comme "Resistance", "Revelations", etc.)
KEYWORDS = ["resident evil", "biohazard"]

def matches_resident_evil(name: str) -> bool:
    if pd.isna(name):
        return False
    name_lower = name.lower()
    return any(kw in name_lower for kw in KEYWORDS)

def main():
    chunks_filtered = []
    total_rows_read = 0
    total_rows_kept = 0

    reader = pd.read_csv(
        INPUT_FILE,
        chunksize=CHUNK_SIZE,
        encoding="utf-8",
        on_bad_lines="skip",   # ignore les lignes corrompues sans planter
    )

    for i, chunk in enumerate(reader):
        total_rows_read += len(chunk)

        mask = chunk["app_name"].apply(matches_resident_evil)
        filtered = chunk[mask]

        if not filtered.empty:
            chunks_filtered.append(filtered)
            total_rows_kept += len(filtered)

        print(f"Chunk {i+1} : {total_rows_read:,} lignes lues, {total_rows_kept:,} gardées jusqu'ici", end="\r")

    print()  # nouvelle ligne après la barre de progression

    if chunks_filtered:
        result = pd.concat(chunks_filtered, ignore_index=True)
        result.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
        print(f"\nTerminé ! {len(result):,} avis Resident Evil trouvés sur {total_rows_read:,} lignes au total.")
        print(f"Fichier sauvegardé : {OUTPUT_FILE}")
        print("\nJeux trouvés dans le dataset :")
        print(result["app_name"].value_counts())
    else:
        print("\nAucun avis Resident Evil trouvé. Vérifie le nom exact de la colonne 'app_name'.")

if __name__ == "__main__":
    main()