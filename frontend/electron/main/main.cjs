const { app, BrowserWindow, shell, session } = require('electron');
const path = require('path');

const isDev = !app.isPackaged;
const PRODUCTION_URL = 'https://erp.medorax.in';
const DEV_URL = 'http://localhost:5173';
const ERP_URL = process.env.MEDORAX_ERP_URL || (isDev ? DEV_URL : PRODUCTION_URL);

const gotLock = app.requestSingleInstanceLock();
if (!gotLock) {
  app.quit();
} else {
  let mainWindow;

  function isAllowedNavigation(url) {
    try {
      const parsed = new URL(url);
      if (isDev) return parsed.origin === new URL(DEV_URL).origin;
      return parsed.protocol === 'https:' && parsed.hostname === 'erp.medorax.in';
    } catch {
      return false;
    }
  }

  function createWindow() {
    mainWindow = new BrowserWindow({
      width: 1440,
      height: 900,
      minWidth: 1100,
      minHeight: 700,
      show: false,
      autoHideMenuBar: true,
      backgroundColor: '#ffffff',
      title: 'MEDORAX ERP',
      webPreferences: {
        preload: path.join(__dirname, '../preload/preload.cjs'),
        contextIsolation: true,
        nodeIntegration: false,
        sandbox: true,
        webSecurity: true,
      },
    });

    mainWindow.once('ready-to-show', () => mainWindow.show());

    mainWindow.webContents.setWindowOpenHandler(({ url }) => {
      if (/^https?:\/\//i.test(url)) shell.openExternal(url);
      return { action: 'deny' };
    });

    mainWindow.webContents.on('will-navigate', (event, url) => {
      if (!isAllowedNavigation(url)) event.preventDefault();
    });

    mainWindow.webContents.on('will-redirect', (event, url) => {
      if (!isAllowedNavigation(url)) event.preventDefault();
    });

    mainWindow.loadURL(ERP_URL);
  }

  app.on('second-instance', () => {
    if (!mainWindow) return;
    if (mainWindow.isMinimized()) mainWindow.restore();
    mainWindow.focus();
  });

  app.whenReady().then(() => {
    session.defaultSession.setPermissionRequestHandler((_webContents, _permission, callback) => callback(false));
    createWindow();
    app.on('activate', () => {
      if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
  });

  app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
  });
}
