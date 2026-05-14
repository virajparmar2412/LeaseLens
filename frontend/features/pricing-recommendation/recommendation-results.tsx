"use client";

import {
  Bar,
  BarChart,
  CartesianGrid,
  PolarAngleAxis,
  PolarGrid,
  Radar,
  RadarChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { Card } from "@/components/ui/card";
import { useAnalysisStore } from "@/hooks/use-analysis-store";

import { ComparablePanel } from "./comparable-panel";
import { FeedbackChat } from "./feedback-chat";

function ConfidenceMeter({ value }: { value: number }) {
  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between text-sm text-slate-600">
        <span>Confidence Score</span>
        <span>{Math.round(value * 100)}%</span>
      </div>
      <div className="h-3 rounded-full bg-slate-100">
        <div
          className="h-3 rounded-full bg-gradient-to-r from-teal-500 to-emerald-400 transition-all"
          style={{ width: `${Math.round(value * 100)}%` }}
        />
      </div>
    </div>
  );
}

export function RecommendationResults() {
  const analysis = useAnalysisStore((state) => state.analysis);
  const isSubmitting = useAnalysisStore((state) => state.isSubmitting);
  const isUpdating = useAnalysisStore((state) => state.isUpdating);
  const recommendation = analysis?.current_recommendation;

  if (isSubmitting) {
    return (
      <Card className="p-8">
        <div className="animate-pulse space-y-4">
          <div className="h-6 w-56 rounded bg-slate-200" />
          <div className="h-24 rounded-3xl bg-slate-100" />
          <div className="grid gap-4 md:grid-cols-3">
            <div className="h-40 rounded-3xl bg-slate-100" />
            <div className="h-40 rounded-3xl bg-slate-100" />
            <div className="h-40 rounded-3xl bg-slate-100" />
          </div>
        </div>
      </Card>
    );
  }

  if (!analysis || !recommendation) {
    return (
      <Card className="flex min-h-72 items-center justify-center p-8 text-center">
        <div>
          <div className="text-lg font-semibold text-slate-900">
            No recommendation yet
          </div>
          <p className="mt-2 max-w-md text-sm text-slate-500">
            Complete the property analysis form to generate a pricing recommendation,
            comparable set, and analyst feedback workspace.
          </p>
        </div>
      </Card>
    );
  }

  const confidenceData = [
    { label: "Low", value: recommendation.rent_low },
    { label: "Recommended", value: recommendation.recommended_rent },
    { label: "High", value: recommendation.rent_high },
  ];

  const comparableWeights = recommendation.comparables.map((comp) => ({
    name: comp.property_name.split(" ")[0],
    weight: comp.weight,
    match: comp.match_percentage,
  }));

  return (
    <div className="space-y-6">
      <section className="grid gap-6 xl:grid-cols-[1.25fr_0.95fr]">
        <div className="space-y-6">
          <Card className="p-6">
            <div className="flex flex-wrap items-start justify-between gap-4">
              <div>
                <div className="text-sm font-medium uppercase tracking-[0.24em] text-teal-700">
                  Recommendation
                </div>
                <div className="mt-3 text-5xl font-semibold tracking-tight text-slate-900">
                  ${recommendation.recommended_rent.toLocaleString()}
                </div>
                <div className="mt-2 text-sm text-slate-500">
                  Range ${recommendation.rent_low.toLocaleString()} to $
                  {recommendation.rent_high.toLocaleString()} at $
                  {recommendation.price_per_sqft}/sq ft
                </div>
              </div>
              <div className="w-full max-w-sm rounded-3xl border border-slate-200 bg-slate-50 p-4">
                <ConfidenceMeter value={recommendation.confidence_score} />
                <div className="mt-4 text-xs leading-5 text-slate-500">
                  {recommendation.market_trend_indicator}
                </div>
              </div>
            </div>
            <p className="mt-6 text-sm leading-7 text-slate-600">
              {recommendation.reasoning_summary}
            </p>
            {isUpdating ? (
              <div className="mt-4 inline-flex rounded-full bg-amber-50 px-3 py-1 text-xs font-medium text-amber-700">
                Refreshing recommendation...
              </div>
            ) : null}
          </Card>

          <div className="grid gap-6 lg:grid-cols-2">
            <Card className="p-6">
              <div className="text-base font-semibold text-slate-900">
                Price Confidence
              </div>
              <div className="mt-4 h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={confidenceData}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} />
                    <XAxis dataKey="label" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="value" fill="#0f766e" radius={[10, 10, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </Card>
            <Card className="p-6">
              <div className="text-base font-semibold text-slate-900">
                Neighborhood Intelligence
              </div>
              <div className="mt-4 h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <RadarChart data={recommendation.neighborhood_summary}>
                    <PolarGrid />
                    <PolarAngleAxis dataKey="label" tick={{ fontSize: 11 }} />
                    <Radar
                      dataKey="score"
                      stroke="#0f766e"
                      fill="#14b8a6"
                      fillOpacity={0.35}
                    />
                  </RadarChart>
                </ResponsiveContainer>
              </div>
            </Card>
          </div>

          <Card className="p-6">
            <div className="text-base font-semibold text-slate-900">
              Pricing Factor Breakdown
            </div>
            <div className="mt-5 space-y-4">
              {recommendation.pricing_factors.map((factor) => (
                <div key={factor.name} className="space-y-2">
                  <div className="flex items-center justify-between text-sm text-slate-600">
                    <span>{factor.name}</span>
                    <span>{factor.value}%</span>
                  </div>
                  <div className="h-2 rounded-full bg-slate-100">
                    <div
                      className="h-2 rounded-full bg-slate-900 transition-all"
                      style={{ width: `${factor.value}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </div>

        <div className="space-y-6">
          <Card className="p-6">
            <div className="text-base font-semibold text-slate-900">
              Comparable Weighting
            </div>
            <div className="mt-4 h-72">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={comparableWeights}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="match" fill="#1f2937" radius={[8, 8, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </Card>
          <ComparablePanel />
        </div>
      </section>

      <FeedbackChat />
    </div>
  );
}
