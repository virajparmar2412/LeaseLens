import Link from "next/link";
import { BarChart3, Bot, Building2, History, LayoutDashboard, Map, Shield } from "lucide-react";

import { Button } from "@/components/ui/button";

const navItems = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/dashboard/new-analysis", label: "New Analysis", icon: Bot },
  { href: "/dashboard/history", label: "History", icon: History },
  { href: "/properties", label: "Properties", icon: Building2 },
  { href: "/recommendations", label: "Recommendations", icon: Bot },
  { href: "/analytics", label: "Analytics", icon: BarChart3 },
  { href: "/maps", label: "Location Intel", icon: Map },
];

export function Sidebar() {
  return (
    <aside className="flex h-full flex-col rounded-[28px] bg-slatepanel p-6 text-white">
      <div className="mb-8">
        <div className="text-xs uppercase tracking-[0.3em] text-teal-200">
          LeaseLens
        </div>
        <div className="mt-2 text-2xl font-semibold">Pricing OS</div>
      </div>
      <nav className="space-y-2">
        {navItems.map(({ href, label, icon: Icon }) => (
          <Link
            key={href}
            href={href}
            className="flex items-center gap-3 rounded-2xl px-4 py-3 text-sm text-slate-200 transition hover:bg-white/10 hover:text-white"
          >
            <Icon className="h-4 w-4" />
            {label}
          </Link>
        ))}
      </nav>
      <Link href="/dashboard/new-analysis" className="mt-6">
        <Button className="w-full bg-white text-slate-900 hover:bg-slate-100">
          Start Pricing Run
        </Button>
      </Link>
      <div className="mt-auto rounded-3xl border border-white/10 bg-white/5 p-4">
        <div className="flex items-center gap-2 text-sm font-medium">
          <Shield className="h-4 w-4 text-teal-300" />
          Enterprise Controls
        </div>
        <p className="mt-2 text-xs leading-5 text-slate-300">
          Recommendation history, analyst overrides, and audit-friendly logic versioning belong here.
        </p>
      </div>
    </aside>
  );
}
