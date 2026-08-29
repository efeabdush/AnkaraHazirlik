import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

function normalizeModelMarkdown(value: string) {
  return value
    .replace(/\*\*[ \t]+([^*\n]+?)[ \t]+\*\*/g, "**$1**")
    .replace(/(^|[^*])\*[ \t]+([^*\n]+?)[ \t]+\*(?!\*)/gm, "$1*$2*")
    .replace(/^\s*•\s+/gm, "- ");
}

export function MarkdownText({ children, className = "" }: { children: string; className?: string }) {
  return (
    <div className={`ai-markdown ${className}`}>
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          a: ({ children: label, href, title }) => <a href={href} title={title} target="_blank" rel="noreferrer">{label}</a>,
        }}
      >
        {normalizeModelMarkdown(children)}
      </ReactMarkdown>
    </div>
  );
}
