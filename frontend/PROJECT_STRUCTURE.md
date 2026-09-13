# Medorax ERP - Project Structure

## Overview

Medorax ERP is a cross-platform Enterprise Resource Planning (ERP) system built with **React (Vite)** for the frontend and **Electron** for desktop packaging. It currently focuses on the **Authentication Module** as the primary implemented feature, with scaffolded directories for future modules.

---

## Technology Stack

| Layer | Technology |
|-------|-----------|
| **UI Library** | React 18 (JSX) |
| **Build Tool** | Vite |
| **Desktop Shell** | Electron |
| **State Management** | Redux Toolkit |
| **Routing** | React Router v6 |
| **Styling** | CSS Modules + Global CSS |
| **Linting** | ESLint (Flat Config) |
| **Language** | JavaScript (`.jsx`, `.cjs`) |

---

## Top-Level Directory Layout

```
medorax-erp/
├── electron/          # Electron main process & IPC handlers
├── public/            # Static public assets
├── src/               # React application source code
├── .github/           # GitHub-specific meta files
├── .gitignore
├── eslint.config.js   # ESLint flat config
├── index.html         # Vite HTML entry point
├── package.json       # Dependencies & scripts
├── package-lock.json
├── README.md
└── vite.config.js     # Vite configuration
```

---

## `electron/` — Electron Desktop Shell

The Electron layer handles native OS integration and desktop-specific functionality.

```
electron/
├── assets/
│   └── logo.ico                   # App icon for Windows
├── config/
│   └── electron.config.cjs        # Electron build & packaging config
├── ipc/
│   ├── index.cjs                  # IPC handler registration hub
│   ├── auth.ipc.cjs               # Authentication IPC handlers
│   ├── billing.ipc.cjs            # Billing module IPC handlers
│   ├── inventory.ipc.cjs          # Inventory module IPC handlers
│   └── settings.ipc.cjs           # Settings IPC handlers
├── main/
│   ├── main.cjs                   # Electron main process entry point
│   ├── preload.cjs                # Preload script (context bridge)
│   └── window.cjs                 # BrowserWindow creation & management
└── utils/
    └── logger.cjs                 # Logging utility for Electron
```

Key design points:
- **preload.cjs** bridges renderer (React) to main process via `contextBridge`
- **window.cjs** handles window creation, lifecycle, and configuration
- IPC handlers are separated by domain (`auth`, `billing`, `inventory`, `settings`)

---

## `src/` — React Application

The bulk of the application lives here, organized by feature/domain.

```
src/
├── api/                    # API client layer (scaffolded)
├── assets/                 # Static assets (images, icons)
│   ├── icons/
│   │   └── logo.ico
│   ├── images/auth/
│   │   ├── login-banner.png
│   │   ├── login-illustration.png
│   │   └── logo.png
│   └── logo.png
├── components/             # Reusable UI components
├── config/                 # Application configuration files
├── constants/              # Global constants (scaffolded)
├── contexts/               # React context providers (scaffolded)
├── hooks/                  # Custom React hooks (scaffolded)
├── layouts/                # Layout components (scaffolded)
├── modules/                # Feature modules (domain-organized)
│   └── authentication/     # Authentication module (fully implemented)
├── permissions/            # Permission/role management (scaffolded)
├── redux/                  # Redux store configuration & global slices
├── routes/                 # Route definitions & guards
├── services/               # Service layer (scaffolded)
├── store/                  # Alternative/store setup (scaffolded)
├── styles/                 # Global and utility stylesheets
├── theme/                  # Design system / theme tokens
├── types/                  # Type definitions (scaffolded)
├── utils/                  # Utility functions (scaffolded)
├── validators/             # Validation rules (scaffolded)
├── App.css
├── App.jsx                 # Root application component
├── index.css
├── index.js                # Alternative entry (scaffolded)
└── main.jsx                # Application entry point
```

---

### `src/components/` — Reusable UI Components

