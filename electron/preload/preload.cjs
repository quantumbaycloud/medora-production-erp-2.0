const { contextBridge } = require("electron");

contextBridge.exposeInMainWorld(
  "medoraxDesktop",
  Object.freeze({
    isDesktop: true,
    platform: process.platform,
    version: process.versions.electron,
  }),
);
