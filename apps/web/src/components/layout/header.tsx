"use client";

import { useTheme } from "next-themes";
import { Bell, Sun, Moon, Search, Monitor } from "lucide-react";
import { useState, useCallback } from "react";
import { cn } from "@/shared/lib/utils";
import { useRealtimeStore } from "@/shared/stores/realtime.store";
import { useUIStore } from "@/shared/stores/ui.store";

function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  const cycle = useCallback(() => {
    if (theme === "dark") setTheme("light");
    else if (theme === "light") setTheme("system");
    else setTheme("dark");
  }, [theme, setTheme]);

  return (
    <button
      onClick={cycle}
      className="flex h-8 w-8 items-center justify-center rounded-lg text-muted-foreground hover:bg-muted/60 hover:text-foreground transition-all duration-150"
      title={`Theme: ${theme}`}
    >
      {theme === "dark" ? (
        <Moon className="h-4 w-4" />
      ) : theme === "light" ? (
        <Sun className="h-4 w-4" />
      ) : (
        <Monitor className="h-4 w-4" />
      )}
    </button>
  );
}

function ConnectionBadge() {
  const status = useRealtimeStore((s) => s.status);
  return (
    <div className="flex items-center gap-1.5 rounded-full bg-muted/50 px-2.5 py-1 text-xs">
      <span
        className={cn("h-1.5 w-1.5 rounded-full", {
          "status-dot-green animate-pulse-dot": status === "connected",
          "status-dot-yellow": status === "connecting",
          "status-dot-red": status === "disconnected" || status === "error",
        })}
      />
      <span className="text-muted-foreground capitalize">{status}</span>
    </div>
  );
}

export function Header() {
  const [query, setQuery] = useState("");
  const { notificationsPanelOpen, setNotificationsPanelOpen } = useUIStore();

  return (
    <header className="flex h-[60px] shrink-0 items-center gap-4 border-b border-border/50 bg-card/60 px-6 backdrop-blur-xl">
      {/* Search */}
      <div className="relative flex-1 max-w-md">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-muted-foreground" />
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search events, users, domains…"
          className="h-8 w-full rounded-lg border border-border/50 bg-muted/30 pl-9 pr-4 text-sm text-foreground placeholder:text-muted-foreground/60 focus:outline-none focus:ring-1 focus:ring-ring transition-all"
        />
      </div>

      <div className="ml-auto flex items-center gap-2">
        <ConnectionBadge />
        <ThemeToggle />

        {/* Notifications */}
        <button
          onClick={() => setNotificationsPanelOpen(!notificationsPanelOpen)}
          className="relative flex h-8 w-8 items-center justify-center rounded-lg text-muted-foreground hover:bg-muted/60 hover:text-foreground transition-all duration-150"
        >
          <Bell className="h-4 w-4" />
          <span className="absolute right-1.5 top-1.5 h-1.5 w-1.5 rounded-full bg-primary" />
        </button>

        {/* Avatar */}
        <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary/10 ring-1 ring-primary/20 text-xs font-semibold text-primary">
          A
        </div>
      </div>
    </header>
  );
}
