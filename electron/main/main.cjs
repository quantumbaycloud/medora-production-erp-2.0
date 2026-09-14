const { app, BrowserWindow, shell, session } = require("electron");
const path = require("path");

const LOCAL_URL = "http://127.0.0.1:5173";
const PRODUCTION_URL = "https://erp.meodrax.in";
const isDev = !app.isPackaged;

const ERP_URL = isDev
  ? (process.env.MEDORAX_ERP_URL || LOCAL_URL)
  : PRODUCTION_URL;

let mainWindow;

function isAllowedNavigation(url) {
  try {
    const parsed = new URL(url);

    if (isDev) {
      return parsed.origin === new URL(LOCAL_URL).origin;
    }

    return (
      parsed.protocol === "https:" &&
      (parsed.hostname === "erp.medorax.in" ||
        parsed.hostname === "erp.meodrax.in")
    );
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
    backgroundColor: "#ffffff",
    title: "MEDORAX ERP",
    webPreferences: {
      preload: path.join(__dirname, "../preload/preload.cjs"),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true,
      webSecurity: true,
    },
  });

  mainWindow.once("ready-to-show", () => mainWindow.show());

  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    if (/^https?:\/\//i.test(url)) shell.openExternal(url);
    return { action: "deny" };
  });

  mainWindow.webContents.on("will-navigate", (event, url) => {
    if (!isAllowedNavigation(url)) event.preventDefault();
  });

  mainWindow.webContents.on("will-redirect", (event, url) => {
    if (!isAllowedNavigation(url)) event.preventDefault();
  });

  mainWindow.loadURL(ERP_URL).catch((error) => {
    console.error("MEDORAX ERP failed to load:", error);
  });
}

const gotLock = app.requestSingleInstanceLock();

if (!gotLock) {
  app.quit();
} else {
  app.whenReady().then(() => {
    session.defaultSession.setPermissionRequestHandler(
      (_webContents, _permission, callback) => callback(false),
    );

    createWindow();

    app.on("activate", () => {
      if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
  });

  app.on("window-all-closed", () => {
    if (process.platform !== "darwin") app.quit();
  });
}
