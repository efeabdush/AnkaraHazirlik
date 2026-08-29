import { ListeningSession } from "@/components/ListeningSession";

export default async function Page({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return <ListeningSession testId={id} kind="conversation" />;
}
