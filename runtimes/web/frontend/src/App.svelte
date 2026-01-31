<script>
  import Login from './components/Login.svelte'
  import Header from './components/Header.svelte'
  import Chat from './components/Chat.svelte'
  import TadaExplorer from './components/TadaExplorer.svelte'
  import Dashboard from './components/Dashboard.svelte'
  import { onMount } from 'svelte'
  import { API_BASE } from './config.js'

  let token = localStorage.getItem('tada_token')
  let isAuthenticated = !!token
  let currentTab = 'chat'

  function handleLogin(event) {
    token = event.detail.token
    localStorage.setItem('tada_token', token)
    isAuthenticated = true
  }

  function handleLogout() {
    token = null
    localStorage.removeItem('tada_token')
    isAuthenticated = false
  }

  function handleCaptured() {
    // Rafraîchir les composants si nécessaire
    if (currentTab === 'tada') {
      // Force un re-render de TadaExplorer
      currentTab = ''
      setTimeout(() => currentTab = 'tada', 0)
    } else if (currentTab === 'dashboard') {
      currentTab = ''
      setTimeout(() => currentTab = 'dashboard', 0)
    }
  }

  onMount(() => {
    // Vérifier si le token est toujours valide
    if (token) {
      fetch(`${API_BASE}/dashboard`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      .then(res => {
        if (res.status === 401) {
          handleLogout()
        }
      })
      .catch(() => handleLogout())
    }
  })
</script>

{#if isAuthenticated}
  <div class="app">
    <Header {token} on:logout={handleLogout} on:captured={handleCaptured} />

    <div class="content">
      {#if currentTab === 'chat'}
        <Chat {token} on:logout={handleLogout} />
      {:else if currentTab === 'tada'}
        <TadaExplorer {token} on:logout={handleLogout} />
      {:else if currentTab === 'dashboard'}
        <Dashboard {token} on:logout={handleLogout} />
      {/if}
    </div>

    <div class="bottom-nav">
      <button
        class="nav-item {currentTab === 'chat' ? 'active' : ''}"
        on:click={() => currentTab = 'chat'}
      >
        <div class="nav-icon">💬</div>
        <div class="nav-label">Chat</div>
      </button>
      <button
        class="nav-item {currentTab === 'tada' ? 'active' : ''}"
        on:click={() => currentTab = 'tada'}
      >
        <div class="nav-icon">📁</div>
        <div class="nav-label">TADA</div>
      </button>
      <button
        class="nav-item {currentTab === 'dashboard' ? 'active' : ''}"
        on:click={() => currentTab = 'dashboard'}
      >
        <div class="nav-icon">📊</div>
        <div class="nav-label">Dashboard</div>
      </button>
    </div>
  </div>
{:else}
  <Login on:login={handleLogin} />
{/if}

<style>
  :global(body) {
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #0a0a0a;
    color: #e0e0e0;
    overflow: hidden;
  }

  .app {
    display: flex;
    flex-direction: column;
    height: 100vh;
  }

  .content {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;
  }

  .bottom-nav {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: #1a1a1a;
    border-top: 1px solid #2a2a2a;
    display: flex;
    padding: 8px 0;
    z-index: 98;
  }

  .nav-item {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    padding: 8px;
    border: none;
    background: none;
    color: #888;
    cursor: pointer;
    transition: color 0.2s;
  }

  .nav-item.active {
    color: #4a9eff;
  }

  .nav-icon {
    font-size: 24px;
  }

  .nav-label {
    font-size: 11px;
  }
</style>
