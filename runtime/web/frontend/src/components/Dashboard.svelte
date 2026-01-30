<script>
  import { onMount, createEventDispatcher } from 'svelte'
  import QuickCapture from './QuickCapture.svelte'

  export let token

  const dispatch = createEventDispatcher()

  let stats = {
    now_projects: 0,
    pending_items: 0,
    pending_old: 0,
    last_sync: null,
  }
  let projects = []
  let pendingItems = []
  let loading = true
  let error = ''

  const API_BASE = 'http://localhost:8080'

  async function fetchData() {
    loading = true
    error = ''

    try {
      const headers = { Authorization: `Bearer ${token}` }

      const [statsRes, projectsRes, pendingRes] = await Promise.all([
        fetch(`${API_BASE}/dashboard`, { headers }),
        fetch(`${API_BASE}/projects`, { headers }),
        fetch(`${API_BASE}/pending`, { headers }),
      ])

      if (!statsRes.ok || !projectsRes.ok || !pendingRes.ok) {
        throw new Error('Erreur de chargement')
      }

      stats = await statsRes.json()
      projects = await projectsRes.json()
      pendingItems = await pendingRes.json()
    } catch (err) {
      error = err.message
      if (err.message.includes('401')) {
        dispatch('logout')
      }
    } finally {
      loading = false
    }
  }

  function handleCaptureSuccess() {
    fetchData() // Recharger après capture
  }

  onMount(() => {
    fetchData()
  })
</script>

<div class="container">
  <header>
    <h1>TADA</h1>
    <button class="logout" on:click={() => dispatch('logout')}>
      Déconnexion
    </button>
  </header>

  {#if loading}
    <p class="loading">Chargement...</p>
  {:else if error}
    <p class="error">{error}</p>
  {:else}
    <div class="stats">
      <div class="stat">
        <span class="icon">📊</span>
        <div>
          <div class="stat-value">{stats.now_projects}</div>
          <div class="stat-label">Projets actifs</div>
        </div>
      </div>

      <div class="stat" class:warning={stats.pending_old > 0}>
        <span class="icon">⚠️</span>
        <div>
          <div class="stat-value">{stats.pending_items}</div>
          <div class="stat-label">
            En attente
            {#if stats.pending_old > 0}
              <span class="badge">{stats.pending_old} > 7j</span>
            {/if}
          </div>
        </div>
      </div>
    </div>

    <QuickCapture {token} on:success={handleCaptureSuccess} />

    {#if projects.length > 0}
      <section class="section">
        <h2>Projets actifs</h2>
        <div class="projects">
          {#each projects as project}
            <div class="project-card">
              <span class="status">{project.status || '⚪'}</span>
              <span class="name">{project.name}</span>
            </div>
          {/each}
        </div>
      </section>
    {/if}

    {#if pendingItems.length > 0}
      <section class="section">
        <h2>En attente</h2>
        <div class="pending-list">
          {#each pendingItems as item}
            <div class="pending-item" class:old={item.is_old}>
              <span class="name">{item.name}</span>
              <span class="age">{item.age_days.toFixed(1)}j</span>
            </div>
          {/each}
        </div>
      </section>
    {/if}
  {/if}
</div>

<style>
  .container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
  }

  header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 32px;
  }

  h1 {
    font-size: 32px;
    font-weight: 700;
  }

  .logout {
    padding: 8px 16px;
    background: #2a2a2a;
    border: 1px solid #3a3a3a;
    border-radius: 4px;
    color: #e0e0e0;
    cursor: pointer;
    font-size: 14px;
  }

  .logout:hover {
    background: #3a3a3a;
  }

  .stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
    margin-bottom: 32px;
  }

  .stat {
    background: #1a1a1a;
    padding: 20px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    gap: 16px;
  }

  .stat.warning {
    border: 1px solid #ff6b6b;
  }

  .icon {
    font-size: 32px;
  }

  .stat-value {
    font-size: 32px;
    font-weight: 700;
  }

  .stat-label {
    color: #888;
    font-size: 14px;
  }

  .badge {
    background: #ff6b6b;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 12px;
    margin-left: 4px;
  }

  .section {
    margin-bottom: 32px;
  }

  h2 {
    font-size: 20px;
    margin-bottom: 16px;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-size: 12px;
  }

  .projects {
    display: grid;
    gap: 12px;
  }

  .project-card {
    background: #1a1a1a;
    padding: 16px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .status {
    font-size: 20px;
  }

  .name {
    font-size: 16px;
  }

  .pending-list {
    display: grid;
    gap: 8px;
  }

  .pending-item {
    background: #1a1a1a;
    padding: 12px;
    border-radius: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .pending-item.old {
    border-left: 3px solid #ff6b6b;
  }

  .age {
    color: #888;
    font-size: 14px;
  }

  .loading, .error {
    text-align: center;
    padding: 40px;
    color: #888;
  }

  .error {
    color: #ff6b6b;
  }
</style>
