<script>
  import Login from './components/Login.svelte'
  import Dashboard from './components/Dashboard.svelte'
  import { onMount } from 'svelte'
  import { API_BASE } from './config.js'

  let token = localStorage.getItem('tada_token')
  let isAuthenticated = !!token

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
  <Dashboard {token} on:logout={handleLogout} />
{:else}
  <Login on:login={handleLogin} />
{/if}

<style>
  :global(body) {
    margin: 0;
    padding: 0;
  }
</style>
