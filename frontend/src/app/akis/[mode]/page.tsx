import { notFound } from "next/navigation";
import { ReelFeed } from "@/components/ReelFeed";
import { modeById } from "@/lib/modes";

export default async function ModeFeedPage({ params, searchParams }: PageProps<"/akis/[mode]">) {
  const { mode } = await params;
  const found = modeById(mode);
  if (!found) notFound();

  const query = await searchParams;
  const pack = typeof query.pack === "string" ? query.pack : undefined;
  // Set when coming back from the chat: the card to open on.
  const card = typeof query.card === "string" ? query.card : undefined;
  // The key matters: moving between packs stays on this route, and without a
  // remount the feed would keep the previous pack's scroll position and land
  // the learner on the end card instead of question one.
  return <ReelFeed key={`${found.id}:${pack ?? "mix"}`} kind={found.id} pack={pack} focusCard={card} />;
}
