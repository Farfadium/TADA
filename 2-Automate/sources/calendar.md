# Google Calendar — Source

## Config

```yaml
account: yvan.wibaux@gmail.com
api: Google Calendar API via gog CLI
```

## Filtres

```yaml
periode:
  debut: 2024-01-01
  fin: now

calendriers_inclus:
  - principal  # yvan.wibaux@gmail.com

calendriers_exclus:
  - "Anniversaires"
  - "Jours fériés en France"

filtres:
  duree_min: 5min
  exclure_declined: true
```

## Status

| Métrique | Valeur |
|----------|--------|
| Dernière sync | 2026-01-30 |
| Events collectés | 42,321 |
| Couverture | 2007-01 → 2026-02 |

## Issues

Aucune — ✅ Complet
