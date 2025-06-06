import os
import pdftotext

def extraire_textes_pdf(fichier_pdf, fichier_sortie):
    """
    Convertit un fichier PDF en texte et le sauvegarde dans un fichier TXT.
    """
    if not os.path.isfile(fichier_pdf):
        raise FileNotFoundError(f"Le fichier {fichier_pdf} n'existe pas.")

    # Supprimer le fichier s'il existe déjà
    if os.path.exists(fichier_sortie):
        os.remove(fichier_sortie)

    with open(fichier_pdf, "rb") as f:
        pdf = pdftotext.PDF(f)

    with open(fichier_sortie, "w", encoding="utf-8") as f:
        f.write("\n\n".join(pdf))

    print(f"✔ Conversion de {fichier_pdf} vers {fichier_sortie} terminée.")
