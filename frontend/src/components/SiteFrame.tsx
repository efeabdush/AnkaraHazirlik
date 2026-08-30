"use client";

import { usePathname } from "next/navigation";
import { Footer, Header } from "@/components/SiteChrome";

const immersive = /^\/akis\/(sorular|kelime|bosluk)(?:\?.*)?$|^\/akis\/ogren(?:\/|$)/;

export function SiteFrame({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  if (immersive.test(pathname)) {
    return <main className="min-h-dvh w-full flex-1">{children}</main>;
  }
  return (
    <>
      <Header />
      <main className="mx-auto w-full max-w-6xl flex-1 px-4 py-8 sm:px-5 sm:py-10">{children}</main>
      <Footer />
    </>
  );
}
