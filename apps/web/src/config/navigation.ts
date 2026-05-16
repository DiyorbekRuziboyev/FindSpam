export interface NavItem {
  label: string;
  labelUz: string;
  href: string;
  icon: string;
  children?: NavItem[];
}

export const NAVIGATION: NavItem[] = [
  {
    label: "Overview",
    labelUz: "Umumiy",
    href: "/dashboard/overview",
    icon: "LayoutDashboard",
  },
  {
    label: "Moderation",
    labelUz: "Moderatsiya",
    href: "/dashboard/moderation/live",
    icon: "Shield",
    children: [
      { label: "Live Feed", labelUz: "Jonli tasmasi", href: "/dashboard/moderation/live", icon: "Activity" },
      { label: "Queue", labelUz: "Navbat", href: "/dashboard/moderation/queue", icon: "ListChecks" },
      { label: "History", labelUz: "Tarix", href: "/dashboard/moderation/history", icon: "History" },
    ],
  },
  {
    label: "Analytics",
    labelUz: "Tahlillar",
    href: "/dashboard/analytics/spam-trends",
    icon: "BarChart3",
    children: [
      { label: "Spam Trends", labelUz: "Spam trendlari", href: "/dashboard/analytics/spam-trends", icon: "TrendingUp" },
      { label: "Threat Map", labelUz: "Xavf xaritasi", href: "/dashboard/analytics/threat-map", icon: "Map" },
      { label: "Model Performance", labelUz: "Model samaradorligi", href: "/dashboard/analytics/model-performance", icon: "Cpu" },
    ],
  },
  {
    label: "AI Engine",
    labelUz: "AI Dvigatel",
    href: "/dashboard/ai-engine/predictions",
    icon: "Brain",
    children: [
      { label: "Predictions", labelUz: "Bashoratlar", href: "/dashboard/ai-engine/predictions", icon: "Zap" },
      { label: "Training", labelUz: "O'qitish", href: "/dashboard/ai-engine/training", icon: "RefreshCw" },
      { label: "Models", labelUz: "Modellar", href: "/dashboard/ai-engine/models", icon: "Package" },
    ],
  },
  {
    label: "Telegram",
    labelUz: "Telegram",
    href: "/dashboard/telegram/groups",
    icon: "Send",
    children: [
      { label: "Groups", labelUz: "Guruhlar", href: "/dashboard/telegram/groups", icon: "Users" },
      { label: "Events", labelUz: "Voqealar", href: "/dashboard/telegram/events", icon: "Bell" },
    ],
  },
  {
    label: "Blacklist",
    labelUz: "Qora ro'yxat",
    href: "/dashboard/blacklist",
    icon: "Ban",
  },
  {
    label: "Users",
    labelUz: "Foydalanuvchilar",
    href: "/dashboard/users",
    icon: "UserCog",
  },
  {
    label: "Audit Log",
    labelUz: "Audit jurnali",
    href: "/dashboard/audit",
    icon: "FileText",
  },
  {
    label: "Settings",
    labelUz: "Sozlamalar",
    href: "/dashboard/settings",
    icon: "Settings",
  },
];
