import { notFound } from "next/navigation";
import { PackList } from "@/components/PackList";
import { levelFromSlug } from "@/lib/levels";
import { modeById } from "@/lib/modes";

export default async function ModePacksPage({ params }: PageProps<"/akis/[mode]/seviye/[slug]">) {
  const { mode, slug } = await params;
  const found = modeById(mode);
  const level = levelFromSlug(slug);
  if (!found || !level) notFound();
  return <PackList mode={found.id} level={level} />;
}
