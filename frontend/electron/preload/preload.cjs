const { contextBridge } = require('electron');

contextBridge.exposeInMainWorld('medoraxDesktop', Object.freeze({
  platform: process.platform,
  version: process.versions.electron,
  isDesktop: true,
}));
