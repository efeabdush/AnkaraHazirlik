import { notFound } from "next/navigation";
import { LevelPicker } from "@/components/LevelPicker";
import { modeById } from "@/lib/modes";

export default async function ModeLevelsPage({ params }: PageProps<"/akis/[mode]/seviye">) {
  const { mode } = await params;
  const found = modeById(mode);
  if (!found) notFound();
  return <LevelPicker mode={found.id} />;
}
