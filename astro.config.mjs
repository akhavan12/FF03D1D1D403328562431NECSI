// @ts-check
import { defineConfig } from 'astro/config';

import tailwindcss from '@tailwindcss/vite';

// https://astro.build/config
export default defineConfig({
  site: 'https://akhavan12.github.io',
  base: '/FF03D1D1D403328562431NECSI/',
  vite: {
    plugins: [tailwindcss()]
  }
});