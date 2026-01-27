### Mise à jour index

**Déclencheurs :**

| Type | Valeur |
|------|--------|
| Logique | Fichier ajouté ou supprimé |
| Tag | #maj-index |

**Contexte :**
Chaque dossier a un `index.md` qui liste son contenu. Cette routine parcourt tous les index et les synchronise avec le contenu réel.

**Actions :**

1. **Parcourir les dossiers principaux :**
   - NOW/ (projets actifs)
   - PENDING/ (en attente)
   - ARCHIVE/ (consultation)
   - GARDEN/ (idées)

2. **Pour chaque dossier avec un index.md :**
   - Lire l'index existant
   - Lister le contenu réel du dossier
   - Comparer et détecter les différences :
     - Fichiers présents mais pas dans l'index
     - Fichiers dans l'index mais supprimés
     - Informations obsolètes (statut, dates)

3. **Proposer les mises à jour :**
   - Montrer le diff pour chaque index
   - Regrouper par dossier

4. **Appliquer après validation**

**Validation requise :** Oui (par dossier ou global)

**Exemple :**
```
#maj-index

Je parcours tous les index...

---

**NOW/Achat Maison/index.md**
+ | 2026-01-27_Compromis_Signe.pdf | Compromis signé |
+ Statut : Compromis signé → en attente acte définitif

**NOW/Changement Travail/index.md**
(à jour)

**PENDING/index.md**
- | 2026-01-10_Devis_Travaux.pdf | (déplacé vers ARCHIVE) |

**ARCHIVE/Répertoires/People/index.md**
+ | [[Jean Dupont]] | Notaire |

---

3 index à mettre à jour. Valider tout ?
```

**Mode rapide :**
Si tu détectes un changement ponctuel (un fichier ajouté), tu proposes directement la mise à jour de l'index concerné sans parcourir tout le système.
