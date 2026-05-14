"use client";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { useAnalysisStore } from "@/hooks/use-analysis-store";
import type { ComparableActionType } from "@/types/pricing";

const actions: { label: string; action: ComparableActionType }[] = [
  { label: "Increase Weight", action: "increase_weight" },
  { label: "Decrease Weight", action: "decrease_weight" },
  { label: "Remove", action: "remove" },
  { label: "Mark Irrelevant", action: "mark_irrelevant" },
];

export function ComparablePanel() {
  const analysis = useAnalysisStore((state) => state.analysis);
  const adjustComparable = useAnalysisStore((state) => state.adjustComparable);
  const isUpdating = useAnalysisStore((state) => state.isUpdating);
  const recommendation = analysis?.current_recommendation;

  if (!recommendation) {
    return null;
  }

  return (
    <Card className="p-6">
      <div className="mb-4 flex items-center justify-between">
        <div>
          <div className="text-base font-semibold text-slate-900">
            Comparable Properties
          </div>
          <div className="text-sm text-slate-500">
            Rank, exclude, and reweight comps to refine the recommendation.
          </div>
        </div>
      </div>
      <div className="space-y-4">
        {recommendation.comparables.map((comp) => (
          <div
            key={comp.id}
            className={`rounded-3xl border p-5 transition ${
              comp.status === "active"
                ? "border-slate-200 bg-white hover:shadow-card"
                : "border-slate-200 bg-slate-50 opacity-80"
            }`}
          >
            <div className="flex items-start justify-between gap-4">
              <div>
                <div className="text-lg font-semibold text-slate-900">
                  {comp.property_name}
                </div>
                <div className="mt-1 text-sm text-slate-500">{comp.address}</div>
              </div>
              <div className="text-right">
                <div className="text-xl font-semibold text-slate-900">
                  ${comp.monthly_rent.toLocaleString()}
                </div>
                <div className="text-sm text-teal-700">{comp.match_percentage}% match</div>
              </div>
            </div>
            <div className="mt-4 grid gap-3 text-sm text-slate-600 md:grid-cols-3">
              <div>{comp.distance_miles} mi away</div>
              <div>Weight {comp.weight.toFixed(2)}</div>
              <div className="capitalize">{comp.status}</div>
            </div>
            <div className="mt-4 text-sm leading-6 text-slate-600">
              {comp.selection_reason}
            </div>
            <div className="mt-4 flex flex-wrap gap-2">
              {comp.key_matching_factors.map((factor) => (
                <span
                  key={factor}
                  className="rounded-full bg-slate-100 px-3 py-1 text-xs text-slate-600"
                >
                  {factor}
                </span>
              ))}
            </div>
            <div className="mt-5 flex flex-wrap gap-2">
              {actions.map(({ label, action }) => (
                <Button
                  key={action}
                  className="bg-white text-slate-800 ring-1 ring-slate-200 hover:bg-slate-50"
                  disabled={isUpdating}
                  onClick={() => adjustComparable(comp.id, action)}
                  type="button"
                >
                  {label}
                </Button>
              ))}
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
}
