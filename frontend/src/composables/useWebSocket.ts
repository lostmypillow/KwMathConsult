// src/composables/useWebSocket.ts
import { ref, onUnmounted } from 'vue'
import { v7 as uuidv7 } from 'uuid'

const receivedMessage = ref<any | null>(null)
const socket = ref<WebSocket | null>(null)

let reconnectAttempts = 0
let reconnectTimeout: ReturnType<typeof setTimeout> | null = null
const clientUUID = uuidv7()

const getBrowserInfo = () => ({
  userAgent: navigator.userAgent,
  language: navigator.language,
  hardwareConcurrency: navigator.hardwareConcurrency || 'unknown',
  screen: {
    width: screen.width,
    height: screen.height,
    pixelRatio: window.devicePixelRatio
  }
})
// import.meta.env.VITE_FASTAPI_URL
const url = 'ws://' + `${import.meta.env.VITE_FASTAPI_URL}` +`/ws/${uuidv7()}`
const getTimestamp = () => new Date().toISOString()

const log = (level: 'log' | 'error' | 'warn', msg: string, data?: any) => {
    console[level](`[WebSocket] ${JSON.stringify(msg)}`, data || '')
  
    // Optional: forward to server *only if socket is ready*

  }
  


const initializeWebSocket = () => {
  if (socket.value && socket.value.readyState !== WebSocket.CLOSED) {
    log('log', 'WebSocket already open or connecting')
    return
  }

  log('log', 'Initializing WebSocket connection...')
  socket.value = new WebSocket(url)

  socket.value.onopen = () => {
    log('log', 'WebSocket Connected')
    reconnectAttempts = 0

    if (reconnectTimeout) {
      clearTimeout(reconnectTimeout)
      reconnectTimeout = null
    }

    sendMessage('client_info', getBrowserInfo())
  }

  socket.value.onmessage = (event) => {
    try {
      receivedMessage.value = JSON.parse(event.data)
    } catch (error) {
      log('error', `Message parse error: ${JSON.stringify(error)}`)
    }
  }

  socket.value.onclose = () => {
    log('log', 'WebSocket Disconnected')
    attemptReconnect()
  }

  socket.value.onerror = (error) => {
    log('error', `WebSocket Error: ${JSON.stringify(error)}`)
    socket.value?.close()
  }
}

const attemptReconnect = () => {
  const backoff = Math.min(2000 * reconnectAttempts, 30000)
  if (reconnectTimeout) clearTimeout(reconnectTimeout)

  reconnectTimeout = setTimeout(() => {
    reconnectAttempts++
    log('log', `Reconnecting attempt ${reconnectAttempts}`)
    initializeWebSocket()
  }, backoff)
}

const sendMessage = (action: string, message: any, to = 'server') => {
  if (socket.value?.readyState === WebSocket.OPEN) {
    try {
      socket.value.send(JSON.stringify({
        action,
        message
      }))
    } catch (e) {
      log('error', `Send error: ${JSON.stringify(e)}`)
    }
  } else {
    log('warn', `Socket not open, cannot send: ${message}`)
  }
}

onUnmounted(() => {
  socket.value?.close()
})

export function useWebSocket() {
  initializeWebSocket()
  return {
    receivedMessage,
    sendMessage
  }
}
