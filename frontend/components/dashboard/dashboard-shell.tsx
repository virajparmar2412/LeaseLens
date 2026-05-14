import { KpiCards } from "@/components/dashboard/kpi-cards";
import { Sidebar } from "@/components/layout/sidebar";
import { Card } from "@/components/ui/card";

export function DashboardShell() {
  return (
    <div className="min-h-screen p-4 md:p-6">
      <div className="grid min-h-[calc(100vh-2rem)] gap-4 lg:grid-cols-[280px_1fr]">
        <Sidebar />
        <main className="space-y-4">
          <section className="rounded-[28px] bg-hero-grid p-8 shadow-card">
            <div className="max-w-3xl">
              <div className="text-xs uppercase tracking-[0.35em] text-teal-800">
                Analyst Workspace
              </div>
              <h1 className="mt-3 text-4xl font-semibold tracking-tight text-slate-900">
                AI rental pricing, grounded in comparables and analyst judgment.
              </h1>
              <p className="mt-4 max-w-2xl text-sm leading-6 text-slate-600">
                Use the property intake workflow to generate a recommended rent,
                inspect match-ranked comparables, and refine the outcome through natural-language feedback.
              </p>
            </div>
          </section>
          <KpiCards />
          <section className="grid gap-4 xl:grid-cols-[1.4fr_1fr]">
            <Card className="p-6">
              <div className="text-lg font-semibold">Recommended Page Build Order</div>
              <ol className="mt-4 space-y-3 text-sm text-slate-600">
                <li>1. Login page and authenticated app shell</li>
                <li>2. Property details input form</li>
                <li>3. Recommendation results page</li>
                <li>4. Comparable selection panel</li>
                <li>5. AI feedback chat and recalculation</li>
                <li>6. Analytics and admin views</li>
              </ol>
            </Card>
            <Card className="p-6">
              <div className="text-lg font-semibold">Prototype Priorities</div>
              <div className="mt-4 grid gap-3 text-sm text-slate-600">
                <div className="rounded-2xl bg-slate-50 p-4">
                  Deterministic pricing engine before LLM-based explanation.
                </div>
                <div className="rounded-2xl bg-slate-50 p-4">
                  Store analyst feedback separately from recommendation outputs.
                </div>
                <div className="rounded-2xl bg-slate-50 p-4">
                  Keep comparable ranking transparent and adjustable.
                </div>
              </div>
            </Card>
          </section>
        </main>
      </div>
    </div>
  );
}
