# Agents TADA

> Implémentation des agents spécialisés.

Voir [1-Trust/AGENTS.md](../1-Trust/AGENTS.md) pour l'architecture globale.

## Agents implémentés

| Agent | Statut | Dossier | Mission |
|-------|--------|---------|---------|
| 🌟 Cassiopée | ✅ Principal | — | Interface Yvan, orchestration |
| 🗂️ Curateur | ✅ Prêt | [curateur/](curateur/) | Structure DATA |
| 🔌 Collecteur | ✅ Prêt | [collecteur/](collecteur/) | Fait rentrer la donnée |
| 📝 Scribe | ✅ Prêt | [scribe/](scribe/) | Mémoire (USER.md, daily notes) |
| 🔧 Tech Lead | ✅ Prêt | [tech-lead/](tech-lead/) | Maintient _SYSTEM |
| 🛡️ Gardien | ✅ Prêt | [gardien/](gardien/) | QA, vérifie, alerte |

## Structure d'un agent

```
agents/
  curateur/
    SOUL.md           # Personnalité, mission, principes
    HEARTBEAT.md      # Checks spécifiques
    METHODOLOGY.md    # Manuel de travail (tri PENDING)
    STRUCTURE.md      # Structure TADA validée
    CALENDAR.md       # Convention calendrier (hub quotidien)
    
  collecteur/
    SOUL.md           # Personnalité, mission
    DATA-COLLECTION.md # Manuel de collecte
```

## Lancement

Les agents sont lancés via :
- **Cron Moltbot** : session isolée avec le SOUL de l'agent
- **Sub-agent spawn** : `sessions_spawn(task="...", label="curateur")`
- **Heartbeat dédié** : mode différencié dans le heartbeat principal
