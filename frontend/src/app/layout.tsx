import type { Metadata } from "next";
import { Source_Sans_3, Source_Serif_4 } from "next/font/google";
import { Footer, Header } from "@/components/SiteChrome";
import "./globals.css";

const sans = Source_Sans_3({
  variable: "--font-source-sans",
  subsets: ["latin", "latin-ext"],
});

const serif = Source_Serif_4({
  variable: "--font-source-serif",
  subsets: ["latin", "latin-ext"],
});

export const metadata: Metadata = {
  title: "Ankara Hazırlık · Yeterlik sınavı çalışması",
  description:
    "Ankara Üniversitesi İngilizce yeterlik sınavına hazırlık: üç oturumda dinleme, okuma, dil kullanımı, yazma ve konuşma pratiği.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="tr" className={`${sans.variable} ${serif.variable} h-full antialiased`}>
      <body className="flex min-h-full flex-col font-sans">
        <Header />
        <main className="mx-auto w-full max-w-6xl flex-1 px-4 py-8 sm:px-5 sm:py-10">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
