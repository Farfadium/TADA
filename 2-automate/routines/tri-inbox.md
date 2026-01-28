### Tri INBOX

**Déclencheurs :**

| Type | Valeur |
|------|--------|
| Temps | 7j sans tri |
| Logique | Fichier déposé dans DATA/INBOX/ |

**Impact :** Contenu

**Contexte :**
L'INBOX est le point d'entrée unique. Tout fichier qui y arrive doit être trié vers son emplacement définitif.

**Actions :**

1. Lister les fichiers dans `DATA/INBOX/`
2. Pour chaque fichier :
   - Identifier le type (document projet, archive, en attente de décision)
   - Proposer un emplacement :
     - `DATA/NOW/[Projet]/` → document lié à un projet actif
     - `DATA/ARCHIVE/` → document de consultation
     - `DATA/PENDING/` → en attente d'une décision externe
   - Proposer un renommage si nécessaire (convention `YYYY-MM-DD_HHMM_Nom.ext`)
3. Attendre validation avant chaque déplacement

**Validation requise :** Oui (chaque déplacement)

**Exemple :**
```
INBOX/ contient : facture_electricite.pdf

→ Proposition :
  - Type : Facture
  - Destination : DATA/ARCHIVE/Administratif/Factures/
  - Renommage : 2026-01-27_Facture_Electricite.pdf

Valider ? (oui/non)
```
