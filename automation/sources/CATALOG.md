# CATALOG.md — Catalogue complet des sources

> Toutes les sources possibles pour alimenter TADA, classées par priorité et catégorie.

---

## Comment utiliser ce catalogue

1. **Bootstrap** : L'agent parcourt chaque catégorie par ordre de priorité
2. **Pour chaque source** : Demander si l'utilisateur l'utilise
3. **Si oui** : Configurer la source (voir fichier dédié ou créer depuis `_template.md`)
4. **Statut** : Tracker dans `TOOLS.md` quelles sources sont actives

---

## Priorité 1 — Core (Vie quotidienne)

Ces sources capturent l'essentiel de la vie active.

### 📧 Email
| Source | Fichier | Statut | Détection |
|--------|---------|--------|-----------|
| Gmail | [[email.md]] | 🟢 Documenté | Push (Pub/Sub) |
| Outlook/O365 | [[email.md]] | 🟢 Documenté | Push (Graph) |
| ProtonMail | — | 🔲 À créer | — |
| FastMail | — | 🔲 À créer | — |
| IMAP générique | [[email.md]] | 🟢 Documenté | IDLE polling |

### 📅 Calendar
| Source | Fichier | Statut | Détection |
|--------|---------|--------|-----------|
| Google Calendar | [[calendar.md]] | 🟢 Documenté | Push (Pub/Sub) |
| Outlook Calendar | [[calendar.md]] | 🟢 Documenté | Push (Graph) |
| Apple Calendar (CalDAV) | [[calendar.md]] | 🟢 Documenté | Polling |
| Calendly | — | 🔲 À créer | — |

### 👥 Contacts & CRM
| Source | Fichier | Statut | Détection |
|--------|---------|--------|-----------|
| Folk | [[folk.md]] | 🟢 Documenté | Webhook + Polling |
| Google Contacts | [[google-contacts.md]] | 🟢 Documenté | Polling (syncToken) |
| Apple Contacts | [[apple-contacts.md]] | 🟢 Documenté | Polling local |
| HubSpot | — | 🔲 À créer | — |
| Pipedrive | — | 🔲 À créer | — |
| Salesforce | — | 🔲 À créer | — |
| Attio | — | 🔲 À créer | — |
| LinkedIn Connections | — | 🔲 À créer | — |

### 🎙️ Meetings & Transcripts
| Source | Fichier | Statut | Détection |
|--------|---------|--------|-----------|
| Fireflies.ai | [[meetings.md]] | 🟢 Documenté | Webhook |
| Otter.ai | [[meetings.md]] | 🟢 Documenté | Webhook/Polling |
| Grain | — | 🔲 À créer | — |
| Fathom | — | 🔲 À créer | — |
| Zoom (recordings) | — | 🔲 À créer | — |
| Google Meet (recordings) | — | 🔲 À créer | — |

---

## Priorité 2 — Documents & Projets

Organisation et documentation.

### 📁 Fichiers & Cloud
| Source | Fichier | Statut | Détection |
|--------|---------|--------|-----------|
| Système local | [[files.md]] | 🟢 Documenté | Filesystem watch |
| Google Drive | [[google-drive.md]] | 🟢 Documenté | Push (Pub/Sub) |
| Dropbox | [[dropbox.md]] | 🟢 Documenté | Webhook |
| OneDrive | [[onedrive.md]] | 🟢 Documenté | Push (Graph) |
| iCloud Drive | [[icloud.md]] | 🟢 Documenté | Filesystem watch |
| Box | — | 🔲 À créer | — |
| NAS (Synology, etc.) | — | 🔲 À créer | — |

### 📝 Notes & Wikis
| Source | Fichier | Statut | Détection |
|--------|---------|--------|-----------|
| Notion | [[notion.md]] | 🟢 Documenté | Webhook |
| Obsidian | — | 🔲 À créer | — |
| Apple Notes | [[apple-notes.md]] | 🟢 Documenté | Polling SQLite |
| Bear | [[bear.md]] | 🟢 Documenté | Polling SQLite |
| Evernote | [[evernote.md]] | 🟢 Documenté | Polling API |
| Roam Research | — | 🔲 À créer | — |
| Logseq | — | 🔲 À créer | — |
| Confluence | — | 🔲 À créer | — |
| Coda | — | 🔲 À créer | — |

