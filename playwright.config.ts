import { defineConfig } from '@playwright/test';
export default defineConfig({ testDir: './tests', fullyParallel: true, timeout: 30000, use: { baseURL: 'http://127.0.0.1:4321', browserName: 'chromium' }, webServer: { command: 'npm run preview', url: `http://127.0.0.1:4321${process.env.TEST_BASE_PATH || '/'}`, reuseExistingServer: false, timeout: 30000 } });