Structure follows a **domain-grouped** pattern with placeholders for future component categories:

```
src/components/
├── breadcrumbs/            # Breadcrumb components (scaffolded)
├── buttons/                # Button variants (scaffolded)
├── cards/                  # Card components (scaffolded)
├── charts/                 # Chart/graph components (scaffolded)
├── common/                 # Common/shared components (scaffolded)
├── dialogs/                # Dialog components (scaffolded)
├── forms/                  # Form components (scaffolded)
├── loaders/                # Loading indicators (scaffolded)
├── modals/                 # Modal components (scaffolded)
├── navbar/                 # Navigation bar (scaffolded)
├── pagination/             # Pagination components (scaffolded)
├── sidebar/                # Sidebar navigation (scaffolded)
├── tables/                 # Table components (scaffolded)
├── ui/                     # Atomic UI components (implemented)
│   ├── index.js            # Barrel export
│   ├── AuthCard/           # Authentication card wrapper
│   ├── AuthHeader/         # Authentication header
│   ├── Button/             # Reusable button component
│   ├── Card/               # Generic card component
│   ├── Checkbox/           # Checkbox input
│   ├── Divider/            # Visual divider
│   ├── FormField/          # Form field wrapper with label + error
│   ├── Input/              # Text input
│   ├── Logo/               # Logo display component
│   ├── OTPInput/           # One-time password input
│   ├── PasswordInput/      # Password input with toggle visibility
│   ├── RememberMe/         # "Remember me" checkbox with label
│   ├── SearchInput/        # Search input field
│   ├── Select/             # Dropdown select
│   ├── SocialButton/       # Social login button
│   ├── Spinner/            # Loading spinner
│   └── Typography/         # Text typography component
└── widgets/                # Widget components (scaffolded)
```

Each UI component follows a consistent pattern:
- **`ComponentName.jsx`** — Component implementation
- **`ComponentName.module.css`** — Scoped CSS Module styles
- **`index.js`** — Barrel export for clean imports

---

### `src/config/` — Configuration Files

```
src/config/
├── api.config.js           # API endpoints & base URL
├── app.config.js           # Application-level settings
├── auth.config.js          # Authentication configuration
├── electron.config.js      # Electron-specific config (renderer side)
└── theme.config.js         # Theme configuration
```

---

### `src/theme/` — Design System Tokens

```
src/theme/
├── index.js                # Barrel export
├── animations.js           # Animation definitions
├── breakpoints.js          # Responsive breakpoints
├── colors.js               # Color palette tokens
├── components.js           # Component-level theme overrides
├── fonts.js                # Font family definitions
├── radius.js               # Border radius values
├── shadow.js               # Box shadow definitions
├── spacing.js              # Spacing scale
├── typography.js           # Typography scale
└── zIndex.js               # Z-index values
```

---

### `src/styles/` — Global Stylesheets

```
src/styles/
├── animations.css           # Keyframe animations
├── global.css               # Global styles / base
├── globals.css              # Alternative global styles
├── index.css                # Style aggregator
├── reset.css                # CSS reset
├── utilities.css            # Utility classes
└── variables.css            # CSS custom properties
```

---

### `src/redux/` — State Management

```
src/redux/
├── store.js                 # Redux store creation
├── rootReducer.js           # Combined root reducer
├── persist.js               # Redux persist configuration
└── slices/
    ├── appSlice.js           # App-level state (loading, modals, etc.)
    ├── authSlice.js          # Global auth state
    └── themeSlice.js         # Theme state (dark/light mode)
```

---

### `src/routes/` — Routing

```
src/routes/
├── AppRoutes.jsx            # Main route definitions
├── ProtectedRoute.jsx       # Auth guard for protected pages
└── PublicRoute.jsx          # Redirect logged-in users away from public pages
```

Route structure:
- **ProtectedRoute** — Wraps pages that require authentication
- **PublicRoute** — Wraps pages like Login/Register that should redirect authenticated users

