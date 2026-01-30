<script>
  import { onMount, tick } from 'svelte'
  import { API_BASE } from '../config.js'

  export let token
  export let runtime = 'claude'

  let messages = []
  let input = ''
  let loading = false
  let messagesContainer
  let runtimes = []

  async function fetchRuntimes() {
    try {
      const response = await fetch(`${API_BASE}/runtimes`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      if (response.ok) {
        const data = await response.json()
        runtimes = data.runtimes || []
      }
    } catch (err) {
      console.error('Failed to fetch runtimes:', err)
    }
  }

  onMount(() => {
    fetchRuntimes()
  })

  async function sendMessage() {
    if (!input.trim() || loading) return

    const userMessage = input.trim()
    input = ''
    
    messages = [...messages, { role: 'user', content: userMessage }]
    await tick()
    scrollToBottom()
    
    loading = true

    try {
      const response = await fetch(`${API_BASE}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ message: userMessage, runtime }),
      })

      if (!response.ok) throw new Error('Erreur')

      const data = await response.json()
      messages = [...messages, { role: 'assistant', content: data.response }]
    } catch (err) {
      messages = [...messages, { role: 'error', content: 'Erreur de connexion' }]
    } finally {
      loading = false
      await tick()
      scrollToBottom()
    }
  }

  async function clearHistory() {
    try {
      await fetch(`${API_BASE}/chat/history`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` },
      })
      messages = []
    } catch (err) {
      console.error(err)
    }
  }

  function scrollToBottom() {
    if (messagesContainer) {
      messagesContainer.scrollTop = messagesContainer.scrollHeight
    }
  }

  function handleKeydown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }
</script>

<div class="chat-panel">
  <div class="panel-header">
    <h2>💬 Chat</h2>
    <div class="header-controls">
      {#if runtimes.length > 0}
        <select bind:value={runtime} class="runtime-select">
          {#each runtimes as rt}
            <option value={rt.id}>{rt.label}</option>
          {/each}
        </select>
      {/if}
      {#if messages.length > 0}
        <button class="clear-btn" on:click={clearHistory}>Effacer</button>
      {/if}
    </div>
  </div>

  <div class="messages" bind:this={messagesContainer}>
    {#if messages.length === 0}
      <div class="empty">
        <p>👋 Salut ! Je suis ton assistant TADA.</p>
        <p class="hint">Pose-moi des questions sur tes projets, ton organisation, ou capture des idées.</p>
      </div>
    {/if}
    
    {#each messages as msg}
      <div class="message {msg.role}">
        <div class="avatar">
          {#if msg.role === 'user'}👤{:else if msg.role === 'error'}⚠️{:else}🤖{/if}
        </div>
        <div class="content">{msg.content}</div>
      </div>
    {/each}
    
    {#if loading}
      <div class="message assistant loading">
        <div class="avatar">🤖</div>
        <div class="content">
          <span class="typing">
            <span></span><span></span><span></span>
          </span>
        </div>
      </div>
    {/if}
  </div>

  <form class="input-area" on:submit|preventDefault={sendMessage}>
    <textarea
      bind:value={input}
      on:keydown={handleKeydown}
      placeholder="Écris ton message..."
      disabled={loading}
      rows="2"
    />
    <button type="submit" disabled={loading || !input.trim()}>
      ➤
    </button>
  </form>
</div>

<style>
  .chat-panel {
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

  .header-controls {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .runtime-select {
    padding: 4px 8px;
    background: #1a1a1a;
    border: 1px solid #333;
    border-radius: 4px;
    color: #e0e0e0;
    font-size: 12px;
    cursor: pointer;
  }

  .runtime-select:focus {
    outline: none;
    border-color: #4a9eff;
  }

  .clear-btn {
    padding: 4px 8px;
    background: transparent;
    border: 1px solid #333;
    border-radius: 4px;
    color: #666;
    cursor: pointer;
    font-size: 12px;
  }

  .clear-btn:hover {
    background: #222;
    color: #888;
  }

  .messages {
    flex: 1;
    overflow-y: auto;
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .empty {
    text-align: center;
    padding: 40px 20px;
    color: #666;
  }

  .empty p {
    margin: 8px 0;
  }

  .empty .hint {
    font-size: 13px;
    color: #555;
  }

  .message {
    display: flex;
    gap: 10px;
    align-items: flex-start;
  }

  .avatar {
    font-size: 20px;
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #1a1a1a;
    border-radius: 6px;
    flex-shrink: 0;
  }

  .message.user .avatar {
    background: #1a3a5c;
  }

  .message.assistant .avatar {
    background: #1a4a3a;
  }

  .message.error .avatar {
    background: #4a1a1a;
  }

  .content {
    background: #1a1a1a;
    padding: 10px 14px;
    border-radius: 8px;
    max-width: 85%;
    line-height: 1.5;
    white-space: pre-wrap;
    word-break: break-word;
  }

  .message.user .content {
    background: #1a3a5c;
  }

  .message.error .content {
    background: #4a1a1a;
    color: #ff6b6b;
  }

  .typing {
    display: flex;
    gap: 4px;
  }

  .typing span {
    width: 6px;
    height: 6px;
    background: #666;
    border-radius: 50%;
    animation: bounce 1.4s infinite ease-in-out;
  }

  .typing span:nth-child(1) { animation-delay: -0.32s; }
  .typing span:nth-child(2) { animation-delay: -0.16s; }

  @keyframes bounce {
    0%, 80%, 100% { transform: scale(0); }
    40% { transform: scale(1); }
  }

  .input-area {
    display: flex;
    gap: 8px;
    padding: 12px 16px;
    border-top: 1px solid #222;
    flex-shrink: 0;
  }

  textarea {
    flex: 1;
    padding: 10px 12px;
    background: #1a1a1a;
    border: 1px solid #333;
    border-radius: 8px;
    color: #e0e0e0;
    font-size: 14px;
    font-family: inherit;
    resize: none;
    line-height: 1.4;
  }

  textarea:focus {
    outline: none;
    border-color: #4a9eff;
  }

  textarea:disabled {
    opacity: 0.6;
  }

  button[type="submit"] {
    width: 44px;
    height: 44px;
    background: #4a9eff;
    border: none;
    border-radius: 8px;
    color: white;
    font-size: 18px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s;
    flex-shrink: 0;
  }

  button[type="submit"]:hover:not(:disabled) {
    background: #3a8eef;
    transform: scale(1.05);
  }

  button[type="submit"]:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
</style>
