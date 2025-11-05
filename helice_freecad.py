import FreeCAD, Part, csv
from FreeCAD import Vector

doc = FreeCAD.newDocument("Helice_Avancee_Progressive")

# Paramètres
profil_csv = r"chemin d acces "
nb_sections = 8
nb_pales = 3
rayon_bout = 100
moyeu_rayon = 15
moyeu_hauteur = 15
trou_diametre = 6
pitch_angle_deg = 15
penetration_base = 4.0    # base fortement insérée
penetration_tip = 1.0     # pointe légèrement insérée
marge_trou = 0.5
facteur_corde = 2.0

# Lecture profil
airfoil_pts = []
with open(profil_csv) as f:
    reader = csv.reader(f)
    next(reader,None)
    for row in reader:
        airfoil_pts.append(Vector(float(row[0]), float(row[1]), 0))
if (airfoil_pts[0]-airfoil_pts[-1]).Length > 1e-6:
    airfoil_pts.append(airfoil_pts[0])

def make_section(radius, scale=1.0):
    pts=[]
    for p in airfoil_pts:
        x = radius
        y = p.x*scale-moyeu_rayon
        z = p.y*scale
        pts.append(Vector(x,y,z))
    wire = Part.makePolygon(pts)
    wire = Part.Wire(wire.Edges)
    return Part.Face(wire)

# Échelle
c_profil = max(p.x for p in airfoil_pts) - min(p.x for p in airfoil_pts)
scale_base = facteur_corde * moyeu_hauteur / c_profil
rayon_depart_pale = (trou_diametre/2) + marge_trou
angle_step = 360/nb_pales

# Moyeu
moyeu = Part.makeCylinder(moyeu_rayon, moyeu_hauteur)
moyeu.translate(Vector(0,0,-moyeu_hauteur/2))

pales = []

for i in range(nb_pales):
    sections = []
    for j in range(nb_sections):
        t = j/(nb_sections-1)
        radius = rayon_depart_pale + t*(rayon_bout - rayon_depart_pale)
        scale = scale_base*(1-0.2*t)
        # Décalage progressif base → pointe
        penetration = penetration_base*(1-t) + penetration_tip*t
        radius += -penetration
        sections.append(make_section(radius,scale))
    
    loft = Part.makeLoft(sections, True, False)
    pale = doc.addObject("Part::Feature", f"Pale_{i}")
    pale.Shape = loft

    # Rotation + pitch
    rotation_z = FreeCAD.Rotation(Vector(0,0,1), angle_step*i)
    rotation_x = FreeCAD.Rotation(Vector(1,0,0), -pitch_angle_deg)
    rotation = rotation_z.multiply(rotation_x)
    pale.Placement = FreeCAD.Placement(Vector(0,0,0), rotation)

    # Translation radiale après rotation
    decalage_radial = moyeu_rayon / 2
    translation_vector = rotation.multVec(Vector(decalage_radial,0,0))
    pale.Placement.Base = pale.Placement.Base + translation_vector

    pales.append(pale)

# Fusion
fusion = moyeu
for p in pales:
    if p.Shape.isValid():
        fusion = fusion.fuse(p.Shape)

# Perçage
trou_longueur = rayon_bout*2 + moyeu_hauteur
trou = Part.makeCylinder((trou_diametre/2)+0.2, trou_longueur)
trou.translate(Vector(0,0,-trou_longueur/2))
fusion = fusion.cut(trou)

Part.show(fusion)
doc.recompute()
print("✅ Hélice générée avec avancée progressive et fusionnée au moyeu.")
