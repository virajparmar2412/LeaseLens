export type ComparableAdjustment = {
  id: string;
  action: string;
  previous_weight: number;
  new_weight: number;
  previous_status: string;
  new_status: string;
  created_at: string;
};

export type ComparableModel = {
  id: string;
  property_name: string;
  address: string;
  monthly_rent: number;
  bedrooms: number;
  bathrooms: number;
  area_sqft: number;
  distance_miles: number;
  similarity_score: number;
  match_percentage: number;
  selection_reason: string;
  key_matching_factors: string[];
  weight: number;
  status: string;
  adjustments: ComparableAdjustment[];
};

export type RecommendationSnapshot = {
  id: string;
  version_number: number;
  recommended_rent: number;
  rent_low: number;
  rent_high: number;
  confidence_score: number;
  price_per_sqft: number;
  reasoning_summary: string;
  market_trend_indicator: string;
  pricing_factors: { name: string; value: number }[];
  neighborhood_summary: { label: string; score: number }[];
  triggered_by: string;
  created_at: string;
  comparables: ComparableModel[];
};

export type FeedbackMessage = {
  id: string;
  role: string;
  message_text: string;
  parsed_intent: string;
  pricing_adjustment: number;
  affected_recommendation_version: number;
  created_at: string;
};

export type RecommendationHistoryItem = {
  id: string;
  recommendation_id: string;
  previous_recommendation_value: number;
  new_recommendation_value: number;
  previous_confidence_score: number;
  new_confidence_score: number;
  change_reason: string;
  trigger_type: string;
  created_at: string;
};

export type RecommendationEvent = {
  id: string;
  event_type: string;
  event_summary: string;
  metadata: Record<string, unknown>;
  created_at: string;
};

export type AnalysisDetail = {
  id: string;
  property_name: string;
  address: string;
  city: string;
  state: string;
  zip_code: string;
  property_type: string;
  status: string;
  analyst_notes?: string | null;
  amenities: string[];
  current_recommendation: RecommendationSnapshot | null;
  feedback_messages: FeedbackMessage[];
  recommendation_history: RecommendationHistoryItem[];
  recommendation_events: RecommendationEvent[];
};

export type AnalysisListItem = {
  id: string;
  property_name: string;
  city: string;
  property_type: string;
  status: string;
  latest_recommendation_value?: number | null;
  latest_confidence_score?: number | null;
  updated_at: string;
};

export type AnalysisListResponse = {
  items: AnalysisListItem[];
  total: number;
  page: number;
  page_size: number;
};
