---
A quoi sert ce fichier:
Système de liens Obsidian — Règles pour créer liens [[Nom]], maintenir répertoires People/Entreprises/Concepts, enrichir fiches (recherche web, photos, logos)
---

## Liens

Tu connectes les informations entre elles avec des liens.

**Syntaxe Obsidian — tu utilises :**
- Lien simple : `[[Prénom Nom]]`
- Lien avec alias : `[[Prénom Nom|texte affiché]]`

**Répertoires de référence :**
| Type | Emplacement |
|------|-------------|
| Personnes | `DATA/ARCHIVE/Répertoires/People/` |
| Entreprises | `DATA/ARCHIVE/Répertoires/Entreprise/` |
| Concepts | `DATA/ARCHIVE/Répertoires/Concepts/` |

**Quand tu mentionnes quelqu'un ou une entreprise :**
1. Vérifier si la fiche existe dans le répertoire (Glob avant de créer)
2. Si non → créer la fiche immédiatement avec les infos disponibles
3. Créer le lien `[[Prénom Nom]]` dans le document

**Tu crées une fiche automatiquement quand :**
- Une personne est mentionnée dans un projet actif
- Une entreprise est impliquée dans un projet
- Un concept revient régulièrement

**Contenu minimum d'une fiche personne :**
- Relation avec l'utilisateur
- Projets liés
- Infos de contact si connues

**Enrichissement des fiches :**
Quand tu crées une fiche, tu cherches à l'enrichir :
1. **Recherche web** : site personnel, LinkedIn, entreprise (si publiquement disponible)
2. **Photo** : télécharger depuis source publique (site perso, site entreprise, etc.)
   - Stockage : `DATA/ARCHIVE/Répertoires/People/_photos/Prénom_Nom.jpg`
   - Référence dans la fiche : `![[_photos/Prénom_Nom.jpg|200]]`
3. **Infos métier** : titre, entreprise, localisation

**Limites :**
- LinkedIn bloque souvent les accès directs → utiliser d'autres sources
- Ne pas inventer d'informations — si rien trouvé, laisser la fiche minimale

**Enrichissement des fiches entreprises :**
Quand tu crées une fiche entreprise, tu cherches à l'enrichir :
1. **Site web** : URL officiel
2. **Logo** : télécharger depuis le site officiel
   - Stockage : `DATA/ARCHIVE/Répertoires/Entreprises/_logos/Nom_Entreprise.png`
   - Référence dans la fiche : `![[_logos/Nom_Entreprise.png|200]]`
3. **Infos clés** : type, groupe, siège

**Tu ne stockes rien dans ta mémoire.** Ce qui n'est pas écrit dans un fichier n'existe pas.
