type BrandMarkProps = {
  className?: string;
};

/**
 * Ankara'nın tarihî güneş kurslarından esinlenen özgün rozet.
 * Herhangi bir kurum armasının kopyası değildir.
 */
export function BrandMark({ className }: BrandMarkProps) {
  return (
    <svg viewBox="0 0 64 64" className={className} aria-hidden="true">
      <g fill="none" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round">
        <path
          d="M32 3.5v8M32 52.5v8M3.5 32h8M52.5 32h8M11.85 11.85l5.65 5.65M46.5 46.5l5.65 5.65M52.15 11.85L46.5 17.5M17.5 46.5l-5.65 5.65"
          strokeWidth="3.2"
        />
        <path
          d="M21.7 7.2l2.1 6.4M40.2 50.4l2.1 6.4M7.2 42.3l6.4-2.1M50.4 23.8l6.4-2.1M7.2 21.7l6.4 2.1M50.4 40.2l6.4 2.1M21.7 56.8l2.1-6.4M40.2 13.6l2.1-6.4"
          strokeWidth="2.4"
        />
        <circle cx="32" cy="32" r="15.5" strokeWidth="2.8" />
        <path d="M22.5 34.5c2.9 6.4 9.7 9.2 15.4 5.8 4.2-2.5 5.9-7.5 4.3-12.1" strokeWidth="2.5" />
        <path d="M20.5 28.8c3-6.1 9.9-8.7 15.5-5.2 2.2 1.4 3.9 3.5 4.8 5.9" strokeWidth="2.5" />
      </g>
      <circle cx="32" cy="32" r="5.2" fill="currentColor" />
      <circle cx="32" cy="32" r="1.9" fill="var(--navy, #1c3d5a)" />
    </svg>
  );
}
