import { redirect } from "next/navigation";
import type { Metadata } from "next";
import { LearnChat } from "@/components/LearnChat";
import { DEFAULT_MODE, modeById } from "@/lib/modes";

export const metadata: Metadata = { robots: { index: false, follow: false } };

export default async function OgrenPage({ searchParams }: PageProps<"/akis/ogren">) {
  const params = await searchParams;
  const reel = typeof params.reel === "string" ? params.reel : "";
  const choice = typeof params.choice === "string" ? params.choice.slice(0, 1) : "";
  const pack = typeof params.pack === "string" ? params.pack : "";
  const mode = modeById(typeof params.mode === "string" ? params.mode : undefined);
  if (!reel) redirect("/akis");
  return <LearnChat reelId={reel} choice={choice} pack={pack} mode={mode?.id ?? DEFAULT_MODE} />;
}
