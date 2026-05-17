"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import {
  LayoutDashboard,
  Shield,
  BarChart3,
  Brain,
  Send,
  Ban,
  UserCog,
  FileText,
  Settings,
  Activity,
  ListChecks,
  History,
  TrendingUp,
  Map,
  Cpu,
  Zap,
  RefreshCw,
  Package,
  Users,
  Bell,
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  Zap as ZapIcon,
} from "lucide-react";
import { cn } from "@/shared/lib/utils";
import { useUIStore } from "@/shared/stores/ui.store";
import { NAVIGATION } from "@/config/navigation";
import type { NavItem } from "@/config/navigation";

const ICON_MAP: Record<string, React.ComponentType<{ className?: string }>> = {
  LayoutDashboard,
  Shield,
  BarChart3,
  Brain,
  Send,
  Ban,
  UserCog,
  FileText,
  Settings,
  Activity,
  ListChecks,
  History,
  TrendingUp,
  Map,
  Cpu,
  Zap,
  RefreshCw,
  Package,
  Users,
  Bell,
};

function NavIcon({ name, className }: { name: string; className?: string }) {
  const Icon = ICON_MAP[name] ?? ZapIcon;
  return <Icon className={className} />;
}

function NavItemComponent({
  item,
  collapsed,
  depth = 0,
}: {
  item: NavItem;
  collapsed: boolean;
  depth?: number;
}) {
  const pathname = usePathname();
  const [open, setOpen] = useState(() =>
    item.children?.some((c) => pathname.startsWith(c.href)) ?? false,
  );

  const isActive = pathname === item.href || pathname.startsWith(item.href + "/");
  const hasChildren = Boolean(item.children?.length);

  if (hasChildren) {
    return (
      <div>
        <button
          onClick={() => setOpen((o) => !o)}
          className={cn(
            "flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-all duration-150",
            isActive
              ? "text-primary"
              : "text-muted-foreground hover:text-foreground hover:bg-muted/60",
          )}
        >
          <NavIcon name={item.icon} className="h-4 w-4 shrink-0" />
          {!collapsed && (
            <>
              <span className="flex-1 text-left">{item.label}</span>
              <ChevronDown
                className={cn(
                  "h-3.5 w-3.5 transition-transform duration-200",
                  open && "rotate-180",
                )}
              />
            </>
          )}
        </button>
        <AnimatePresence initial={false}>
          {open && !collapsed && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: "auto", opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              transition={{ duration: 0.2, ease: "easeInOut" }}
              className="overflow-hidden"
            >
              <div className="ml-4 mt-1 space-y-0.5 border-l border-border/50 pl-3">
                {item.children!.map((child) => (
                  <NavItemComponent
                    key={child.href}
                    item={child}
                    collapsed={false}
                    depth={depth + 1}
                  />
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    );
  }

  return (
    <Link
      href={item.href}
      title={collapsed ? item.label : undefined}
      className={cn(
        "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm transition-all duration-150",
        isActive
          ? "sidebar-item-active"
          : "sidebar-item-hover text-muted-foreground",
        depth > 0 && "py-2 text-xs",
      )}
    >
      <NavIcon name={item.icon} className="h-4 w-4 shrink-0" />
      {!collapsed && <span>{item.label}</span>}
    </Link>
  );
}

export function Sidebar() {
  const { sidebarCollapsed, toggleSidebar } = useUIStore();

  return (
    <motion.aside
      animate={{ width: sidebarCollapsed ? 64 : 240 }}
      transition={{ duration: 0.25, ease: "easeInOut" }}
      className="relative flex h-full flex-col border-r border-border/50 bg-card/80 backdrop-blur-xl"
    >
      {/* Logo */}
      <div className="flex h-[60px] items-center border-b border-border/50 px-4">
        <div className="flex items-center gap-2.5">
          <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-primary/10 ring-1 ring-primary/20">
            <Shield className="h-4 w-4 text-primary" />
          </div>
          {!sidebarCollapsed && (
            <motion.div
              initial={{ opacity: 0, x: -8 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -8 }}
              transition={{ duration: 0.15 }}
            >
              <span className="gradient-text text-sm font-bold tracking-tight">
                FindSpam
              </span>
              <p className="text-[10px] text-muted-foreground leading-none mt-0.5">
                Admin Dashboard
              </p>
            </motion.div>
          )}
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto p-3 space-y-0.5">
        {NAVIGATION.map((item) => (
          <NavItemComponent
            key={item.href}
            item={item}
            collapsed={sidebarCollapsed}
          />
        ))}
      </nav>

      {/* Collapse Toggle */}
      <div className="border-t border-border/50 p-3">
        <button
          onClick={toggleSidebar}
          className="flex w-full items-center justify-center gap-2 rounded-lg px-3 py-2 text-xs text-muted-foreground hover:bg-muted/60 hover:text-foreground transition-all duration-150"
        >
          {sidebarCollapsed ? (
            <ChevronRight className="h-4 w-4" />
          ) : (
            <>
              <ChevronLeft className="h-4 w-4" />
              <span>Collapse</span>
            </>
          )}
        </button>
      </div>
    </motion.aside>
  );
}
