<script>
  import { createEventDispatcher, onMount } from 'svelte'
  import { API_BASE } from '../config.js'

  export let token

  const dispatch = createEventDispatcher()

  let currentPath = []
  let items = []
  let loading = true
  let error = ''

  onMount(() => {
    loadRoot()
  })

  async function loadRoot() {
    loading = true
    error = ''

    try {
      const headers = { Authorization: `Bearer ${token}` }

      const [dashboardRes, projectsRes, pendingRes] = await Promise.all([
        fetch(`${API_BASE}/dashboard`, { headers }),
        fetch(`${API_BASE}/projects`, { headers }),
        fetch(`${API_BASE}/pending`, { headers })
      ])

      if (!dashboardRes.ok || !projectsRes.ok || !pendingRes.ok) {
        throw new Error('Erreur de chargement')
      }

      const dashboard = await dashboardRes.json()
      const projects = await projectsRes.json()
      const pending = await pendingRes.json()

      // Construire la liste des dossiers racine
      items = [
        {
          type: 'folder',
          icon: '📂',
          name: 'NOW',
          description: 'Projets actifs',
          count: dashboard.now_projects,
          path: ['NOW']
        },
        {
          type: 'folder',
          icon: '⏳',
          name: 'PENDING',
          description: 'En attente de tri',
          count: dashboard.pending_items,
          path: ['PENDING']
        },
        {
          type: 'folder',
          icon: '📦',
          name: 'ARCHIVE',
          description: 'Projets archivés',
          count: 0,
          path: ['ARCHIVE']
        }
      ]

      currentPath = []
    } catch (err) {
      error = err.message
      if (err.message.includes('401')) {
        dispatch('logout')
      }
    } finally {
      loading = false
    }
  }

  async function loadFolder(folderPath) {
    loading = true
    error = ''

    try {
      const headers = { Authorization: `Bearer ${token}` }

      if (folderPath[0] === 'NOW') {
        // Charger les projets NOW
        const response = await fetch(`${API_BASE}/projects`, { headers })
        if (!response.ok) throw new Error('Erreur de chargement')
        const projects = await response.json()

        items = projects.map(project => ({
          type: 'folder',
          icon: project.status || '⚪',
          name: project.name,
          description: project.has_index ? 'Projet avec index' : 'Projet',
          path: [...folderPath, project.name]
        }))

        currentPath = folderPath
      } else if (folderPath[0] === 'PENDING') {
        // Charger les items PENDING
        const response = await fetch(`${API_BASE}/pending`, { headers })
        if (!response.ok) throw new Error('Erreur de chargement')
        const pendingItems = await response.json()

        items = pendingItems.slice(0, 50).map(item => ({
          type: 'file',
          icon: getFileIcon(item.name),
          name: item.name,
          description: item.is_old ? `⚠️ ${item.age_days}j` : `${item.age_days}j`,
          path: [...folderPath, item.name]
        }))

        currentPath = folderPath
      } else {
        // ARCHIVE ou autre - pour l'instant vide
        items = []
        currentPath = folderPath
      }
    } catch (err) {
      error = err.message
      if (err.message.includes('401')) {
        dispatch('logout')
      }
    } finally {
      loading = false
    }
  }

  function getFileIcon(filename) {
    if (filename.endsWith('.md')) return '📝'
    if (filename.endsWith('.jpg') || filename.endsWith('.png') || filename.endsWith('.jpeg')) return '🖼️'
    if (filename.endsWith('.mp3') || filename.endsWith('.wav') || filename.endsWith('.webm')) return '🎤'
    if (filename.endsWith('.pdf')) return '📄'
    return '📄'
  }

  function handleItemClick(item) {
    if (item.type === 'folder') {
      loadFolder(item.path)
    }
    // Pour les fichiers, on pourrait ouvrir un aperçu mais pour l'instant on ne fait rien
  }

  function goBack() {
    if (currentPath.length === 0) return

    if (currentPath.length === 1) {
      loadRoot()
    } else {
      const parentPath = currentPath.slice(0, -1)
      loadFolder(parentPath)
    }
  }
</script>

<div class="explorer-container">
  {#if currentPath.length > 0}
    <div class="breadcrumb">
      <button class="back-btn" on:click={goBack}>
        ← Retour
      </button>
      <div class="path">
        {currentPath.join(' / ')}
      </div>
    </div>
  {/if}

  {#if loading}
    <div class="loading">Chargement...</div>
  {:else if error}
    <div class="error">{error}</div>
  {:else if items.length === 0}
    <div class="empty">Aucun élément</div>
  {:else}
    <div class="file-list">
      {#each items as item (item.path.join('/'))}
        <div
          class="file-item {item.type}"
          on:click={() => handleItemClick(item)}
        >
          <div class="file-icon {item.type}-icon">
            {item.icon}
          </div>
          <div class="file-info">
            <div class="file-name">{item.name}</div>
            <div class="file-path">{item.description}</div>
          </div>
          {#if item.count !== undefined}
            <div class="file-meta">{item.count}</div>
          {/if}
        </div>
      {/each}
    </div>
  {/if}
</div>

<style>
  .explorer-container {
    padding: 16px;
    padding-bottom: 80px;
  }

  .breadcrumb {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid #2a2a2a;
  }

  .back-btn {
    background: #2a2a2a;
    border: none;
    border-radius: 8px;
    color: #e0e0e0;
    padding: 8px 12px;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.2s;
  }

  .back-btn:active {
    background: #4a9eff;
    transform: scale(0.95);
  }

  .path {
    font-size: 14px;
    color: #888;
    font-weight: 500;
  }

  .file-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .file-item {
    background: linear-gradient(135deg, #1a1a1a 0%, #1f1f1f 100%);
    padding: 16px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    gap: 14px;
    border: 1px solid #2a2a2a;
    transition: all 0.2s;
    cursor: pointer;
  }

  .file-item:active {
    transform: scale(0.98);
    border-color: #4a9eff;
  }

  .file-item.folder {
    border-left: 3px solid #4a9eff;
  }

  .file-item.file {
    border-left: 3px solid #666;
  }

  .file-icon {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    flex-shrink: 0;
  }

  .file-icon.folder-icon {
    background: linear-gradient(135deg, #4a9eff22 0%, #4a9eff11 100%);
  }

  .file-icon.file-icon {
    background: linear-gradient(135deg, #66666622 0%, #66666611 100%);
  }

  .file-info {
    flex: 1;
    min-width: 0;
  }

  .file-name {
    font-size: 15px;
    font-weight: 600;
    color: #e0e0e0;
    margin-bottom: 4px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .file-path {
    font-size: 12px;
    color: #888;
  }

  .file-meta {
    font-size: 12px;
    color: #888;
    text-align: right;
    font-weight: 500;
    padding: 4px 10px;
    background: #2a2a2a;
    border-radius: 12px;
    flex-shrink: 0;
  }

  .loading, .error, .empty {
    text-align: center;
    padding: 40px;
    color: #888;
  }

  .error {
    color: #ff6b6b;
  }
</style>
