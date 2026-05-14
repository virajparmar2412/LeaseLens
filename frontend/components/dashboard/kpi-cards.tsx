import { Card } from "@/components/ui/card";

const metrics = [
  { label: "Active Pricing Runs", value: "128", delta: "+12.4%" },
  { label: "Avg. Confidence", value: "84%", delta: "+4.1%" },
  { label: "Override Rate", value: "17%", delta: "-2.8%" },
  { label: "Comp Match Health", value: "91%", delta: "+3.3%" },
];

export function KpiCards() {
  return (
    <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
      {metrics.map((metric) => (
        <Card key={metric.label} className="p-5">
          <div className="text-sm text-slate-500">{metric.label}</div>
          <div className="mt-3 text-3xl font-semibold text-slate-900">
            {metric.value}
          </div>
          <div className="mt-2 text-sm text-teal-700">{metric.delta}</div>
        </Card>
      ))}
    </div>
  );
}
