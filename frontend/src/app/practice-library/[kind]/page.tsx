import { notFound } from "next/navigation";
import { PracticeArchive } from "@/components/PracticeArchive";
import { isPracticeKind } from "@/lib/practiceLibrary";

export default async function PracticeLibraryPage({ params }: { params: Promise<{ kind: string }> }) {
  const { kind } = await params;
  if (!isPracticeKind(kind)) notFound();
  return <PracticeArchive kind={kind} />;
}
