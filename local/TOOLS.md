# TOOLS.md - Local Notes

Skills define *how* tools work. This file is for *your* specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:
- Camera names and locations
- SSH hosts and aliases  
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras
- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH
- home-server → 192.168.1.100, user: admin

### TTS
- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

---

## Email

**Service :** Gmail
**Compte :** yvan.wibaux@gmail.com (+ redirection yvan@evaneos.com)
**MCP :** mcp__gmail
**Statut :** actif

**Dernière vérification :** 2026-01-27 15:30
**Inbox 0 :** _jamais_

**Configuration spécifique :**
- Labels projet : synchronisés avec DATA/NOW/
- Labels existants : Les Jaunets, Sidekicks, Evaneos, Investissements

---

## Messaging

**Service :** _non configuré_
**MCP :** —
**Statut :** inactif

**Proposé le :** —
**Réponse utilisateur :** —

---

## Calendar

**Service :** Google Calendar
**Compte :** yvan@evaneos.com
**MCP :** mcp__calendar
**Statut :** actif

**Dernière vérification :** 2026-01-27 20:20

**Configuration spécifique :**
- Calendrier principal : yvan@evaneos.com
- Calendriers partagés : Famille Wibaux, Evaneos Events

---

## Files

**Service :** Système de fichiers local
**MCP :** aucun (natif)
**Statut :** actif

**Dernière vérification :** _jamais_

---

## Meetings

**Service :** Fireflies.ai
**Compte :** yvan@evaneos.com
**MCP :** mcp__fireflies
**Statut :** actif

**Dernière vérification :** 2026-01-28 10:00

**Contenu :** Transcripts de tous les meetings

---

## Moltbot (TADA-Yvan)

**Nom :** TADA-Yvan
**Service :** Moltbot sur Hetzner
**Statut :** actif

**Serveur :**
- IP publique : 89.167.14.30
- IP Tailscale : 100.120.155.10
- User : clawdbot
- Accès : `ssh clawdbot@100.120.155.10`

**Canaux :**
- Telegram : @tada_yvan_bot (actif)
- Web UI : https://tada-yvan.[tailnet].ts.net

**Comptes Google liés :**
- yvan.wibaux@gmail.com (Gmail, Drive, Contacts)
- yvan@evaneos.com (Calendar)

**Voice :**
- STT : OpenAI Whisper API
- TTS : ElevenLabs

**Workspace :** ~/tada (sync git toutes les 5 min)

**Installé le :** 2026-01-29
