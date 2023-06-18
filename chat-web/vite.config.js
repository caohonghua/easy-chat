import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  define: {
    BASE_URL: JSON.stringify('http://127.0.0.1:5000')
  },
  server: {
    host: '0.0.0.0',
    port: 5173,
    open: true
  }
})