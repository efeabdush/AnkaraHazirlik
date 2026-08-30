import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { PracticeArchive } from "@/components/PracticeArchive";
import { isPracticeKind, practiceLibrary, type PracticeKind } from "@/lib/practiceLibrary";
import { createPageMetadata } from "@/lib/seo";

export function generateStaticParams() {
  return (Object.keys(practiceLibrary) as PracticeKind[]).map((kind) => ({ kind }));
}

export async function generateMetadata({ params }: { params: Promise<{ kind: string }> }): Promise<Metadata> {
  const { kind } = await params;
  if (!isPracticeKind(kind)) return {};
  const meta = practiceLibrary[kind];
  return createPageMetadata(meta.label, meta.description, `/practice-library/${kind}`);
}

export default async function PracticeLibraryPage({ params }: { params: Promise<{ kind: string }> }) {
  const { kind } = await params;
  if (!isPracticeKind(kind)) notFound();
  return <PracticeArchive kind={kind} />;
}
