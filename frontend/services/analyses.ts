import type { AnalysisDetail, AnalysisListResponse } from "@/types/analysis";
import type { RecommendationPayload, UpdateRecommendationPayload } from "@/types/pricing";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
    cache: "no-store",
  });
  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Request failed: ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export async function createAnalysis(
  payload: RecommendationPayload,
): Promise<AnalysisDetail> {
  return request("/analyses", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function recalculateAnalysis(
  analysisId: string,
  payload: UpdateRecommendationPayload,
): Promise<AnalysisDetail> {
  return request(`/analyses/${analysisId}/recalculate`, {
    method: "POST",
    body: JSON.stringify({
      feedback_text: payload.feedbackText,
      comparable_actions: payload.comparableActions?.map((action) => ({
        comparable_id: action.comparableId,
        action: action.action,
      })),
    }),
  });
}

export async function listAnalyses(params?: {
  page?: number;
  pageSize?: number;
  city?: string;
  propertyType?: string;
  search?: string;
}): Promise<AnalysisListResponse> {
  const searchParams = new URLSearchParams();
  if (params?.page) searchParams.set("page", String(params.page));
  if (params?.pageSize) searchParams.set("page_size", String(params.pageSize));
  if (params?.city) searchParams.set("city", params.city);
  if (params?.propertyType) searchParams.set("property_type", params.propertyType);
  if (params?.search) searchParams.set("search", params.search);
  const suffix = searchParams.toString() ? `?${searchParams.toString()}` : "";
  return request(`/analyses${suffix}`);
}

export async function getAnalysis(analysisId: string): Promise<AnalysisDetail> {
  return request(`/analyses/${analysisId}`);
}

export async function getAnalysisHistory(analysisId: string) {
  return request(`/analyses/${analysisId}/history`);
}
