import pandas as pd
import matplotlib.pyplot as plt
 
# === Nom du fichier à tester ===
fichier_csv = "naca2412_profil.csv"   # ← mets ici ton chemin exact
 
# === Lecture du fichier ===
df = pd.read_csv(fichier_csv)
 
# Vérification des colonnes
if not all(col in df.columns for col in ["x", "y"]):
    raise ValueError("⚠️ Le fichier doit contenir des colonnes 'x' et 'y'.")
 
x = df["x"].values
y = df["y"].values
 
# === Visualisation ===
plt.figure(figsize=(7, 3))
plt.plot(x, y, "-o", markersize=3, label="Profil NACA")
 
# On relie le dernier point au premier pour vérifier la fermeture
plt.plot([x[0], x[-1]], [y[0], y[-1]], "r--", label="Fermeture")
 
plt.axis("equal")
plt.title(f"Visualisation du profil : {fichier_csv}")
plt.xlabel("x (corde)")
plt.ylabel("y (épaisseur)")
plt.legend()
plt.grid(True)
plt.show()
 
# === Diagnostic automatique ===
dx = abs(x[0] - x[-1])
dy = abs(y[0] - y[-1])
if dx < 1e-6 and dy < 1e-6:
    print("✅ Profil correctement fermé.")
else:
    print(f"⚠️ Profil ouvert : Δx={dx:.6g}, Δy={dy:.6g} → à fermer avant FreeCAD.")