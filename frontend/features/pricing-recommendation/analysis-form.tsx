"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import type { ReactNode } from "react";
import { z } from "zod";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { useAnalysisStore } from "@/hooks/use-analysis-store";
import type { RecommendationPayload } from "@/types/pricing";

const amenities = [
  "Gym",
  "Pool",
  "Clubhouse",
  "Security",
  "Coworking Lounge",
  "EV Charging",
];

const formSchema = z.object({
  propertyName: z.string().min(2),
  address: z.string().min(5),
  city: z.string().min(2),
  state: z.string().min(2),
  zipCode: z.string().min(4),
  propertyType: z.string().min(2),
  bedrooms: z.coerce.number().min(0),
  bathrooms: z.coerce.number().min(1),
  areaSqft: z.coerce.number().min(250),
  furnishingStatus: z.string(),
  floorNumber: z.coerce.number().min(0),
  parkingAvailability: z.string(),
  parkingSpaces: z.coerce.number().min(0),
  yearBuilt: z.coerce.number().min(1900),
  gatedCommunity: z.boolean(),
  nearbyMetroDistance: z.coerce.number().min(0),
  schoolQualityScore: z.coerce.number().min(0).max(10),
  roadNoiseScore: z.coerce.number().min(0).max(10),
  floodRiskScore: z.coerce.number().min(0).max(10),
  neighborhoodAppealScore: z.coerce.number().min(0).max(10),
  transitScore: z.coerce.number().min(0).max(10),
  hasGym: z.boolean(),
  hasPool: z.boolean(),
  petFriendly: z.boolean(),
  analystNotes: z.string().optional(),
  amenities: z.array(z.string()).min(1),
});

type FormValues = z.infer<typeof formSchema>;

const defaultValues: FormValues = {
  propertyName: "",
  address: "",
  city: "",
  state: "",
  zipCode: "",
  propertyType: "Apartment",
  bedrooms: 2,
  bathrooms: 2,
  areaSqft: 1200,
  furnishingStatus: "Semi Furnished",
  floorNumber: 4,
  parkingAvailability: "Covered",
  parkingSpaces: 1,
  yearBuilt: 2019,
  gatedCommunity: true,
  nearbyMetroDistance: 0.8,
  schoolQualityScore: 7,
  roadNoiseScore: 4,
  floodRiskScore: 3,
  neighborhoodAppealScore: 8,
  transitScore: 7,
  hasGym: true,
  hasPool: false,
  petFriendly: true,
  analystNotes: "",
  amenities: ["Gym", "Security"],
};

function Field({
  label,
  children,
  error,
}: {
  label: string;
  children: ReactNode;
  error?: string;
}) {
  return (
    <label className="block space-y-2">
      <span className="text-sm font-medium text-slate-700">{label}</span>
      {children}
      {error ? <span className="text-xs text-rose-600">{error}</span> : null}
    </label>
  );
}

