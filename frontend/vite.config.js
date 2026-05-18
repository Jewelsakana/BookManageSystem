import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,
    proxy: {
      '/user': 'http://localhost:8000',
      '/book': 'http://localhost:8000',
      '/purchase': 'http://localhost:8000',
      '/sale': 'http://localhost:8000',
      '/bill': 'http://localhost:8000'
    }
  }
})
