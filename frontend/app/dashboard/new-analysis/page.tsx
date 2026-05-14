import { Sidebar } from "@/components/layout/sidebar";
import { AnalysisWorkspace } from "@/features/pricing-recommendation/analysis-workspace";

export default async function NewAnalysisPage({
  searchParams,
}: {
  searchParams?: Promise<{ analysisId?: string }>;
}) {
  const params = (await searchParams) ?? {};
  return (
    <main className="min-h-screen p-4 md:p-6">
      <div className="grid min-h-[calc(100vh-2rem)] gap-4 lg:grid-cols-[280px_1fr]">
        <Sidebar />
        <div className="space-y-6">
          <section className="rounded-[30px] bg-hero-grid p-8 shadow-card">
            <div className="max-w-3xl">
              <div className="text-xs uppercase tracking-[0.32em] text-teal-800">
                New Analysis
              </div>
              <h1 className="mt-3 text-4xl font-semibold tracking-tight text-slate-900">
                Generate and refine a rental pricing recommendation.
              </h1>
              <p className="mt-4 text-sm leading-7 text-slate-600">
                Enter subject property details, review ranked comparable properties,
                and refine the pricing band through deterministic analyst feedback.
              </p>
            </div>
          </section>

          <AnalysisWorkspace analysisId={params.analysisId} />
        </div>
      </div>
    </main>
  );
}