---

## `src/modules/authentication/` — Authentication Feature Module

This is the **fully implemented** module and demonstrates the project's architectural patterns.

```
src/modules/authentication/
├── AuthLayout/              # Shared auth layout wrapper
│   ├── AuthLayout.jsx
│   ├── AuthLayout.css
│   └── index.js
├── DeviceManagement/        # Device management page
├── ForgotPassword/          # Forgot password flow
├── Login/                   # Login flow (most feature-rich)
├── LoginHistory/            # Login history page
├── PasswordPolicy/          # Password policy page
├── ResetPassword/           # Reset password page
├── VerifyEmail/             # Email verification page
├── shared/                  # Shared auth components
│   ├── index.js
│   ├── AuthBanner/
│   ├── AuthFooter/
│   └── AuthNavbar/
├── constants/               # Module-level constants
│   ├── authConstants.js
│   ├── authMessages.js
│   ├── authRoutes.js
│   └── storageKeys.js
├── hooks/                   # Module-level hooks
│   ├── useAuth.js
│   ├── useCountdown.js
│   ├── useLogin.js
│   ├── useOTP.js
│   └── useRememberMe.js
├── services/                # Module-level services
│   ├── authService.js
│   ├── deviceService.js
│   ├── loginHistoryService.js
│   ├── otpService.js
│   ├── passwordService.js
│   └── tokenService.js
├── store/                   # Module-level Redux store
│   ├── index.js
│   ├── authSlice.js
│   ├── authThunk.js
│   └── authSelectors.js
├── styles/                  # Module-level styles
│   ├── auth.css
│   ├── auth-animation.css
│   └── auth-theme.css
└── utils/                   # Module-level utilities
    ├── authHelper.js
    ├── deviceFingerprint.js
    ├── encryption.js
    ├── rememberMe.js
    ├── tokenStorage.js
    └── validation.js
```

### Login Sub-Module (Deep Dive)

The `Login` sub-module is the most detailed, showing the full feature architecture:

```
src/modules/authentication/Login/
├── components/
│   ├── LoginBanner/          # Hero banner on login page
│   ├── LoginFooter/          # Footer links (Sign Up, Forgot Password)
│   ├── LoginForm/            # Main login form with validation
│   │   ├── LoginForm.jsx
│   │   ├── LoginForm.css
│   │   ├── index.js
│   │   └── validation.js     # Form validation rules
│   ├── LoginHeader/          # Header (logo, title, subtitle)
│   └── LoginIllustration/    # Decorative illustration
├── constants/
│   └── loginConstants.js     # Login-specific constants
├── hooks/
│   └── useLogin.js           # Login-specific hook
├── services/
│   └── authService.js        # Login API calls
├── store/
│   ├── index.js
│   ├── authSlice.js          # Login-specific slice
│   └── authThunk.js          # Async thunks for login
├── utils/
│   ├── loginHelper.js        # Login helper functions
│   ├── rememberMe.js         # Remember me logic
│   └── tokenStorage.js       # Token persistence
├── Login.jsx
├── Login.css
└── index.js
```

---

### Architectural Pattern Per Feature Page

Each page within a module follows this pattern:

```
FeatureName/
├── FeatureName.jsx       # Page component (logic + markup)
├── FeatureName.css       # Page-level styles
├── index.js              # Barrel export
├── components/           # Page-specific sub-components
│   └── SubComponent/     # Each with its own .jsx, .css, index.js
├── constants/            # Page-specific constants
├── hooks/                # Page-specific custom hooks
├── services/             # Page-specific API/service calls
├── store/                # Page-specific Redux slices/thunks
└── utils/                # Page-specific utility functions
```

---

## Architectural Patterns

### 1. Feature-Based Modular Structure
- Features are organized under `src/modules/` by domain
- Each module is self-contained with its own components, hooks, services, store, utils, and styles
- Encourages loose coupling and high cohesion

