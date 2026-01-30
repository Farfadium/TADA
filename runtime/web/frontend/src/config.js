// API configuration
// Utilise localhost en dev, chemins relatifs en production (via nginx proxy)
export const API_BASE = window.location.hostname === 'localhost'
  ? 'http://localhost:8080'
  : window.location.origin
