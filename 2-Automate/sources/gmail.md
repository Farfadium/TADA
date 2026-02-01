# Gmail — Source

## Config

```yaml
account: yvan.wibaux@gmail.com
api: Gmail API via gog CLI
```

## Filtres

```yaml
periode:
  debut: 2024-01-01
  fin: now

labels_inclus:
  - INBOX
  - Important
  - Starred
  - Sent

labels_exclus:
  - Promotions
  - Social
  - Spam
  - Updates

expediteurs_prioritaires:
  - "*@evaneos.com"
  - "*@sidekicks.fr"
  - "*@theodo.fr"

attachments:
  min_size: 10KB
  exclude_inline: true
  exclude_extensions: [.ics, .vcf]
```

## Status

| Métrique | Valeur |
|----------|--------|
| Dernière sync | 2026-01-30 |
| Emails collectés | 12,567 |
| Attachments | 1,892 téléchargés / 635 manquants |
| Couverture | 2023-06 → 2026-01 |

## Issues

- ⚠️ 635 attachments manquants (erreurs téléchargement)
