import aerosandbox as asb
import aerosandbox.numpy as np
import pandas as pd
 
# Demande à l'utilisateur le nom du profil d'aile
x = str(input("Profil d'aile principal : "))
 
# Chargement du profil
af = asb.Airfoil(x)
 
# Conversion en profil Kulfan (optionnel)
kulfan_airfoil = af.to_kulfan_airfoil()
print("Paramètres Kulfan :")
print(kulfan_airfoil.kulfan_parameters)
 
# Récupération des coordonnées du profil (x, y)
coords = af.coordinates  # Tableau Nx2
 
# ✅ S'assurer que le profil est fermé
if not np.allclose(coords[0], coords[-1], atol=1e-6):
    coords = np.vstack([coords, coords[0]])  # Ajoute le premier point à la fin
 
# ✅ Optionnel : s’assurer que le profil va bien dans l’ordre (haut → bas)
# Certaines versions d’AeroSandbox inversent l’ordre, donc on peut le forcer :
# coords = np.flipud(coords)  # Décommente si ton profil semble “retourné” dans FreeCAD
 
# Conversion en DataFrame Pandas
df = pd.DataFrame(coords, columns=["x", "y"])
 
# Sauvegarde en fichier CSV
nom_fichier = f"{x}_profil.csv"
df.to_csv(nom_fichier, index=False)
 
print(f"\n✅ Profil exporté avec succès dans le fichier : {nom_fichier}")
print(f"➡️ Profil correctement fermé pour utilisation dans FreeCAD.")
 
