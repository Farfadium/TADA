---
A quoi sert ce fichier: Ajout d'une nouvelle source de capture — création du template de documentation, configuration MCP, test de connexion et mise à jour du fichier TOOLS.md
---

### Ajout d'une source

**Déclencheurs :**

| Type | Valeur |
|------|--------|
| Tag | `#source`, `#add-source` |
| Logique | Utilisateur demande d'ajouter une source de capture |

**Impact :** `Système`

**Contexte :**
Quand l'utilisateur veut connecter une nouvelle source de capture (email, calendrier, meetings, messaging, etc.), cette routine garantit que tout est configuré correctement.

**Actions :**

1. **Créer le fichier template** dans `_SYSTEM/2-Automate/sources/[source].md`
   - Utiliser `_template.md` comme base
   - Documenter le comportement générique de cette source
   - **Inclure obligatoirement :**
     - Format d'archivage (si applicable)
     - Règles de vérification des doublons
     - Stratégie de recherche par projet/parties prenantes
   - Ce fichier est agnostique (réutilisable sur toute instance TADA)

2. **Configurer le MCP** (si applicable)
   - Chercher si un MCP existe pour ce service
   - Ajouter la config dans `~/.claude.json` (section `mcpServers` du projet)
   - Demander les credentials à l'utilisateur

3. **Mettre à jour `local/TOOLS.md`**
   - Ajouter la section avec : Service, Compte, MCP, Statut
   - Noter la date de dernière vérification

4. **Tester la connexion**
   - Vérifier que le MCP fonctionne
   - Mettre à jour le statut dans `local/TOOLS.md`

5. **Logger** dans `local/logs.md`

**Validation requise :** Oui (pour les credentials et la config MCP)

**Checklist :**
- [ ] `_SYSTEM/2-Automate/sources/[source].md` créé
- [ ] MCP configuré dans `~/.claude.json`
- [ ] `_SYSTEM/local/TOOLS.md` mis à jour
- [ ] Connexion testée
- [ ] Statut = actif

**Exemple :**
```
Utilisateur : "Ajoute Fireflies comme source"

1. Créer _SYSTEM/2-Automate/sources/meetings.md
2. Configurer MCP Fireflies dans ~/.claude.json
3. Ajouter section Meetings dans local/TOOLS.md
4. Tester : mcp__fireflies__fireflies_get_user
5. Statut : actif
```
