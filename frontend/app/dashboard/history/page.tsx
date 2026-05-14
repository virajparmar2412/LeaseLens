import Link from "next/link";

import { Sidebar } from "@/components/layout/sidebar";
import { Card } from "@/components/ui/card";
import { listAnalyses } from "@/services/analyses";

export default async function HistoryPage({
  searchParams,
}: {
  searchParams?: Promise<{ city?: string; property_type?: string; search?: string }>;
}) {
  const params = (await searchParams) ?? {};
  const data = await listAnalyses({
    city: params.city,
    propertyType: params.property_type,
    search: params.search,
    page: 1,
    pageSize: 20,
  });

  return (
    <main className="min-h-screen p-4 md:p-6">
      <div className="grid min-h-[calc(100vh-2rem)] gap-4 lg:grid-cols-[280px_1fr]">
        <Sidebar />
        <div className="space-y-6">
          <section className="rounded-[30px] bg-hero-grid p-8 shadow-card">
            <div className="max-w-3xl">
              <div className="text-xs uppercase tracking-[0.32em] text-teal-800">
                Analysis History
              </div>
              <h1 className="mt-3 text-4xl font-semibold tracking-tight text-slate-900">
                Reopen saved pricing sessions and inspect recommendation evolution.
              </h1>
            </div>
          </section>

          <Card className="p-6">
            <div className="mb-4 flex items-center justify-between">
              <div className="text-lg font-semibold text-slate-900">Recent Analyses</div>
              <div className="text-sm text-slate-500">{data.total} saved sessions</div>
            </div>
            {data.items.length === 0 ? (
              <div className="rounded-3xl border border-dashed border-slate-200 p-10 text-center text-sm text-slate-500">
                No saved analyses yet. Run a pricing analysis to start building history.
              </div>
            ) : (
              <div className="space-y-3">
                {data.items.map((item) => (
                  <Link key={item.id} href={`/dashboard/history/${item.id}`}>
                    <div className="rounded-3xl border border-slate-200 bg-white p-5 transition hover:shadow-card">
                      <div className="flex flex-wrap items-start justify-between gap-4">
                        <div>
                          <div className="text-lg font-semibold text-slate-900">
                            {item.property_name}
                          </div>
                          <div className="mt-1 text-sm text-slate-500">
                            {item.city} • {item.property_type}
                          </div>
                        </div>
                        <div className="text-right">
                          <div className="text-xl font-semibold text-slate-900">
                            {item.latest_recommendation_value
                              ? `$${item.latest_recommendation_value.toLocaleString()}`
                              : "No recommendation"}
                          </div>
                          <div className="text-sm text-teal-700">
                            {item.latest_confidence_score
                              ? `${Math.round(item.latest_confidence_score * 100)}% confidence`
                              : "Pending"}
                          </div>
                        </div>
                      </div>
                    </div>
                  </Link>
                ))}
              </div>
            )}
          </Card>
        </div>
      </div>
    </main>
  );
}
