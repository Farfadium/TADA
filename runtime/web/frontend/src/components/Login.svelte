<script>
  import { createEventDispatcher } from 'svelte'
  import { API_BASE } from '../config.js'

  const dispatch = createEventDispatcher()

  let username = ''
  let password = ''
  let error = ''
  let loading = false

  async function handleSubmit() {
    error = ''
    loading = true

    try {
      const response = await fetch(`${API_BASE}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      })

      if (!response.ok) {
        throw new Error('Identifiants invalides')
      }

      const data = await response.json()
      dispatch('login', { token: data.access_token })
    } catch (err) {
      error = err.message
    } finally {
      loading = false
    }
  }
</script>

<div class="login-container">
  <div class="login-box">
    <h1>TADA</h1>
    <p class="subtitle">Own your life.</p>

    <form on:submit|preventDefault={handleSubmit}>
      <input
        type="text"
        placeholder="Username"
        bind:value={username}
        disabled={loading}
      />
      <input
        type="password"
        placeholder="Password"
        bind:value={password}
        disabled={loading}
      />

      {#if error}
        <p class="error">{error}</p>
      {/if}

      <button type="submit" disabled={loading}>
        {loading ? 'Connexion...' : 'Se connecter'}
      </button>
    </form>
  </div>
</div>

<style>
  .login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 20px;
  }

  .login-box {
    background: #1a1a1a;
    padding: 40px;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    width: 100%;
    max-width: 400px;
  }

  h1 {
    font-size: 48px;
    font-weight: 700;
    margin-bottom: 8px;
    text-align: center;
  }

  .subtitle {
    text-align: center;
    color: #888;
    margin-bottom: 32px;
    font-style: italic;
  }

  input {
    width: 100%;
    padding: 12px;
    margin-bottom: 16px;
    background: #2a2a2a;
    border: 1px solid #3a3a3a;
    border-radius: 4px;
    color: #e0e0e0;
    font-size: 16px;
  }

  input:focus {
    outline: none;
    border-color: #4a9eff;
  }

  button {
    width: 100%;
    padding: 12px;
    background: #4a9eff;
    border: none;
    border-radius: 4px;
    color: white;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s;
  }

  button:hover:not(:disabled) {
    background: #3a8eef;
  }

  button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .error {
    color: #ff6b6b;
    font-size: 14px;
    margin-bottom: 16px;
  }
</style>
