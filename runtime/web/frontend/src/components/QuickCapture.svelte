<script>
  import { createEventDispatcher } from 'svelte'
  import { fade, slide } from 'svelte/transition'

  export let token

  const dispatch = createEventDispatcher()

  let content = ''
  let loading = false
  let recording = false
  let mediaRecorder = null
  let audioChunks = []

  async function handleSubmit() {
    if (!content.trim()) return

    loading = true

    try {
      const response = await fetch('http://localhost:8080/capture', {
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

      const result = await response.json()

      // Délai pour voir l'animation du spinner (800ms)
      await new Promise(resolve => setTimeout(resolve, 800))

      loading = false
      content = ''

      dispatch('success', result)
    } catch (err) {
      alert(err.message)
      loading = false
    }
  }

  async function startRecording() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      mediaRecorder = new MediaRecorder(stream)
      audioChunks = []

      mediaRecorder.ondataavailable = (event) => {
        audioChunks.push(event.data)
      }

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/webm' })
        await uploadFile(audioBlob, 'audio.webm', 'Enregistrement audio')
        stream.getTracks().forEach(track => track.stop())
      }

      mediaRecorder.start()
      recording = true
    } catch (err) {
      alert('Erreur: ' + err.message)
    }
  }

  function stopRecording() {
    if (mediaRecorder && recording) {
      mediaRecorder.stop()
      recording = false
    }
  }

  async function handlePhoto(event) {
    const file = event.target.files[0]
    if (file) {
      await uploadFile(file, file.name, 'Photo')
    }
  }

  async function uploadFile(file, filename, description) {
    loading = true
    const formData = new FormData()
    formData.append('file', file, filename)
    formData.append('description', description)

    try {
      const response = await fetch('http://localhost:8080/capture/file', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData
      })

      if (!response.ok) {
        throw new Error('Erreur lors de l\'upload')
      }

      const result = await response.json()

      // Délai pour l'UX
      await new Promise(resolve => setTimeout(resolve, 800))

      loading = false
      dispatch('success', result)
    } catch (err) {
      alert(err.message)
      loading = false
    }
  }
</script>

<div class="capture-box">
  <h2>💬 Capture rapide</h2>

  <form on:submit|preventDefault={handleSubmit}>
    <textarea
      bind:value={content}
      placeholder="Tape ton idée, tâche, note...
Utilise @projet pour lier à un projet
Utilise #tag pour tagger
Utilise [[lien]] pour créer des liens"
      disabled={loading}
      rows="4"
    />

    <button type="submit" disabled={loading || !content.trim()} class:loading>
      {#if loading}
        <span class="spinner"></span>
        Capture en cours...
      {:else}
        Capturer
      {/if}
    </button>
  </form>

  <div class="media-buttons">
    <button
      type="button"
      class="media-btn"
      on:click={recording ? stopRecording : startRecording}
      disabled={loading}
      class:recording
    >
      {#if recording}
        ⏹ Arrêter
      {:else}
        🎤 Audio
      {/if}
    </button>

    <label class="media-btn" class:disabled={loading}>
      📷 Photo
      <input
        type="file"
        accept="image/*"
        capture="environment"
        on:change={handlePhoto}
        disabled={loading}
        style="display: none"
      />
    </label>
  </div>

  <div class="hint">
    💡 Syntaxe: <code>@projet</code> <code>#tag</code> <code>[[lien]]</code>
  </div>
</div>

<style>
  .capture-box {
    background: #1a1a1a;
    padding: 24px;
    border-radius: 8px;
    margin-bottom: 32px;
    transition: all 0.3s ease;
  }

  h2 {
    font-size: 18px;
    margin-bottom: 16px;
    color: #e0e0e0;
    text-transform: none;
    letter-spacing: normal;
  }

  textarea {
    width: 100%;
    padding: 12px;
    background: #2a2a2a;
    border: 1px solid #3a3a3a;
    border-radius: 4px;
    color: #e0e0e0;
    font-size: 16px;
    font-family: inherit;
    resize: vertical;
    margin-bottom: 12px;
    transition: all 0.3s ease;
  }

  textarea:focus {
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
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
  }

  button:hover:not(:disabled) {
    background: #3a8eef;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(74, 158, 255, 0.3);
  }

  button:active:not(:disabled) {
    transform: translateY(0);
  }

  button:disabled {
    opacity: 0.8;
    cursor: not-allowed;
  }

  button.loading {
    background: #5aa5ff;
  }

  .spinner {
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top-color: white;
    border-radius: 50%;
    animation: spin 0.6s linear infinite;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  .media-buttons {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-top: 16px;
    margin-bottom: 12px;
  }

  .media-btn {
    padding: 12px;
    background: #2a2a2a;
    border: 1px solid #3a3a3a;
    border-radius: 4px;
    color: #e0e0e0;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    text-align: center;
  }

  .media-btn:hover:not(.disabled) {
    background: #3a3a3a;
    border-color: #4a4a4a;
  }

  .media-btn.recording {
    background: #ff4a4a;
    border-color: #ff6a6a;
    animation: pulse 1.5s ease-in-out infinite;
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
  }

  .media-btn.disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .hint {
    margin-top: 12px;
    font-size: 12px;
    color: #666;
  }

  code {
    background: #2a2a2a;
    padding: 2px 6px;
    border-radius: 3px;
    font-family: 'Monaco', 'Courier New', monospace;
  }
</style>
