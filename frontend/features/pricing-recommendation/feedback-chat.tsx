"use client";

import { useState } from "react";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { useAnalysisStore } from "@/hooks/use-analysis-store";

const suggestions = [
  "Ignore properties near highways",
  "Increase importance of school quality",
  "This property should be priced more premium",
  "Reduce flood-risk weighting",
];

export function FeedbackChat() {
  const [value, setValue] = useState("");
  const analysis = useAnalysisStore((state) => state.analysis);
  const sendFeedback = useAnalysisStore((state) => state.sendFeedback);
  const isUpdating = useAnalysisStore((state) => state.isUpdating);
  const recommendation = analysis?.current_recommendation;

  if (!recommendation) {
    return null;
  }

  const submit = async () => {
    const next = value.trim();
    if (!next) {
      return;
    }
    setValue("");
    await sendFeedback(next);
  };

  return (
    <Card className="p-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="text-base font-semibold text-slate-900">
            AI Feedback Workspace
          </div>
          <div className="text-sm text-slate-500">
            Provide analyst feedback in natural language to update pricing logic.
          </div>
        </div>
        <div className="flex flex-wrap gap-2">
          {suggestions.map((suggestion) => (
            <button
              key={suggestion}
              type="button"
              className="rounded-full border border-slate-200 bg-white px-3 py-2 text-xs text-slate-600 transition hover:border-slate-300 hover:bg-slate-50"
              onClick={() => setValue(suggestion)}
            >
              {suggestion}
            </button>
          ))}
        </div>
      </div>

      <div className="mt-5 max-h-80 space-y-3 overflow-y-auto rounded-3xl bg-slate-50 p-4">
        {analysis.feedback_messages.map((message) => (
          <div
            key={message.id}
            className={`max-w-2xl rounded-3xl px-4 py-3 text-sm leading-6 ${
              message.role === "analyst"
                ? "ml-auto bg-slate-900 text-white"
                : "bg-white text-slate-700"
            }`}
          >
            {message.message_text}
          </div>
        ))}
      </div>

      <div className="mt-5 flex flex-col gap-3 md:flex-row">
        <textarea
          className="min-h-24 flex-1 rounded-3xl border border-slate-200 bg-white px-4 py-3 text-sm outline-none focus:border-accent"
          placeholder="Tell the pricing assistant what to adjust..."
          value={value}
          onChange={(event) => setValue(event.target.value)}
        />
        <Button className="md:self-end" disabled={isUpdating} onClick={submit} type="button">
          {isUpdating ? "Updating..." : "Send Feedback"}
        </Button>
      </div>
    </Card>
  );
}
