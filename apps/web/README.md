# FindSpam Admin Dashboard

Enterprise-grade Next.js 15 admin dashboard for the FindSpam AI moderation platform.

---

## Stack

| Layer | Technology |
|---|---|
| Framework | Next.js 15 (App Router) |
| Language | TypeScript |
| Styling | TailwindCSS + CSS custom properties |
| Components | shadcn/ui primitives + custom design system |
| State | Zustand v5 (UI + Auth) |
| Server state | TanStack Query v5 |
| Charts | Recharts 2 |
| Animations | Framer Motion 11 |
| Realtime | WebSocket (custom hook + Zustand store) |
| Theming | next-themes (dark/light/system) |
| Notifications | Sonner |

---

## Architecture

```
src/
├── app/
│   ├── (auth)/login/          # Login page (Server Component shell, Client form)
│   ├── (dashboard)/
│   │   ├── layout.tsx         # Dashboard shell: Sidebar + Header + main
│   │   └── dashboard/
│   │       ├── overview/      # KPI stats, trend chart, live feed, system health
│   │       ├── moderation/    # live/, queue/, history/
│   │       ├── analytics/     # spam-trends/, threat-map/, model-performance/
│   │       ├── ai-engine/     # predictions/, models/, training/
│   │       ├── telegram/      # groups/, events/
│   │       ├── blacklist/     # Domain/pattern/phrase management
│   │       ├── users/         # Admin RBAC user management
│   │       ├── audit/         # Immutable audit log
│   │       └── settings/      # Platform-wide configuration
│   ├── globals.css            # Design tokens + utility classes
│   └── layout.tsx             # Root layout: Providers + fonts + Toaster
├── components/
│   ├── layout/
│   │   ├── sidebar.tsx        # Collapsible animated sidebar with nested nav
│   │   └── header.tsx         # Search, theme toggle, connection badge, avatar
│   ├── ui/
│   │   ├── stat-card.tsx      # Animated KPI card with delta indicator
│   │   ├── chart-card.tsx     # Chart container with header + loading state
│   │   ├── threat-badge.tsx   # ThreatLevel colored badge (NONE→CRITICAL)
│   │   ├── action-badge.tsx   # ModerationAction badge
│   │   ├── data-table.tsx     # Sortable, paginated, typed table
│   │   ├── search-input.tsx   # Debounced search with clear button
│   │   ├── skeleton.tsx       # Skeleton loading components
│   │   ├── empty-state.tsx    # Empty state with icon + action
│   │   └── page-header.tsx    # Page title + breadcrumbs + action slot
│   └── charts/
│       ├── area-chart.tsx     # Recharts AreaChart (dark-themed, gradient fills)
│       ├── bar-chart.tsx      # Recharts BarChart with per-bar colors
│       ├── donut-chart.tsx    # Recharts PieChart with center label
│       └── line-chart.tsx     # Recharts LineChart with dashed series support
├── features/                  # Feature-slice architecture
│   ├── overview/              # hooks/ + components/
│   ├── moderation/            # hooks/ + components/
│   ├── analytics/             # hooks/ + components/
│   ├── ai-engine/             # hooks/ + components/
│   ├── telegram/              # hooks/ + components/
│   ├── blacklist/             # hooks/ + components/
│   └── users/                 # hooks/
├── providers/
│   ├── theme-provider.tsx     # next-themes wrapper
│   ├── query-provider.tsx     # TanStack Query provider + devtools
│   └── index.tsx              # Combined provider tree
└── shared/
    ├── stores/
    │   ├── ui.store.ts        # Sidebar collapse (persisted)
    │   ├── auth.store.ts      # Auth session + login action
    │   └── realtime.store.ts  # WebSocket event buffer + system health
    ├── hooks/
    │   ├── useWebSocket.ts    # Auto-reconnecting WebSocket hook
    │   └── use-realtime-feed.ts  # Realtime moderation event consumer
    ├── lib/
    │   ├── api-client.ts      # Typed fetch client with JWT injection
    │   ├── query-client.ts    # TanStack Query config
    │   └── utils.ts           # cn(), formatNumber, formatPercent, formatRelativeTime…
    └── config/
        └── navigation.ts      # Sidebar nav tree (icon names + hrefs)
```

---

## Design System

### Glassmorphism Tokens

```css
/* Light mode */
--glass-bg: rgba(255, 255, 255, 0.8);
--glass-border: rgba(0, 0, 0, 0.06);

/* Dark mode */
--glass-bg: rgba(255, 255, 255, 0.04);
--glass-border: rgba(255, 255, 255, 0.07);
```

### Utility Classes

| Class | Description |
|---|---|
| `.glass` | Glassmorphism with backdrop-blur(12px) |
| `.glass-card` | Glass with drop shadow |
| `.neon-glow` | Blue neon box shadow |
| `.gradient-text` | Blue→purple gradient text |
| `.bg-grid` | Subtle dot grid background |
| `.sidebar-item-active` | Left border highlight + primary tint |
| `.status-dot-green/yellow/red` | Colored glow dot for status indicators |
| `.shine` | Hover shine sweep effect |
| `.animate-pulse-dot` | Breathing pulse animation |

### Threat Level Colors

| Level | Color |
|---|---|
| NONE | Emerald (#22c55e) |
| LOW | Lime (#84cc16) |
| MEDIUM | Amber (#f59e0b) |
| HIGH | Red (#ef4444) |
| CRITICAL | Violet (#7c3aed) |

---

## Realtime Integration

WebSocket connects to `NEXT_PUBLIC_WS_URL/ws/v1/moderation?token=<jwt>`.

Message format:
```json
{
  "channel": "moderation",
  "event": "moderation_event",
  "payload": { "eventId": "...", "groupTitle": "...", "confidence": 0.94 },
  "timestamp": "2025-01-01T00:00:00Z"
}
```

Events consumed:
- `moderation_event` → pushed into `useRealtimeStore.latestEvents` (capped at 100)
- `system_health` → updates `useRealtimeStore.systemHealth`

Auto-reconnects up to 10 times with 3s delay.

---

## Configuration

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

---

## Development

```bash
# From monorepo root
pnpm --filter @findspam/web dev

# Type check
pnpm --filter @findspam/web type-check

# Build
pnpm --filter @findspam/web build
```

---

## URL Structure

| URL | Page |
|---|---|
| `/` | → redirect to `/dashboard/overview` |
| `/login` | Login form |
| `/dashboard/overview` | KPI overview |
| `/dashboard/moderation/live` | Real-time event stream |
| `/dashboard/moderation/queue` | Pending review queue |
| `/dashboard/moderation/history` | Full event history |
| `/dashboard/analytics/spam-trends` | Volume + category charts |
| `/dashboard/analytics/threat-map` | Hourly heatmap |
| `/dashboard/analytics/model-performance` | Model metrics timeline |
| `/dashboard/ai-engine/predictions` | AI prediction history |
| `/dashboard/ai-engine/models` | Model registry |
| `/dashboard/ai-engine/training` | Training controls |
| `/dashboard/telegram/groups` | Monitored groups |
| `/dashboard/telegram/events` | Bot event log |
| `/dashboard/blacklist` | Blacklist management |
| `/dashboard/users` | Admin user management |
| `/dashboard/audit` | Audit log |
| `/dashboard/settings` | Platform configuration |