### 2. Shared UI Component Library
- Atomic UI components live in `src/components/ui/`
- Each component has its own directory with `.jsx`, `.module.css`, and `index.js`
- Components are reusable across modules via barrel exports

### 3. Redux Store Layers
- **Global Store** (`src/redux/`) — App-wide state (theme, global auth, app state)
- **Module Store** (`src/modules/*/store/`) — Feature-specific state
- **Page Store** (`src/modules/*/Feature/store/`) — Page-specific state (if needed)

### 4. Service Layer
- **API Services** (`src/modules/*/services/`) handle HTTP requests
- Services return promises consumed by Redux thunks or hooks
- Keeps API logic separate from UI

### 5. Custom Hooks
- Hooks abstract complex logic and state management from components
- Separate levels:
  - Module hooks (`src/modules/*/hooks/`)
  - Page hooks (`src/modules/*/Feature/hooks/`)
  - Future global hooks (`src/hooks/`)

### 6. Routing & Guards
- `ProtectedRoute` — Requires authentication to access
- `PublicRoute` — Redirects authenticated users away (e.g., Login page)

### 7. Electron Integration
- Electron runs as a separate layer with its own entry point (`main.cjs`)
- Communication via IPC handlers (`electron/ipc/`)
- Preload script exposes a controlled API to the renderer

### 8. Styling Strategy
- **CSS Modules** for component-scoped styles (`*.module.css`)
- **Global CSS** for reset, variables, animations, and utilities (`src/styles/`)
- **Theme tokens** in JavaScript (`src/theme/`) for programmatic access
- Module-level stylesheets for feature-specific theming

---

## Scaffolded / Placeholder Directories

The following directories exist as placeholders for future development:

| Directory | Purpose |
|-----------|---------|
| `src/api/` | API client configuration (Axios instance, interceptors) |
| `src/constants/` | Global application constants |
| `src/contexts/` | React context providers |
| `src/hooks/` | Global custom hooks |
| `src/layouts/` | Layout components (e.g., DashboardLayout) |
| `src/permissions/` | Role-based access control logic |
| `src/services/` | Global service layer |
| `src/store/` | Alternative store setup |
| `src/types/` | Type definitions (for future TypeScript migration) |
| `src/utils/` | Global utility functions |
| `src/validators/` | Global validation rules |
| `src/components/breadcrumbs/` | Breadcrumb navigation |
| `src/components/buttons/` | Button variants |
| `src/components/cards/` | Card variants |
| `src/components/charts/` | Chart components |
| `src/components/common/` | Common utilities |
| `src/components/dialogs/` | Dialog components |
| `src/components/forms/` | Form components |
| `src/components/loaders/` | Loading indicators |
| `src/components/modals/` | Modal components |
| `src/components/navbar/` | Navigation bar |
| `src/components/pagination/` | Pagination |
| `src/components/sidebar/` | Sidebar |
| `src/components/tables/` | Table components |
| `src/components/widgets/` | Widget components |

---

## Entry Points

| File | Role |
|------|------|
| `index.html` | Vite HTML shell (mounts `#root`) |
| `src/main.jsx` | React entry point (renders `<App />` into DOM) |
| `src/App.jsx` | Root component (providers, routing, layout) |
| `electron/main/main.cjs` | Electron main process entry |
| `electron/main/preload.cjs` | Electron preload (context bridge) |

---

## Scripts (from `package.json`)

| Script | Command | Description |
|--------|---------|-------------|
| `dev` | `vite` | Start Vite dev server |
| `build` | `vite build` | Build for production |
| `preview` | `vite preview` | Preview production build |
| `lint` | `eslint .` | Run ESLint |

---

## Summary

The Medorax ERP project follows a **feature-first modular architecture** with clear separation of concerns. The authentication module is fully implemented and serves as the architectural blueprint for future modules (billing, inventory, HR, etc.). The Electron integration provides a path to desktop deployment while keeping the React frontend platform-agnostic.