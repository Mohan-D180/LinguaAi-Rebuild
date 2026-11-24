# LinguaAi frontend

The frontend is a React 19 + TypeScript application built with Vite. Tailwind CSS 4 provides styling, React Router handles client-side navigation, and Lucide React supplies icons.

## Requirements

- Node.js 20.19+ or 22.12+
- npm

## Setup

From this directory, install dependencies and start the development server:

```powershell
npm install
npm run dev
```

Vite prints the local URL when the server is ready. Other useful commands:

```powershell
npm run typecheck
npm run lint
npm run format:check
npm run build
```

## Routes

| Path           | Page                     |
| -------------- | ------------------------ |
| `/`            | Home                     |
| `/login`       | Login placeholder        |
| `/register`    | Registration placeholder |
| `/dashboard`   | Dashboard placeholder    |
| `/practice`    | Practice placeholder     |
| `/sessions`    | Sessions placeholder     |
| `/progress`    | Progress placeholder     |
| `/settings`    | Settings placeholder     |
| Any other path | Not found                |

Pages are intentionally placeholders. Authentication and backend integration are not implemented.

## Project layout

- `src/components/layout/` contains the shared application shell, header, and responsive sidebar.
- `src/components/ui/` contains small reusable presentation components.
- `src/pages/` contains route-level page components.
- `src/App.tsx` declares the routes; `src/main.tsx` mounts the app.
- `src/index.css` loads Tailwind CSS and defines the design tokens.

The `@/` import alias points to `src/` and is configured in both TypeScript and Vite.
