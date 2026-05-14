"use client";

import { useEffect } from "react";

import { AnalysisForm } from "@/features/pricing-recommendation/analysis-form";
import { RecommendationResults } from "@/features/pricing-recommendation/recommendation-results";
import { useAnalysisStore } from "@/hooks/use-analysis-store";

export function AnalysisWorkspace({ analysisId }: { analysisId?: string }) {
  const loadAnalysis = useAnalysisStore((state) => state.loadAnalysis);
  const isLoadingAnalysis = useAnalysisStore((state) => state.isLoadingAnalysis);
  const error = useAnalysisStore((state) => state.error);

  useEffect(() => {
    if (analysisId) {
      void loadAnalysis(analysisId);
    }
  }, [analysisId, loadAnalysis]);

  return (
    <div className="space-y-6">
      {isLoadingAnalysis ? (
        <div className="rounded-3xl border border-slate-200 bg-white/80 p-6 text-sm text-slate-500 shadow-card">
          Loading saved analysis...
        </div>
      ) : null}
      {error ? (
        <div className="rounded-3xl border border-rose-200 bg-rose-50 p-4 text-sm text-rose-700">
          {error}
        </div>
      ) : null}
      <AnalysisForm />
      <RecommendationResults />
    </div>
  );
}
