import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // Em dev, encaminha as chamadas ao back-end (outra equipe) em http://localhost:8000.
    // Troque a porta aqui (ou use BACKEND_URL no .env, ex.: BACKEND_URL=http://localhost:9000) se necessário.
    proxy: {
      '^/(automatos|api)': {
        target: process.env.BACKEND_URL ?? 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
