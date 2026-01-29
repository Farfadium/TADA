---
A quoi sert ce fichier: Routine de tri des emails récents — labellisation Gmail, téléchargement des pièces jointes, mise à jour des projets et archivage systématique
---

### Tri emails

**Déclencheurs :**

| Type | Valeur |
|------|--------|
| Tag | #emails |

**Impact :** Contenu, Externe

**Contexte :**
Trier les emails non lus ou récents pour les router vers les bons projets et archiver.

**Actions :**

1. Rechercher les emails récents (via MCP Gmail)
2. Présenter chaque email au format ci-dessous
3. Proposer les actions pour chaque email
4. Exécuter après validation
5. Si tous les emails ont été traités → mettre à jour "Inbox 0" avec date+heure dans `local/TOOLS.md`

**Format de présentation :**
```
**Email X/Y** — Expéditeur | Sujet | date relative

> Résumé du contenu (2-3 lignes max)

**Actions proposées :**
- Label : [nom du projet si applicable]
- PJ : [destination si pièce jointe à stocker]
- Gmail : [archiver / marquer lu / créer brouillon réponse]
- TADA : [mettre à jour projet / créer tâche / rien]
```

**Actions possibles :**
- Appliquer un label Gmail (= projet actif, voir `DATA/NOW/index.md`)
- Archiver l'email
- Télécharger les PJ vers le dossier projet
- Créer un brouillon de réponse
- Mettre à jour un index de projet

**Validation requise :** Oui (par lot ou par email)

**Exemple :**
```
**Email 1/3** — notaire@office.fr | Compromis signé | il y a 2h

> Le compromis a été signé par toutes les parties.
> Document en PJ.

**Actions proposées :**
- Label : Achat Maison
- PJ : DATA/NOW/Achat Maison/2026-01-27_Compromis_Signe.pdf
- Gmail : archiver
- TADA : mettre à jour statut dans DATA/NOW/Achat Maison/index.md

Valider ?
```
