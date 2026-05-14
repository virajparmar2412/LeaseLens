import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

export default function LoginPage() {
  return (
    <main className="grid min-h-screen lg:grid-cols-[1.1fr_0.9fr]">
      <section className="bg-slatepanel px-8 py-16 text-white md:px-16">
        <div className="max-w-xl">
          <div className="text-xs uppercase tracking-[0.35em] text-teal-300">
            LeaseLens
          </div>
          <h1 className="mt-5 text-5xl font-semibold tracking-tight">
            Rental pricing intelligence for institutional-grade analysis.
          </h1>
          <p className="mt-6 text-sm leading-7 text-slate-300">
            Combine weighted property scoring, comparable ranking, neighborhood context, and AI-assisted explanation.
          </p>
        </div>
      </section>
      <section className="flex items-center justify-center px-6 py-16">
        <Card className="w-full max-w-md p-8">
          <div className="text-2xl font-semibold text-slate-900">Sign in</div>
          <p className="mt-2 text-sm text-slate-500">
            Connect to the analyst workspace.
          </p>
          <div className="mt-6 space-y-4">
            <Input placeholder="Work email" />
            <Input placeholder="Password" type="password" />
            <Button className="w-full">Continue</Button>
          </div>
        </Card>
      </section>
    </main>
  );
}
