<script>
  import { createEventDispatcher } from 'svelte'
  import { API_BASE } from '../config.js'

  export let token

  const dispatch = createEventDispatcher()

  let textModalOpen = false
  let textContent = ''
  let loading = false
  let mediaRecorder = null
  let recording = false
  let audioChunks = []

  async function handleTextCapture() {
    textModalOpen = true
  }

  async function submitTextCapture() {
    if (!textContent.trim()) return

    loading = true

    try {
      const response = await fetch(`${API_BASE}/capture`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ content: textContent })
      })

      if (!response.ok) {
        if (response.status === 401) {
          dispatch('logout')
        }
        throw new Error('Erreur lors de la capture')
      }

      textContent = ''
      textModalOpen = false
      dispatch('captured')
    } catch (error) {
      alert(`Erreur: ${error.message}`)
    } finally {
      loading = false
    }
  }

  function closeTextModal() {
    textModalOpen = false
    textContent = ''
  }

  async function handleVoiceCapture() {
    if (recording) {
      stopRecording()
    } else {
      startRecording()
    }
  }

  async function startRecording() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      mediaRecorder = new MediaRecorder(stream)
      audioChunks = []

      mediaRecorder.ondataavailable = (e) => {
        audioChunks.push(e.data)
      }

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/webm' })
        await uploadAudio(audioBlob)
        stream.getTracks().forEach(track => track.stop())
      }

      mediaRecorder.start()
      recording = true
    } catch (error) {
      if (window.location.protocol !== 'https:' && window.location.hostname !== 'localhost') {
        alert('Erreur: L\'enregistrement audio nécessite HTTPS. Utilisez https://tada-yvan.tail014c2b.ts.net/')
      } else {
        alert(`Erreur d'accès au microphone: ${error.message}`)
      }
    }
  }

  function stopRecording() {
    if (!recording || !mediaRecorder) return

    mediaRecorder.stop()
    recording = false
  }

  async function uploadAudio(audioBlob) {
    loading = true

    try {
      const formData = new FormData()
      formData.append('file', audioBlob, 'voice_capture.webm')
      formData.append('description', '')

      const response = await fetch(`${API_BASE}/capture/file`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData
      })

      if (!response.ok) {
        if (response.status === 401) {
          dispatch('logout')
        }
        throw new Error('Erreur lors de l\'envoi')
      }

      dispatch('captured')
    } catch (error) {
      alert(`Erreur: ${error.message}`)
    } finally {
      loading = false
    }
  }

  async function handlePhotoCapture() {
    const input = document.createElement('input')
    input.type = 'file'
    input.accept = 'image/*'
    input.capture = 'environment'

    input.onchange = async (e) => {
      const file = e.target.files[0]
      if (!file) return

      loading = true

      try {
        const formData = new FormData()
        formData.append('file', file)
        formData.append('description', '')

        const response = await fetch(`${API_BASE}/capture/file`, {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${token}`,
          },
          body: formData
        })

        if (!response.ok) {
          if (response.status === 401) {
            dispatch('logout')
          }
          throw new Error('Erreur lors de l\'envoi')
        }

        dispatch('captured')
      } catch (error) {
        alert(`Erreur: ${error.message}`)
      } finally {
        loading = false
      }
    }

    input.click()
  }
</script>

<div class="header">
  <h1>TADA</h1>
  <div class="header-actions">
    <button class="icon-btn" on:click={handleTextCapture} disabled={loading} title="Texte rapide">
      📝
    </button>
    <button
      class="icon-btn {recording ? 'recording' : ''}"
      on:click={handleVoiceCapture}
      disabled={loading}
      title="Note vocale"
    >
      {recording ? '⏹️' : '🎤'}
    </button>
    <button class="icon-btn" on:click={handlePhotoCapture} disabled={loading} title="Photo">
      📷
    </button>
  </div>
</div>

{#if textModalOpen}
  <div class="modal-backdrop" on:click={closeTextModal}>
    <div class="modal" on:click|stopPropagation>
      <h2>Capture rapide</h2>
      <textarea
        bind:value={textContent}
        placeholder="Écris ton idée, ta note, ton rappel..."
        rows="6"
        autofocus
      ></textarea>
      <div class="modal-actions">
        <button class="btn-secondary" on:click={closeTextModal} disabled={loading}>
          Annuler
        </button>
        <button class="btn-primary" on:click={submitTextCapture} disabled={loading || !textContent.trim()}>
          {loading ? 'Envoi...' : 'Capturer'}
        </button>
      </div>
    </div>
  </div>
{/if}

<style>
  .header {
    background: #1a1a1a;
    padding: 12px 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #2a2a2a;
    position: sticky;
    top: 0;
    z-index: 100;
  }

  h1 {
    font-size: 20px;
    font-weight: 700;
    margin: 0;
  }

  .header-actions {
    display: flex;
    gap: 8px;
  }

  .icon-btn {
    width: 36px;
    height: 36px;
    background: #2a2a2a;
    border: none;
    border-radius: 8px;
    color: #e0e0e0;
    font-size: 18px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s;
  }

  .icon-btn:active {
    transform: scale(0.95);
    background: #4a9eff;
  }

  .icon-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .icon-btn.recording {
    background: #ff4a4a;
    animation: pulse 1s infinite;
  }

  @keyframes pulse {
    0%, 100% {
      opacity: 1;
    }
    50% {
      opacity: 0.7;
    }
  }

  .modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.7);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    padding: 20px;
  }

  .modal {
    background: #1a1a1a;
    border-radius: 16px;
    padding: 24px;
    max-width: 500px;
    width: 100%;
    border: 1px solid #2a2a2a;
  }

  .modal h2 {
    margin: 0 0 16px 0;
    font-size: 18px;
  }

  .modal textarea {
    width: 100%;
    background: #2a2a2a;
    border: 1px solid #3a3a3a;
    border-radius: 8px;
    padding: 12px;
    color: #e0e0e0;
    font-size: 15px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    resize: vertical;
    margin-bottom: 16px;
  }

  .modal textarea:focus {
    outline: none;
    border-color: #4a9eff;
  }

  .modal-actions {
    display: flex;
    gap: 12px;
    justify-content: flex-end;
  }

  .btn-secondary, .btn-primary {
    padding: 10px 20px;
    border-radius: 8px;
    border: none;
    font-size: 15px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
  }

  .btn-secondary {
    background: #2a2a2a;
    color: #e0e0e0;
  }

  .btn-secondary:active {
    background: #333;
    transform: scale(0.95);
  }

  .btn-primary {
    background: #4a9eff;
    color: #fff;
  }

  .btn-primary:active {
    background: #3a8eef;
    transform: scale(0.95);
  }

  .btn-primary:disabled, .btn-secondary:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
</style>
