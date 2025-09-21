// @ts-check
import { defineConfig } from 'astro/config';

import tailwindcss from '@tailwindcss/vite';

// https://astro.build/config
export default defineConfig({
  site: 'https://akhavan12.github.io',
  base: process.env.NODE_ENV === 'development' ? '/' : '/FF03D1D1D403328562431NECSI/',
  vite: {
    plugins: [tailwindcss()]
  }
});