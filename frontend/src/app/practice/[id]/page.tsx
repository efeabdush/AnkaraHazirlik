import { AcademicPracticeSession } from "@/components/AcademicPracticeSession";

export default async function PracticePage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return <AcademicPracticeSession testId={id} />;
}
