import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  build: {
    outDir: "../backend/public", // Output to backend/public
    emptyOutDir: true, // Delete existing files before building
  },
  base: '/dash',
  server: {
    proxy: {
      "/ws": {
        target: "http://127.0.0.1:8000",
        ws: true, // Enable WebSocket proxying
        changeOrigin: true,
        secure: false
      },
      
    },
  },
  
})