### 🎨 Boards & Visuel
| Source | Fichier | Statut | Détection |
|--------|---------|--------|-----------|
| Miro | [[miro.md]] | 🟢 Documenté | Webhook (Enterprise) |
| FigJam | — | 🔲 À créer | — |
| Mural | — | 🔲 À créer | — |
| Whimsical | — | 🔲 À créer | — |
| Figma | — | 🔲 À créer | — |

### ✅ Tâches & Projets
| Source | Fichier | Statut | Détection |
|--------|---------|--------|-----------|
| Things 3 | [[things3.md]] | 🟢 Documenté | Polling local |
| Todoist | [[todoist.md]] | 🟢 Documenté | Webhook |
| Apple Reminders | — | 🔲 À créer | — |
| Asana | [[asana.md]] | 🟢 Documenté | Webhook |
| Trello | [[trello.md]] | 🟢 Documenté | Webhook |
| Monday | — | 🔲 À créer | — |
| Linear | [[linear.md]] | 🟢 Documenté | Webhook |
| Jira | — | 🔲 À créer | — |
| GitHub Issues | — | 🔲 À créer | — |

---

## Priorité 3 — Communication étendue

Autres canaux de communication.

### 💬 Messagerie instantanée
| Source | Fichier | Statut | Détection |
|--------|---------|--------|-----------|
| WhatsApp | [[whatsapp.md]] | 🟢 Documenté | Webhook (Business) |
| Telegram | [[telegram.md]] | 🟢 Documenté | Webhook/MTProto |
| Signal | [[signal.md]] | 🟢 Documenté | Polling local |
| iMessage/SMS | [[messaging.md]] | 🟡 Template | Polling SQLite |
| Messenger | — | 🔲 À créer | — |
| Discord | [[discord.md]] | 🟢 Documenté | Gateway WS |

### 💼 Messagerie pro
| Source | Fichier | Statut | Détection |
|--------|---------|--------|-----------|
| Slack | [[slack.md]] | 🟢 Documenté | Events API/Socket |
| Teams | — | 🔲 À créer | — |
| Google Chat | — | 🔲 À créer | — |

### 📱 Réseaux sociaux DMs
| Source | Fichier | Statut | Détection |
|--------|---------|--------|-----------|
| LinkedIn DMs | — | 🔲 À créer | — |
| Twitter/X DMs | — | 🔲 À créer | — |
| Instagram DMs | — | 🔲 À créer | — |

---

## Priorité 4 — Finance & Admin

Données sensibles mais importantes.

### 💰 Finance
| Source | Fichier | Statut |
|--------|---------|--------|
| Relevés bancaires (PDF) | — | 🔲 À créer |
| Agrégateurs (Bankin, Linxo) | — | 🔲 À créer |
| Courtiers/Investissements | — | 🔲 À créer |
| Comptabilité (Pennylane, etc.) | — | 🔲 À créer |
| Factures (Stripe, PayPal) | — | 🔲 À créer |
| Crypto wallets | — | 🔲 À créer |

### 🏛️ Administratif & Légal
| Source | Fichier | Statut |
|--------|---------|--------|
| Notaires (actes, procurations) | — | 🔲 À créer |
| Impôts (déclarations) | — | 🔲 À créer |
| Assurances | — | 🔲 À créer |
| Entreprises (Kbis, statuts) | — | 🔲 À créer |

---

## Priorité 5 — Enrichissement

Données qui enrichissent le contexte.

### 📚 Lecture & Apprentissage
| Source | Fichier | Statut |
|--------|---------|--------|
| Kindle highlights | — | 🔲 À créer |
| Readwise | — | 🔲 À créer |
| Pocket/Instapaper | — | 🔲 À créer |
| Goodreads | — | 🔲 À créer |
| Podcasts (abonnements) | — | 🔲 À créer |
| RSS (Feedly) | — | 🔲 À créer |