export function AnalysisForm() {
  const generate = useAnalysisStore((state) => state.generate);
  const isSubmitting = useAnalysisStore((state) => state.isSubmitting);
  const error = useAnalysisStore((state) => state.error);

  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
    setValue,
  } = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues,
  });

  const selectedAmenities = watch("amenities");
  const schoolQualityScore = watch("schoolQualityScore");
  const roadNoiseScore = watch("roadNoiseScore");
  const floodRiskScore = watch("floodRiskScore");
  const neighborhoodAppealScore = watch("neighborhoodAppealScore");
  const transitScore = watch("transitScore");

  const onSubmit = async (values: FormValues) => {
    const payload: RecommendationPayload = {
      property: {
        propertyName: values.propertyName,
        address: values.address,
        city: values.city,
        state: values.state,
        zipCode: values.zipCode,
        propertyType: values.propertyType,
        bedrooms: values.bedrooms,
        bathrooms: values.bathrooms,
        areaSqft: values.areaSqft,
        yearBuilt: values.yearBuilt,
        furnishingStatus: values.furnishingStatus,
        floorNumber: values.floorNumber,
        parkingAvailability: values.parkingAvailability,
        parkingSpaces: values.parkingSpaces,
        hasGym: values.hasGym,
        hasPool: values.hasPool,
        petFriendly: values.petFriendly,
        gatedCommunity: values.gatedCommunity,
        nearbyMetroDistance: values.nearbyMetroDistance,
        amenities: values.amenities,
      },
      neighborhood: {
        schoolQualityScore: values.schoolQualityScore,
        floodRiskScore: values.floodRiskScore,
        transitScore: values.transitScore,
        roadNoiseScore: values.roadNoiseScore,
        neighborhoodAppealScore: values.neighborhoodAppealScore,
      },
      analystNotes: values.analystNotes,
    };

    await generate(payload);
  };

  const toggleAmenity = (amenity: string) => {
    const next = selectedAmenities.includes(amenity)
      ? selectedAmenities.filter((value) => value !== amenity)
      : [...selectedAmenities, amenity];
    setValue("amenities", next, { shouldValidate: true });
  };

  return (
    <form className="space-y-6" onSubmit={handleSubmit(onSubmit)}>
      <Card className="p-6">
        <div className="mb-5">
          <h2 className="text-xl font-semibold text-slate-900">Property Analysis Intake</h2>
          <p className="mt-1 text-sm text-slate-500">
            Capture subject property details and market context to generate a pricing recommendation.
          </p>
        </div>
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          <Field label="Property Name" error={errors.propertyName?.message}>
            <Input {...register("propertyName")} placeholder="Crescent Bay Residences" />
          </Field>
          <Field label="Address" error={errors.address?.message}>
            <Input {...register("address")} placeholder="1000 Market Street" />
          </Field>
          <Field label="City" error={errors.city?.message}>
            <Input {...register("city")} />
          </Field>
          <Field label="State" error={errors.state?.message}>
            <Input {...register("state")} />
          </Field>
          <Field label="Zip Code" error={errors.zipCode?.message}>
            <Input {...register("zipCode")} />
          </Field>
          <Field label="Property Type" error={errors.propertyType?.message}>
            <select className="w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm" {...register("propertyType")}>
              <option>Apartment</option>
              <option>Condo</option>
              <option>Townhome</option>
              <option>Villa</option>
            </select>
          </Field>
          <Field label="Bedrooms" error={errors.bedrooms?.message}>
            <Input type="number" {...register("bedrooms")} />
          </Field>
          <Field label="Bathrooms" error={errors.bathrooms?.message}>
            <Input type="number" step="0.5" {...register("bathrooms")} />
          </Field>
          <Field label="Square Feet" error={errors.areaSqft?.message}>
            <Input type="number" {...register("areaSqft")} />
          </Field>
          <Field label="Furnishing Status" error={errors.furnishingStatus?.message}>
            <select className="w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm" {...register("furnishingStatus")}>
              <option>Unfurnished</option>
              <option>Semi Furnished</option>
              <option>Fully Furnished</option>
            </select>
          </Field>
          <Field label="Floor Number" error={errors.floorNumber?.message}>
            <Input type="number" {...register("floorNumber")} />
          </Field>
          <Field label="Parking Availability" error={errors.parkingAvailability?.message}>
            <select className="w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm" {...register("parkingAvailability")}>
              <option>Covered</option>
              <option>Open</option>
              <option>Street</option>
              <option>None</option>
            </select>
          </Field>
          <Field label="Parking Spaces" error={errors.parkingSpaces?.message}>
            <Input type="number" {...register("parkingSpaces")} />
          </Field>
          <Field label="Year Built" error={errors.yearBuilt?.message}>
            <Input type="number" {...register("yearBuilt")} />
          </Field>
          <Field label="Nearby Metro Distance (mi)" error={errors.nearbyMetroDistance?.message}>
            <Input type="number" step="0.1" {...register("nearbyMetroDistance")} />
          </Field>
        </div>
      </Card>

      <Card className="p-6">
        <h3 className="text-lg font-semibold text-slate-900">Market Signals</h3>
        <div className="mt-5 grid gap-5 md:grid-cols-2">
          {[
            ["School Rating", "schoolQualityScore", schoolQualityScore] as const,
            ["Transit Score", "transitScore", transitScore] as const,
            ["Road Noise Level", "roadNoiseScore", roadNoiseScore] as const,
            ["Flood Risk Score", "floodRiskScore", floodRiskScore] as const,
            ["Neighborhood Appeal", "neighborhoodAppealScore", neighborhoodAppealScore] as const,
          ].map(([label, key, value]) => (
            <div key={String(key)} className="rounded-2xl border border-slate-200 p-4">
              <div className="flex items-center justify-between text-sm font-medium text-slate-700">
                <span>{label}</span>
                <span>{Number(value).toFixed(1)} / 10</span>
              </div>
              <input
                type="range"
                min="0"
                max="10"
                step="0.5"
                className="mt-4 w-full accent-teal-700"
                {...register(key, { valueAsNumber: true })}
              />
            </div>
          ))}
        </div>
      </Card>

      <Card className="p-6">
        <h3 className="text-lg font-semibold text-slate-900">Amenities and Positioning</h3>
        <div className="mt-4 flex flex-wrap gap-3">
          {amenities.map((amenity) => {
            const active = selectedAmenities.includes(amenity);
            return (
              <button
                key={amenity}
                type="button"
                onClick={() => toggleAmenity(amenity)}
                className={`rounded-full border px-4 py-2 text-sm transition ${
                  active
                    ? "border-teal-700 bg-teal-50 text-teal-800"
                    : "border-slate-200 bg-white text-slate-600 hover:border-slate-300"
                }`}
              >
                {amenity}
              </button>
            );
          })}
        </div>
        <div className="mt-5 grid gap-4 md:grid-cols-2">
          <label className="flex items-center gap-3 rounded-2xl border border-slate-200 p-4 text-sm text-slate-700">
            <input type="checkbox" {...register("gatedCommunity")} />
            Gated Community
          </label>
          <label className="flex items-center gap-3 rounded-2xl border border-slate-200 p-4 text-sm text-slate-700">
            <input type="checkbox" {...register("hasGym")} />
            On-site Gym
          </label>
          <label className="flex items-center gap-3 rounded-2xl border border-slate-200 p-4 text-sm text-slate-700">
            <input type="checkbox" {...register("hasPool")} />
            Swimming Pool
          </label>
          <label className="flex items-center gap-3 rounded-2xl border border-slate-200 p-4 text-sm text-slate-700">
            <input type="checkbox" {...register("petFriendly")} />
            Pet Friendly
          </label>
        </div>
        <Field label="Analyst Notes">
          <textarea
            className="min-h-28 w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm outline-none focus:border-accent"
            {...register("analystNotes")}
            placeholder="Optional context about property positioning, tenant target, or local conditions."
          />
        </Field>
      </Card>

      {error ? (
        <div className="rounded-2xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">
          {error}
        </div>
      ) : null}

      <div className="flex items-center justify-end">
        <Button className="min-w-48" disabled={isSubmitting}>
          {isSubmitting ? "Generating..." : "Generate Recommendation"}
        </Button>
      </div>
    </form>
  );
}
