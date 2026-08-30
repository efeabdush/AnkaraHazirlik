import type { Metadata } from "next";

export const SITE_NAME = "Ankara Hazırlık";
export const SITE_URL = "https://ankarahazirlik.com";
export const SITE_DESCRIPTION =
  "Ankara Üniversitesi İngilizce hazırlık muafiyet ve yeterlik sınavı için ücretsiz B1+ dinleme, okuma, dil kullanımı, writing ve speaking pratiği.";

export function createPageMetadata(title: string, description: string, path: string): Metadata {
  const url = new URL(path, SITE_URL).toString();
  const fullTitle = `${title} | ${SITE_NAME}`;

  return {
    title,
    description,
    alternates: { canonical: url },
    openGraph: {
      type: "website",
      locale: "tr_TR",
      url,
      siteName: SITE_NAME,
      title: fullTitle,
      description,
    },
    twitter: {
      card: "summary",
      title: fullTitle,
      description,
    },
  };
}

export const websiteStructuredData = {
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebSite",
      "@id": `${SITE_URL}/#website`,
      url: SITE_URL,
      name: SITE_NAME,
      alternateName: ["AnkaraHazirlik.com", "Ankara Hazırlık Muafiyet"],
      description: SITE_DESCRIPTION,
      inLanguage: "tr-TR",
    },
    {
      "@type": "WebApplication",
      "@id": `${SITE_URL}/#application`,
      url: SITE_URL,
      name: SITE_NAME,
      description: SITE_DESCRIPTION,
      applicationCategory: "EducationalApplication",
      operatingSystem: "Any",
      browserRequirements: "JavaScript etkin modern bir web tarayıcısı",
      isAccessibleForFree: true,
      inLanguage: ["tr-TR", "en"],
      educationalUse: ["practice", "assessment"],
      audience: {
        "@type": "EducationalAudience",
        educationalRole: "student",
      },
      offers: {
        "@type": "Offer",
        price: "0",
        priceCurrency: "TRY",
      },
      about: {
        "@type": "Thing",
        name: "Ankara Üniversitesi İngilizce hazırlık muafiyet ve yeterlik sınavı",
      },
    },
  ],
};
