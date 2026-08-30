import type { Metadata } from "next";
import { Source_Sans_3, Source_Serif_4 } from "next/font/google";
import { Footer, Header } from "@/components/SiteChrome";
import { HumanVerification } from "@/components/HumanVerification";
import { SITE_DESCRIPTION, SITE_NAME, SITE_URL, websiteStructuredData } from "@/lib/seo";
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
  metadataBase: new URL(SITE_URL),
  applicationName: SITE_NAME,
  title: {
    default: "Ankara Üniversitesi Hazırlık Muafiyet Sınavı | Ankara Hazırlık",
    template: `%s | ${SITE_NAME}`,
  },
  description: SITE_DESCRIPTION,
  category: "education",
  robots: {
    index: true,
    follow: true,
    googleBot: { index: true, follow: true, "max-image-preview": "large", "max-snippet": -1 },
  },
  openGraph: {
    type: "website",
    locale: "tr_TR",
    url: SITE_URL,
    siteName: SITE_NAME,
    title: "Ankara Üniversitesi Hazırlık Muafiyet Sınavı | Ankara Hazırlık",
    description: SITE_DESCRIPTION,
  },
  twitter: {
    card: "summary",
    title: "Ankara Üniversitesi Hazırlık Muafiyet Sınavı | Ankara Hazırlık",
    description: SITE_DESCRIPTION,
  },
  icons: {
    icon: "/brand-mark.svg",
    shortcut: "/brand-mark.svg",
    apple: "/brand-mark.svg",
  },
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="tr" className={`${sans.variable} ${serif.variable} h-full antialiased`}>
      <body className="flex min-h-full flex-col font-sans">
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(websiteStructuredData).replace(/</g, "\\u003c") }}
        />
        <HumanVerification />
        <Header />
        <main className="mx-auto w-full max-w-6xl flex-1 px-4 py-8 sm:px-5 sm:py-10">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
