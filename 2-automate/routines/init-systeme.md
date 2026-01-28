### Initialisation système

**Déclencheurs :**

| Type | Valeur |
|------|--------|
| Logique | DATA/NOW/ vide ou presque vide |
| Tag | #setup |

**Impact :** Système

**Contexte :**
Quand le système TADA est nouveau ou peu rempli, tu guides l'utilisateur pour capturer toutes ses informations existantes. L'objectif est d'avoir un système complet et à jour dès le départ.

**Détection automatique :**
Tu proposes cette routine si tu détectes :
- Moins de 2 projets dans DATA/NOW/
- INBOX vide
- Première conversation

**Actions :**

1. **Identifier les projets en cours**
   - "Quels sont tes projets actifs en ce moment ?"
   - Une question à la fois, un projet à la fois
   - Pour chaque projet → lancer `#init [nom]`

2. **Vérifier INBOX**
   - Lister le contenu de DATA/INBOX/
   - Si vide : "As-tu des fichiers à mettre dans INBOX ? (documents en attente, factures, contrats...)"
   - Si fichiers présents → proposer de les trier

3. **Capturer les emails**
   - "Veux-tu qu'on regarde tes emails récents pour les trier ?"
   - Si oui → lancer `#emails`
   - Identifier les emails liés aux projets créés

4. **Identifier les contacts clés**
   - "Quelles sont les personnes avec qui tu travailles régulièrement ?"
   - Proposer de créer les fiches dans DATA/ARCHIVE/Répertoires/People/

5. **Récapitulatif**
   - Montrer ce qui a été créé
   - Proposer les prochaines actions

**Validation requise :** Oui (à chaque étape)

**Exemple :**
```
Je vois que ton système TADA est nouveau. Je vais t'aider à le remplir.

**Étape 1 — Tes projets actifs**

Quel est ton projet principal en ce moment ?
> Achat d'une maison à Bordeaux

→ Je lance #init Achat Maison Bordeaux
[... questions du #init ...]

As-tu un autre projet actif ?
> Oui, changement de travail

→ Je lance #init Changement Travail
[...]

As-tu d'autres projets ?
> Non

---

**Étape 2 — INBOX**

INBOX/ est vide. As-tu des fichiers à y déposer ?
- Documents en attente
- Factures à traiter
- Contrats à relire
- Notes diverses

> J'ai mis 3 fichiers

→ Je vois :
- devis_travaux.pdf
- cv_2026.pdf
- notes_reunion.md

On les trie ?

---

**Étape 3 — Emails**

Veux-tu qu'on regarde tes emails récents ?
> Oui

→ Je lance #emails
[...]

---

**Récapitulatif**

Système initialisé :
- 2 projets créés (Achat Maison, Changement Travail)
- 3 fichiers triés
- 12 emails traités
- 4 fiches contacts créées

Ton système TADA est prêt !
```
