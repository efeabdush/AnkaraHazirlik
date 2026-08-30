import type { MetadataRoute } from "next";
import { practiceLibrary, type PracticeKind } from "@/lib/practiceLibrary";
import { SITE_URL } from "@/lib/seo";

const corePages = [
  { path: "", priority: 1, changeFrequency: "weekly" as const },
  { path: "/exam", priority: 0.9, changeFrequency: "weekly" as const },
  { path: "/listening", priority: 0.9, changeFrequency: "weekly" as const },
  { path: "/reading", priority: 0.9, changeFrequency: "weekly" as const },
  { path: "/use-of-english", priority: 0.9, changeFrequency: "weekly" as const },
  { path: "/writing", priority: 0.8, changeFrequency: "weekly" as const },
  { path: "/speaking", priority: 0.8, changeFrequency: "weekly" as const },
  { path: "/resources", priority: 0.7, changeFrequency: "monthly" as const },
  { path: "/about", priority: 0.5, changeFrequency: "monthly" as const },
];

export default function sitemap(): MetadataRoute.Sitemap {
  const archivePages = (Object.keys(practiceLibrary) as PracticeKind[]).map((kind) => ({
    url: `${SITE_URL}/practice-library/${kind}`,
    changeFrequency: "weekly" as const,
    priority: 0.7,
  }));

  return [
    ...corePages.map((page) => ({
      url: `${SITE_URL}${page.path}`,
      changeFrequency: page.changeFrequency,
      priority: page.priority,
    })),
    ...archivePages,
  ];
}
