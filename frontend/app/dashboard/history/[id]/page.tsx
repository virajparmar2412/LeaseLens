import Link from "next/link";

import { Sidebar } from "@/components/layout/sidebar";
import { Card } from "@/components/ui/card";
import { getAnalysis } from "@/services/analyses";

export default async function AnalysisDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const analysis = await getAnalysis(id);
  const recommendation = analysis.current_recommendation;

  return (
    <main className="min-h-screen p-4 md:p-6">
      <div className="grid min-h-[calc(100vh-2rem)] gap-4 lg:grid-cols-[280px_1fr]">
        <Sidebar />
        <div className="space-y-6">
          <section className="rounded-[30px] bg-hero-grid p-8 shadow-card">
            <div className="flex flex-wrap items-center justify-between gap-4">
              <div>
                <div className="text-xs uppercase tracking-[0.32em] text-teal-800">
                  Analysis Detail
                </div>
                <h1 className="mt-3 text-4xl font-semibold tracking-tight text-slate-900">
                  {analysis.property_name}
                </h1>
                <p className="mt-2 text-sm text-slate-600">
                  {analysis.city}, {analysis.state} • {analysis.property_type}
                </p>
              </div>
              <Link
                href={`/dashboard/new-analysis?analysisId=${analysis.id}`}
                className="rounded-2xl bg-slate-900 px-4 py-3 text-sm font-semibold text-white"
              >
                Reopen Analysis
              </Link>
            </div>
          </section>

          <div className="grid gap-6 xl:grid-cols-[1.15fr_0.85fr]">
            <Card className="p-6">
              <div className="text-lg font-semibold text-slate-900">Recommendation Timeline</div>
              <div className="mt-5 space-y-4">
                {analysis.recommendation_history.length === 0 ? (
                  <div className="rounded-3xl border border-dashed border-slate-200 p-8 text-sm text-slate-500">
                    No revisions yet. This analysis still reflects the initial recommendation.
                  </div>
                ) : (
                  analysis.recommendation_history.map((item) => (
                    <div key={item.id} className="rounded-3xl border border-slate-200 p-4">
                      <div className="flex items-center justify-between text-sm">
                        <span className="font-medium text-slate-900">{item.trigger_type}</span>
                        <span className="text-slate-500">
                          {new Date(item.created_at).toLocaleString()}
                        </span>
                      </div>
                      <div className="mt-2 text-sm text-slate-600">{item.change_reason}</div>
                      <div className="mt-3 flex gap-6 text-sm text-slate-700">
                        <span>${item.previous_recommendation_value.toLocaleString()}</span>
                        <span>→</span>
                        <span className="font-semibold">
                          ${item.new_recommendation_value.toLocaleString()}
                        </span>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </Card>

            <div className="space-y-6">
              <Card className="p-6">
                <div className="text-lg font-semibold text-slate-900">Current Snapshot</div>
                {recommendation ? (
                  <div className="mt-4 space-y-3">
                    <div className="text-4xl font-semibold text-slate-900">
                      ${recommendation.recommended_rent.toLocaleString()}
                    </div>
                    <div className="text-sm text-slate-500">
                      Version {recommendation.version_number} •{" "}
                      {Math.round(recommendation.confidence_score * 100)}% confidence
                    </div>
                    <div className="text-sm leading-6 text-slate-600">
                      {recommendation.reasoning_summary}
                    </div>
                  </div>
                ) : null}
              </Card>

              <Card className="p-6">
                <div className="text-lg font-semibold text-slate-900">Feedback History</div>
                <div className="mt-4 space-y-3">
                  {analysis.feedback_messages.map((message) => (
                    <div key={message.id} className="rounded-2xl bg-slate-50 p-4">
                      <div className="text-xs uppercase tracking-[0.2em] text-slate-500">
                        {message.role}
                      </div>
                      <div className="mt-2 text-sm text-slate-700">
                        {message.message_text}
                      </div>
                    </div>
                  ))}
                </div>
              </Card>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
