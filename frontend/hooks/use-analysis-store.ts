"use client";

import { create } from "zustand";

import {
  createAnalysis,
  getAnalysis,
  recalculateAnalysis,
} from "@/services/analyses";
import type { AnalysisDetail } from "@/types/analysis";
import type {
  ComparableActionType,
  RecommendationPayload,
} from "@/types/pricing";

type ChatMessage = {
  id: string;
  role: "analyst" | "assistant";
  content: string;
};

type AnalysisStore = {
  activePayload: RecommendationPayload | null;
  analysis: AnalysisDetail | null;
  isSubmitting: boolean;
  isUpdating: boolean;
  isLoadingAnalysis: boolean;
  error: string | null;
  generate: (payload: RecommendationPayload) => Promise<void>;
  sendFeedback: (feedbackText: string) => Promise<void>;
  adjustComparable: (
    comparableId: string,
    action: ComparableActionType,
  ) => Promise<void>;
  loadAnalysis: (analysisId: string) => Promise<void>;
};

const assistantMessage = (content: string): ChatMessage => ({
  id: `${Date.now()}-${Math.random()}`,
  role: "assistant",
  content,
});

const analystMessage = (content: string): ChatMessage => ({
  id: `${Date.now()}-${Math.random()}`,
  role: "analyst",
  content,
});

export const useAnalysisStore = create<AnalysisStore>((set, get) => ({
  activePayload: null,
  analysis: null,
  isSubmitting: false,
  isUpdating: false,
  isLoadingAnalysis: false,
  error: null,
  async generate(payload) {
    set({ isSubmitting: true, error: null, activePayload: payload });
    try {
      const analysis = await createAnalysis(payload);
      set({
        analysis,
        isSubmitting: false,
      });
    } catch (error) {
      set({
        isSubmitting: false,
        error: error instanceof Error ? error.message : "Failed to generate recommendation.",
      });
    }
  },
  async sendFeedback(feedbackText) {
    const analysis = get().analysis;
    if (!analysis || !feedbackText.trim()) {
      return;
    }

    set({ isUpdating: true, error: null });

    try {
      const nextAnalysis = await recalculateAnalysis(analysis.id, {
        recommendationId: analysis.current_recommendation?.version_number ?? 0,
        feedbackText,
      });
      set({ analysis: nextAnalysis, isUpdating: false });
    } catch (error) {
      set({
        isUpdating: false,
        error: error instanceof Error ? error.message : "Failed to update recommendation.",
      });
    }
  },
  async adjustComparable(comparableId, action) {
    const analysis = get().analysis;
    if (!analysis) {
      return;
    }

    set({ isUpdating: true, error: null });

    try {
      const nextAnalysis = await recalculateAnalysis(analysis.id, {
        recommendationId: analysis.current_recommendation?.version_number ?? 0,
        comparableActions: [{ comparableId, action }],
      });
      set({ analysis: nextAnalysis, isUpdating: false });
    } catch (error) {
      set({
        isUpdating: false,
        error: error instanceof Error ? error.message : "Failed to adjust comparable.",
      });
    }
  },
  async loadAnalysis(analysisId) {
    set({ isLoadingAnalysis: true, error: null });
    try {
      const analysis = await getAnalysis(analysisId);
      set({ analysis, isLoadingAnalysis: false });
    } catch (error) {
      set({
        isLoadingAnalysis: false,
        error: error instanceof Error ? error.message : "Failed to load analysis.",
      });
    }
  },
}));
