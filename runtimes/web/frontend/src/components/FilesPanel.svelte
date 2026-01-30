<script>
  import { onMount } from 'svelte'
  import { API_BASE } from '../config.js'

  export let token

  let tree = null
  let loading = true
  let selectedFile = null
  let fileContent = null
  let loadingContent = false
  let expandedPaths = new Set(['', 'DATA', '_SYSTEM'])

  async function fetchTree() {
    loading = true
    try {
      const response = await fetch(`${API_BASE}/files/tree`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      if (response.ok) {
        tree = await response.json()
      }
    } catch (err) {
      console.error(err)
    } finally {
      loading = false
    }
  }

  async function loadFile(path) {
    if (selectedFile === path) {
      selectedFile = null
      fileContent = null
      return
    }

    selectedFile = path
    loadingContent = true

    try {
      const response = await fetch(`${API_BASE}/files/content?path=${encodeURIComponent(path)}`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      if (response.ok) {
        fileContent = await response.json()
      } else {
        fileContent = { error: 'Impossible de charger le fichier' }
      }
    } catch (err) {
      fileContent = { error: err.message }
    } finally {
      loadingContent = false
    }
  }

  function toggleExpand(path) {
    if (expandedPaths.has(path)) {
      expandedPaths.delete(path)
    } else {
      expandedPaths.add(path)
    }
    expandedPaths = new Set(expandedPaths)
  }

  function getIcon(item) {
    if (item.type === 'dir') {
      return expandedPaths.has(item.path) ? '📂' : '📁'
    }
    const ext = (item.ext || '').toLowerCase()
    if (ext === '.md') return '📝'
    if (ext === '.json') return '📋'
    if (ext === '.py') return '🐍'
    if (ext === '.js' || ext === '.ts') return '📜'
    if (['.jpg', '.jpeg', '.png', '.gif', '.webp'].includes(ext)) return '🖼️'
    if (['.mp3', '.wav', '.webm', '.ogg'].includes(ext)) return '🎵'
    return '📄'
  }

  function formatSize(bytes) {
    if (!bytes) return ''
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
  }

  function flattenTree(node, depth = 0) {
    if (!node) return []
    let items = []
    
    if (node.children) {
      for (const child of node.children) {
        items.push({ ...child, depth })
        if (child.type === 'dir' && expandedPaths.has(child.path)) {
          items = items.concat(flattenTree(child, depth + 1))
        }
      }
    }
    return items
  }

  $: flatItems = tree ? flattenTree(tree) : []

  onMount(() => {
    fetchTree()
  })
</script>

<div class="files-panel">
  <div class="panel-header">
    <h2>📁 Fichiers</h2>
    <button class="refresh-btn" on:click={fetchTree} disabled={loading}>
      🔄
    </button>
  </div>

  <div class="content-area">
    <div class="tree-view" class:has-preview={fileContent}>
      {#if loading}
        <div class="status">Chargement...</div>
      {:else if !tree}
        <div class="status">Aucun fichier</div>
      {:else}
        <div class="tree">
          {#each flatItems as item (item.path)}
            <div 
              class="tree-item"
              class:selected={selectedFile === item.path}
              style="padding-left: {12 + item.depth * 16}px"
              on:click={() => item.type === 'dir' ? toggleExpand(item.path) : loadFile(item.path)}
              on:keydown={(e) => e.key === 'Enter' && (item.type === 'dir' ? toggleExpand(item.path) : loadFile(item.path))}
              role="button"
              tabindex="0"
            >
              <span class="icon">{getIcon(item)}</span>
              <span class="name">{item.name}</span>
              {#if item.type === 'file' && item.size}
                <span class="meta">{formatSize(item.size)}</span>
              {/if}
              {#if item.type === 'dir' && item.count}
                <span class="meta">{item.count}</span>
              {/if}
            </div>
          {/each}
        </div>
      {/if}
    </div>

    {#if fileContent}
      <div class="preview">
        <div class="preview-header">
          <span class="preview-title">{fileContent.name || selectedFile}</span>
          <button class="close-btn" on:click={() => { selectedFile = null; fileContent = null }}>✕</button>
        </div>
        <div class="preview-content">
          {#if loadingContent}
            <div class="status">Chargement...</div>
          {:else if fileContent.error}
            <div class="error">{fileContent.error}</div>
          {:else}
            <pre>{fileContent.content}</pre>
          {/if}
        </div>
      </div>
    {/if}
  </div>
</div>

<style>
  .files-panel {
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

  .refresh-btn:disabled {
    opacity: 0.5;
  }

  .content-area {
    flex: 1;
    display: flex;
    overflow: hidden;
  }

  .tree-view {
    flex: 1;
    overflow-y: auto;
    padding: 8px 0;
  }

  .tree-view.has-preview {
    width: 50%;
    flex: none;
    border-right: 1px solid #222;
  }

  .tree {
    font-size: 13px;
  }

  .tree-item {
    cursor: pointer;
    padding: 5px 12px;
    display: flex;
    align-items: center;
    gap: 6px;
    user-select: none;
    transition: background 0.1s;
  }

  .tree-item:hover {
    background: #1a1a1a;
  }

  .tree-item.selected {
    background: #1a3a5c;
  }

  .icon {
    font-size: 14px;
    flex-shrink: 0;
  }

  .name {
    flex: 1;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .meta {
    font-size: 11px;
    color: #555;
    flex-shrink: 0;
  }

  .status, .error {
    padding: 20px;
    text-align: center;
    color: #666;
  }

  .error {
    color: #ff6b6b;
  }

  .preview {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    min-width: 0;
  }

  .preview-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 12px;
    background: #111;
    border-bottom: 1px solid #222;
    flex-shrink: 0;
  }

  .preview-title {
    font-size: 13px;
    font-weight: 500;
    color: #888;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .close-btn {
    padding: 2px 6px;
    background: transparent;
    border: none;
    color: #666;
    cursor: pointer;
    font-size: 14px;
  }

  .close-btn:hover {
    color: #fff;
  }

  .preview-content {
    flex: 1;
    overflow: auto;
    padding: 12px;
  }

  pre {
    margin: 0;
    font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
    font-size: 12px;
    line-height: 1.5;
    white-space: pre-wrap;
    word-break: break-word;
    color: #ccc;
  }
</style>
