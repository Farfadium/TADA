<script>
  import { onMount, createEventDispatcher } from 'svelte'
  import ChatPanel from './ChatPanel.svelte'
  import FilesPanel from './FilesPanel.svelte'
  import StatsPanel from './StatsPanel.svelte'
  import { API_BASE } from '../config.js'

  export let token

  const dispatch = createEventDispatcher()

  let stats = {}
  let projects = []
  let loading = true

  async function fetchData() {
    loading = true
    try {
      const headers = { Authorization: `Bearer ${token}` }
      const [statsRes, projectsRes] = await Promise.all([
        fetch(`${API_BASE}/dashboard`, { headers }),
        fetch(`${API_BASE}/projects`, { headers }),
      ])

      if (!statsRes.ok || !projectsRes.ok) {
        if (statsRes.status === 401 || projectsRes.status === 401) {
          dispatch('logout')
          return
        }
        throw new Error('Erreur de chargement')
      }

      stats = await statsRes.json()
      projects = await projectsRes.json()
    } catch (err) {
      console.error(err)
    } finally {
      loading = false
    }
  }

  onMount(() => {
    fetchData()
    // Refresh toutes les 30s
    const interval = setInterval(fetchData, 30000)
    return () => clearInterval(interval)
  })
</script>

<div class="app">
  <header>
    <div class="logo">
      <span class="logo-icon">📋</span>
      <span class="logo-text">TADA</span>
    </div>
    <button class="logout" on:click={() => dispatch('logout')}>
      Déconnexion
    </button>
  </header>

  <main class="panels">
    <div class="panel chat-panel">
      <ChatPanel {token} />
    </div>
    
    <div class="panel files-panel">
      <FilesPanel {token} />
    </div>
    
    <div class="panel stats-panel">
      <StatsPanel {stats} {projects} {loading} {token} on:refresh={fetchData} />
    </div>
  </main>
</div>

<style>
  .app {
    height: 100vh;
    display: flex;
    flex-direction: column;
    background: #0a0a0a;
    color: #e0e0e0;
  }

  header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 20px;
    background: #111;
    border-bottom: 1px solid #222;
    flex-shrink: 0;
  }

  .logo {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .logo-icon {
    font-size: 24px;
  }

  .logo-text {
    font-size: 20px;
    font-weight: 700;
    letter-spacing: 2px;
  }

  .logout {
    padding: 6px 12px;
    background: transparent;
    border: 1px solid #333;
    border-radius: 4px;
    color: #888;
    cursor: pointer;
    font-size: 13px;
    transition: all 0.2s;
  }

  .logout:hover {
    background: #222;
    color: #fff;
    border-color: #444;
  }

  main.panels {
    flex: 1;
    display: grid;
    grid-template-columns: 1fr 1fr 300px;
    gap: 1px;
    background: #222;
    overflow: hidden;
  }

  .panel {
    background: #0a0a0a;
    overflow: hidden;
    display: flex;
    flex-direction: column;
  }

  /* Mobile */
  @media (max-width: 1200px) {
    main.panels {
      grid-template-columns: 1fr 1fr;
      grid-template-rows: 1fr auto;
    }
    
    .stats-panel {
      grid-column: span 2;
      max-height: 200px;
    }
  }

  @media (max-width: 768px) {
    main.panels {
      grid-template-columns: 1fr;
      grid-template-rows: 1fr 1fr auto;
    }
    
    .stats-panel {
      grid-column: span 1;
    }
  }
</style>