### 📱 Social Media (public)
| Source | Fichier | Statut |
|--------|---------|--------|
| Twitter/X (posts, likes) | — | 🔲 À créer |
| LinkedIn (posts) | — | 🔲 À créer |
| Substack/Newsletter | — | 🔲 À créer |
| YouTube (uploads, playlists) | — | 🔲 À créer |

### 🏃 Santé & Bien-être
| Source | Fichier | Statut |
|--------|---------|--------|
| Apple Health | — | 🔲 À créer |
| Eight Sleep | — | 🔲 À créer |
| Oura / Whoop | — | 🔲 À créer |
| Strava | — | 🔲 À créer |
| Doctolib / DMP | — | 🔲 À créer |

### 📍 Localisation & Voyage
| Source | Fichier | Statut |
|--------|---------|--------|
| Google Maps Timeline | — | 🔲 À créer |
| TripIt | — | 🔲 À créer |
| Réservations (Booking, Airbnb) | — | 🔲 À créer |

### 📸 Photos & Media
| Source | Fichier | Statut |
|--------|---------|--------|
| Google Photos | — | 🔲 À créer |
| Apple Photos | — | 🔲 À créer |
| Screenshots | — | 🔲 À créer |

---

## Priorité 6 — Avancé

Sources techniques ou secondaires.

### 🌐 Navigation
| Source | Fichier | Statut |
|--------|---------|--------|
| Browser history | — | 🔲 À créer |
| Bookmarks | — | 🔲 À créer |
| Raindrop.io | — | 🔲 À créer |

### 🏠 Smart Home & IoT
| Source | Fichier | Statut |
|--------|---------|--------|
| Philips Hue | — | 🔲 À créer |
| Sonos | — | 🔲 À créer |
| HomeKit / Home Assistant | — | 🔲 À créer |

### 🔧 Dev & Tech
| Source | Fichier | Statut |
|--------|---------|--------|
| GitHub repos | — | 🔲 À créer |
| GitLab | — | 🔲 À créer |
| Serveurs/logs | — | 🔲 À créer |

### 🛒 Achats
| Source | Fichier | Statut |
|--------|---------|--------|
| Amazon orders | — | 🔲 À créer |
| Abonnements actifs | — | 🔲 À créer |

---

## Résumé des sources documentées

### ✅ Sources complètement documentées (26)

**Priorité 1 (Core) :**
- email.md, calendar.md, folk.md, google-contacts.md, apple-contacts.md, meetings.md

**Priorité 2 (Documents & Projets) :**
- files.md, google-drive.md, dropbox.md, onedrive.md, icloud.md
- notion.md, apple-notes.md, bear.md, evernote.md
- miro.md
- things3.md, todoist.md, asana.md, trello.md, linear.md

**Priorité 3 (Communication) :**
- whatsapp.md, telegram.md, signal.md, discord.md, slack.md, messaging.md

### 🔲 Sources restantes à documenter (~50+)

Voir les sections Priorité 4, 5, 6 ci-dessus.

---

## Processus Bootstrap

Lors du bootstrap d'un nouvel utilisateur :

```
1. Pour chaque PRIORITÉ (1 → 6) :
   a. Présenter la catégorie
   b. Pour chaque SOURCE de la catégorie :
      - "Utilises-tu [Source] ?"
      - Si oui → configurer (API, export, credentials)
      - Si non → passer
   c. Passer à la priorité suivante

2. Résumé des sources actives → TOOLS.md

3. Lancer la collecte initiale pour chaque source active
```

---

## Légende statuts

| Icône | Signification |
|-------|---------------|
| 🟢 | Documenté avec section détection |
| 🟡 | Template existe, à compléter |
| 🔲 | Pas encore de fichier, à créer si besoin |

---

*Ce catalogue est extensible. Ajouter une source = créer un fichier depuis `_template.md`.*
