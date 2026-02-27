import { defineConfig } from 'astro/config';
import preact from '@astrojs/preact';

// https://astro.build/config
export default defineConfig({
  site: 'http://localhost:4321',
  output: 'static',
  integrations: [preact()],
  server: {
    port: 4321,
    host: true,
  },
  build: {
    assets: '_assets',
  },
});
