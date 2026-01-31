<script>
  import { createEventDispatcher, onMount } from 'svelte'
  import { API_BASE } from '../config.js'

  export let token

  const dispatch = createEventDispatcher()

  let messages = []
  let inputText = ''
  let loading = false
  let recording = false
  let mediaRecorder = null
  let audioChunks = []
  let messagesContainer = null

  onMount(() => {
    // Message de bienvenue
    messages = [
      {
        id: Date.now(),
        role: 'assistant',
        content: "Salut ! Je suis Moltbot, ton assistant TADA. Comment puis-je t'aider ?",
        timestamp: new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
      }
    ]
  })

  function scrollToBottom() {
    setTimeout(() => {
      if (messagesContainer) {
        messagesContainer.scrollTop = messagesContainer.scrollHeight
      }
    }, 100)
  }

  async function sendMessage(text) {
    if (!text.trim()) return

    // Ajouter le message de l'utilisateur
    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: text,
      timestamp: new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
    }
    messages = [...messages, userMessage]
    inputText = ''
    scrollToBottom()

    loading = true

    try {
      const response = await fetch(`${API_BASE}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ message: text })
      })

      if (!response.ok) {
        if (response.status === 401) {
          dispatch('logout')
        }
        throw new Error('Erreur de communication avec Moltbot')
      }

      const data = await response.json()

      // Ajouter la réponse de Moltbot
      const botMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: data.response,
        timestamp: new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
      }
      messages = [...messages, botMessage]
      scrollToBottom()

    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: `Erreur: ${error.message}`,
        timestamp: new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
      }
      messages = [...messages, errorMessage]
      scrollToBottom()
    } finally {
      loading = false
    }
  }

  function handleKeyPress(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage(inputText)
    }
  }

  async function startRecording() {
    if (recording) return

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      mediaRecorder = new MediaRecorder(stream)
      audioChunks = []

      mediaRecorder.ondataavailable = (e) => {
        audioChunks.push(e.data)
      }

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/webm' })
        await sendAudioMessage(audioBlob)
        stream.getTracks().forEach(track => track.stop())
      }

      mediaRecorder.start()
      recording = true
    } catch (error) {
      alert(`Erreur d'accès au microphone: ${error.message}`)
    }
  }

  function stopRecording() {
    if (!recording || !mediaRecorder) return

    mediaRecorder.stop()
    recording = false
  }

  async function sendAudioMessage(audioBlob) {
    loading = true

    try {
      const formData = new FormData()
      formData.append('file', audioBlob, 'voice_message.webm')
      formData.append('description', 'Message vocal pour Moltbot')

      const response = await fetch(`${API_BASE}/capture/file`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData
      })

      if (!response.ok) {
        throw new Error('Erreur lors de l\'envoi du message vocal')
      }

      const data = await response.json()

      // Ajouter un message indiquant que le message vocal a été envoyé
      const userMessage = {
        id: Date.now(),
        role: 'user',
        content: '🎤 Message vocal envoyé',
        timestamp: new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
      }
      messages = [...messages, userMessage]

      const botMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: 'Message vocal reçu et en cours de transcription. Je reviendrai vers toi dès que je l\'aurai écouté !',
        timestamp: new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
      }
      messages = [...messages, botMessage]
      scrollToBottom()

    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: `Erreur: ${error.message}`,
        timestamp: new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
      }
      messages = [...messages, errorMessage]
      scrollToBottom()
    } finally {
      loading = false
    }
  }
</script>

<div class="chat-container">
  <div class="messages" bind:this={messagesContainer}>
    {#each messages as message (message.id)}
      <div class="message {message.role}">
        {message.content}
        <div class="message-time">{message.timestamp}</div>
      </div>
    {/each}
    {#if loading}
      <div class="message assistant typing">
        <span>●</span><span>●</span><span>●</span>
      </div>
    {/if}
  </div>

  <div class="chat-input">
    <div class="input-wrapper">
      <input
        type="text"
        bind:value={inputText}
        on:keypress={handleKeyPress}
        placeholder="Message Moltbot..."
        disabled={loading}
      />
      <button class="emoji-btn" disabled={loading}>😊</button>
    </div>
    <button
      class="voice-btn {recording ? 'recording' : ''}"
      on:mousedown={startRecording}
      on:mouseup={stopRecording}
      on:touchstart={startRecording}
      on:touchend={stopRecording}
      disabled={loading}
    >
      {recording ? '⏹️' : '🎤'}
    </button>
  </div>
</div>

<style>
  .chat-container {
    display: flex;
    flex-direction: column;
    height: calc(100vh - 120px);
    position: relative;
  }

  .messages {
    flex: 1;
    overflow-y: auto;
    padding: 16px;
    padding-bottom: 80px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .message {
    max-width: 80%;
    padding: 12px 16px;
    border-radius: 16px;
    line-height: 1.4;
    font-size: 15px;
  }

  .message.user {
    background: #4a9eff;
    color: #fff;
    align-self: flex-end;
    border-bottom-right-radius: 4px;
  }

  .message.assistant {
    background: #1a1a1a;
    color: #e0e0e0;
    align-self: flex-start;
    border-bottom-left-radius: 4px;
  }

  .message.typing {
    display: flex;
    gap: 4px;
    padding: 12px 20px;
  }

  .message.typing span {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #888;
    animation: typing 1.4s infinite;
  }

  .message.typing span:nth-child(2) {
    animation-delay: 0.2s;
  }

  .message.typing span:nth-child(3) {
    animation-delay: 0.4s;
  }

  @keyframes typing {
    0%, 60%, 100% {
      opacity: 0.3;
      transform: translateY(0);
    }
    30% {
      opacity: 1;
      transform: translateY(-8px);
    }
  }

  .message-time {
    font-size: 11px;
    opacity: 0.6;
    margin-top: 4px;
  }

  .chat-input {
    position: fixed;
    bottom: 60px;
    left: 0;
    right: 0;
    background: #1a1a1a;
    border-top: 1px solid #2a2a2a;
    padding: 12px;
    display: flex;
    gap: 8px;
    align-items: center;
    z-index: 10;
  }

  .input-wrapper {
    flex: 1;
    position: relative;
  }

  .input-wrapper input {
    width: 100%;
    background: #2a2a2a;
    border: none;
    border-radius: 20px;
    padding: 12px 48px 12px 16px;
    color: #e0e0e0;
    font-size: 15px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  }

  .input-wrapper input:focus {
    outline: none;
    background: #333;
  }

  .input-wrapper input:disabled {
    opacity: 0.5;
  }

  .emoji-btn {
    position: absolute;
    right: 4px;
    top: 50%;
    transform: translateY(-50%);
    width: 32px;
    height: 32px;
    background: none;
    border: none;
    border-radius: 50%;
    font-size: 18px;
    cursor: pointer;
    transition: all 0.2s;
  }

  .emoji-btn:active {
    transform: translateY(-50%) scale(0.9);
  }

  .emoji-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .voice-btn {
    width: 44px;
    height: 44px;
    background: #4a9eff;
    border: none;
    border-radius: 50%;
    color: #fff;
    font-size: 20px;
    cursor: pointer;
    transition: all 0.2s;
    flex-shrink: 0;
  }

  .voice-btn.recording {
    background: #ff4a4a;
    transform: scale(1.1);
  }

  .voice-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .voice-btn:active:not(.recording) {
    transform: scale(0.95);
  }
</style>
