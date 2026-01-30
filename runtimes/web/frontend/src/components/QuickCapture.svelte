<script>
  import { createEventDispatcher } from 'svelte'
  import { API_BASE } from '../config.js'

  export let token
  export let compact = false

  const dispatch = createEventDispatcher()

  let content = ''
  let loading = false

  async function handleSubmit() {
    if (!content.trim()) return

    loading = true

    try {
      const response = await fetch(`${API_BASE}/capture`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ content }),
      })

      if (!response.ok) {
        throw new Error('Erreur lors de la capture')
      }

      await response.json()
      content = ''
      dispatch('success')
    } catch (err) {
      alert(err.message)
    } finally {
      loading = false
    }
  }

  function handleKeydown(e) {
    if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) {
      e.preventDefault()
      handleSubmit()
    }
  }
</script>

<div class="capture-box" class:compact>
  {#if !compact}
    <h3>💡 Capture rapide</h3>
  {/if}

  <form on:submit|preventDefault={handleSubmit}>
    <textarea
      bind:value={content}
      on:keydown={handleKeydown}
      placeholder={compact ? "Capture rapide... (⌘+Enter)" : "Note, idée, tâche...\n@projet #tag [[lien]]"}
      disabled={loading}
      rows={compact ? 2 : 3}
    />

    <button type="submit" disabled={loading || !content.trim()}>
      {#if loading}
        ⏳
      {:else}
        {compact ? '➤' : 'Capturer'}
      {/if}
    </button>
  </form>

  {#if !compact}
    <div class="hint">
      <code>@projet</code> <code>#tag</code> <code>[[lien]]</code>
    </div>
  {/if}
</div>

<style>
  .capture-box {
    background: #111;
    padding: 12px;
    border-radius: 8px;
  }

  .capture-box.compact {
    padding: 0;
    background: transparent;
  }

  h3 {
    font-size: 14px;
    font-weight: 600;
    margin: 0 0 10px 0;
  }

  form {
    display: flex;
    gap: 8px;
  }

  .compact form {
    flex-direction: column;
  }

  textarea {
    flex: 1;
    padding: 8px 10px;
    background: #1a1a1a;
    border: 1px solid #333;
    border-radius: 6px;
    color: #e0e0e0;
    font-size: 13px;
    font-family: inherit;
    resize: none;
    line-height: 1.4;
  }

  .compact textarea {
    font-size: 12px;
    padding: 6px 8px;
  }

  textarea:focus {
    outline: none;
    border-color: #4a9eff;
  }

  textarea:disabled {
    opacity: 0.6;
  }

  button {
    padding: 8px 16px;
    background: #4a9eff;
    border: none;
    border-radius: 6px;
    color: white;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    white-space: nowrap;
  }

  .compact button {
    align-self: flex-end;
    padding: 6px 12px;
    font-size: 12px;
  }

  button:hover:not(:disabled) {
    background: #3a8eef;
  }

  button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .hint {
    margin-top: 8px;
    font-size: 11px;
    color: #555;
  }

  code {
    background: #1a1a1a;
    padding: 1px 4px;
    border-radius: 3px;
    font-family: monospace;
  }
</style>
