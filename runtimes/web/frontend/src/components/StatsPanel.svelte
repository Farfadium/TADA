<script>
  import { createEventDispatcher } from 'svelte'
  import QuickCapture from './QuickCapture.svelte'

  export let stats = {}
  export let projects = []
  export let loading = false
  export let token = null

  const dispatch = createEventDispatcher()

  function formatDate(isoString) {
    if (!isoString) return 'Jamais'
    const date = new Date(isoString)
    const now = new Date()
    const diff = (now - date) / 1000 / 60  // minutes
    
    if (diff < 1) return 'À l\'instant'
    if (diff < 60) return `Il y a ${Math.floor(diff)} min`
    if (diff < 1440) return `Il y a ${Math.floor(diff / 60)}h`
    return date.toLocaleDateString('fr-FR', { day: 'numeric', month: 'short' })
  }
</script>

<div class="stats-panel">
  <div class="panel-header">
    <h2>📊 Stats</h2>
    <button class="refresh-btn" on:click={() => dispatch('refresh')} disabled={loading}>
      {loading ? '...' : '🔄'}
    </button>
  </div>

  <div class="content">
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">📋</div>
        <div class="stat-info">
          <div class="stat-value">{stats.now_projects || 0}</div>
          <div class="stat-label">Projets actifs</div>
        </div>
      </div>

      <div class="stat-card" class:warning={stats.pending_old > 0}>
        <div class="stat-icon">⏳</div>
        <div class="stat-info">
          <div class="stat-value">{stats.pending_items || 0}</div>
          <div class="stat-label">
            En attente
            {#if stats.pending_old > 0}
              <span class="badge">{stats.pending_old} vieux</span>
            {/if}
          </div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">📁</div>
        <div class="stat-info">
          <div class="stat-value">{stats.total_files || 0}</div>
          <div class="stat-label">Fichiers total</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">🧠</div>
        <div class="stat-info">
          <div class="stat-value">{stats.memory_files || 0}</div>
          <div class="stat-label">Notes mémoire</div>
        </div>
      </div>
    </div>

    <div class="sync-info">
      <span class="sync-label">Dernière sync:</span>
      <span class="sync-value">{formatDate(stats.last_sync)}</span>
    </div>

    {#if projects.length > 0}
      <div class="projects-section">
        <h3>Projets</h3>
        <div class="projects-list">
          {#each projects.slice(0, 8) as project}
            <div class="project-item">
              <span class="project-status">{project.status || '⚪'}</span>
              <span class="project-name">{project.name}</span>
              <span class="project-count">{project.file_count}</span>
            </div>
          {/each}
          {#if projects.length > 8}
            <div class="more">+{projects.length - 8} autres</div>
          {/if}
        </div>
      </div>
    {/if}

    {#if token}
      <div class="capture-section">
        <QuickCapture {token} compact on:success={() => dispatch('refresh')} />
      </div>
    {/if}
  </div>
</div>

<style>
  .stats-panel {
    display: flex;
    flex-direction: column;
    height: 100%;
  }

  .panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 16px;
    border-bottom: 1px solid #222;
    flex-shrink: 0;
  }

  h2 {
    margin: 0;
    font-size: 16px;
    font-weight: 600;
  }

  .refresh-btn {
    padding: 4px 8px;
    background: transparent;
    border: 1px solid #333;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
  }

  .refresh-btn:hover:not(:disabled) {
    background: #222;
  }

  .content {
    flex: 1;
    overflow-y: auto;
    padding: 16px;
  }

  .stats-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-bottom: 16px;
  }

  .stat-card {
    background: #111;
    padding: 12px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    gap: 10px;
    border: 1px solid #222;
  }

  .stat-card.warning {
    border-color: #5a3a1a;
  }

  .stat-icon {
    font-size: 24px;
  }

  .stat-value {
    font-size: 24px;
    font-weight: 700;
    line-height: 1;
  }

  .stat-label {
    font-size: 11px;
    color: #666;
    margin-top: 2px;
  }

  .badge {
    background: #5a3a1a;
    padding: 1px 4px;
    border-radius: 3px;
    font-size: 10px;
    color: #ffa500;
  }

  .sync-info {
    display: flex;
    justify-content: space-between;
    padding: 8px 0;
    border-top: 1px solid #222;
    border-bottom: 1px solid #222;
    margin-bottom: 16px;
    font-size: 12px;
  }

  .sync-label {
    color: #666;
  }

  .sync-value {
    color: #888;
  }

  .projects-section {
    margin-bottom: 16px;
  }

  h3 {
    font-size: 12px;
    font-weight: 600;
    color: #666;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 0 0 8px 0;
  }

  .projects-list {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .project-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 8px;
    background: #111;
    border-radius: 4px;
    font-size: 13px;
  }

  .project-status {
    font-size: 12px;
  }

  .project-name {
    flex: 1;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .project-count {
    font-size: 11px;
    color: #555;
  }

  .more {
    text-align: center;
    font-size: 12px;
    color: #555;
    padding: 4px;
  }

  .capture-section {
    padding-top: 12px;
    border-top: 1px solid #222;
  }
</style>
