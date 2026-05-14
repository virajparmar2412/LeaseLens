export type PropertyInput = {
  propertyName: string;
  address: string;
  city: string;
  state: string;
  zipCode: string;
  propertyType: string;
  bedrooms: number;
  bathrooms: number;
  areaSqft: number;
  yearBuilt: number;
  furnishingStatus: string;
  floorNumber: number;
  parkingSpaces: number;
  parkingAvailability: string;
  hasGym: boolean;
  hasPool: boolean;
  petFriendly: boolean;
  gatedCommunity: boolean;
  nearbyMetroDistance: number;
  amenities: string[];
};

export type NeighborhoodMetricsInput = {
  schoolQualityScore: number;
  floodRiskScore: number;
  transitScore: number;
  roadNoiseScore: number;
  neighborhoodAppealScore: number;
};

export type RecommendationPayload = {
  property: PropertyInput;
  neighborhood: NeighborhoodMetricsInput;
  analystNotes?: string;
};

export type ComparableProperty = {
  id: number;
  propertyName: string;
  address: string;
  monthlyRent: number;
  distanceMiles: number;
  similarityScore: number;
  matchPercentage: number;
  selectionReason: string;
  bedrooms: number;
  bathrooms: number;
  areaSqft: number;
  keyMatchingFactors: string[];
  weight: number;
  status: string;
};

export type RecommendationResponse = {
  recommendationId: number;
  recommendedRent: number;
  rentLow: number;
  rentHigh: number;
  confidenceScore: number;
  reasoningSummary: string;
  pricePerSqft: number;
  marketTrendIndicator: string;
  pricingFactors: { name: string; value: number }[];
  neighborhoodSummary: { label: string; score: number }[];
  comparables: ComparableProperty[];
};

export type ComparableActionType =
  | "remove"
  | "increase_weight"
  | "decrease_weight"
  | "mark_irrelevant";

export type UpdateRecommendationPayload = {
  recommendationId: number;
  feedbackText?: string;
  comparableActions?: {
    comparableId: string;
    action: ComparableActionType;
  }[];
};

export type FeedbackResponse = {
  updatedRecommendation: RecommendationResponse;
  parsedIntent: string;
  pricingAdjustment: number;
};
