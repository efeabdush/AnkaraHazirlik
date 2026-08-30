import type { ReactNode } from "react";

/**
 * Small Markdown renderer for model output.
 *
 * Models answer with **bold**, bullet lists and the occasional `code`, and a
 * chat bubble that prints those raw looks broken. This covers what actually
 * shows up in short tutoring replies and nothing more.
 *
 * It builds React elements — never HTML strings — so model text can't inject
 * markup no matter what it contains.
 */

const HEADING = /^\s{0,3}(#{1,6})\s+(.*)$/;
const QUOTE = /^\s{0,3}>\s?(.*)$/;
const BULLET = /^\s{0,3}([-*+])\s+(.*)$/;
const NUMBERED = /^\s{0,3}(\d{1,3})[.)]\s+(.*)$/;
const RULE = /^\s{0,3}([-*_])\s*\1\s*\1[\s\-*_]*$/;
const FENCE = /^\s{0,3}(`{3,}|~{3,})(.*)$/;

// Two rules keep this honest on real model output:
// 1. A delimiter only opens emphasis when it is glued to the text, so
//    "3 * 4 = 12" keeps its asterisks and an unclosed "**bold" stays literal.
// 2. A span may not contain its own delimiter, so "**C** ... **big one**" stays
//    two spans instead of collapsing into one and leaking stray asterisks.
const INLINE_SRC =
  "`([^`\\n]+)`" + // code
  "|\\*\\*\\*([^\\s*][^*\\n]*[^\\s*]|[^\\s*])\\*\\*\\*" + // bold + italic
  "|\\*\\*([^\\s*][^*\\n]*[^\\s*]|[^\\s*])\\*\\*" + // bold
  "|__([^\\s_][^_\\n]*[^\\s_]|[^\\s_])__" + // bold
  "|~~([^\\s~][^~\\n]*[^\\s~]|[^\\s~])~~" + // strikethrough
  "|\\*([^\\s*][^*\\n]*[^\\s*]|[^\\s*])\\*" + // italic
  "|_([^\\s_][^_\\n]*[^\\s_]|[^\\s_])_" + // italic
  "|\\[([^\\]\\n]+)\\]\\(([^)\\s]+)\\)"; // link

const WORDY = /[A-Za-z0-9ğüşıöçĞÜŞİÖÇ]/;

function inline(text: string, depth = 0): ReactNode[] {
  if (depth > 3) return [text];
  // a fresh regex per call: recursion must not share lastIndex
  const re = new RegExp(INLINE_SRC, "g");
  const out: ReactNode[] = [];
  let last = 0;
  let n = 0;
  let m: RegExpExecArray | null;

  while ((m = re.exec(text)) !== null) {
    if (m.index > last) out.push(text.slice(last, m.index));
    const key = `${depth}-${n++}`;

    if (m[1] !== undefined) {
      out.push(<code key={key}>{m[1]}</code>);
    } else if (m[2] !== undefined) {
      out.push(
        <strong key={key}>
          <em>{inline(m[2], depth + 1)}</em>
        </strong>,
      );
    } else if (m[3] !== undefined) {
      out.push(<strong key={key}>{inline(m[3], depth + 1)}</strong>);
    } else if (m[4] !== undefined) {
      out.push(<strong key={key}>{inline(m[4], depth + 1)}</strong>);
    } else if (m[5] !== undefined) {
      out.push(<s key={key}>{inline(m[5], depth + 1)}</s>);
    } else if (m[6] !== undefined) {
      out.push(<em key={key}>{inline(m[6], depth + 1)}</em>);
    } else if (m[7] !== undefined) {
      // an underscore inside a word (snake_case) is not emphasis
      const before = text[m.index - 1] ?? " ";
      const after = text[m.index + m[0].length] ?? " ";
      if (WORDY.test(before) || WORDY.test(after)) out.push(m[0]);
      else out.push(<em key={key}>{inline(m[7], depth + 1)}</em>);
    } else if (m[8] !== undefined && m[9] !== undefined) {
      const href = m[9];
      out.push(
        /^https?:\/\//i.test(href) ? (
          <a key={key} href={href} target="_blank" rel="noreferrer noopener">
            {inline(m[8], depth + 1)}
          </a>
        ) : (
          <span key={key}>{inline(m[8], depth + 1)}</span>
        ),
      );
    }
    last = m.index + m[0].length;
  }

  if (last < text.length) out.push(text.slice(last));
  return out.length ? out : [text];
}

function paragraph(lines: string[], key: string): ReactNode {
  return (
    <p key={key}>
      {lines.map((line, i) => (
        <span key={i}>
          {i > 0 ? <br /> : null}
          {inline(line)}
        </span>
      ))}
    </p>
  );
}

function blocks(source: string): ReactNode[] {
  const lines = source.replace(/\r\n?/g, "\n").split("\n");
  const out: ReactNode[] = [];
  let i = 0;
  let key = 0;

  while (i < lines.length) {
    const line = lines[i];

    if (!line.trim()) {
      i += 1;
      continue;
    }

    const fence = FENCE.exec(line);
    if (fence) {
      const marker = fence[1][0];
      const body: string[] = [];
      i += 1;
      while (i < lines.length && !new RegExp(`^\\s{0,3}${marker}{3,}\\s*$`).test(lines[i])) {
        body.push(lines[i]);
        i += 1;
      }
      i += 1; // closing fence
      out.push(
        <pre key={`b${key++}`}>
          <code>{body.join("\n")}</code>
        </pre>,
      );
      continue;
    }

    if (RULE.test(line)) {
      out.push(<hr key={`b${key++}`} />);
      i += 1;
      continue;
    }

    const heading = HEADING.exec(line);
    if (heading) {
      out.push(
        <p key={`b${key++}`} className="md-h">
          {inline(heading[2])}
        </p>,
      );
      i += 1;
      continue;
    }

    if (QUOTE.test(line)) {
      const body: string[] = [];
      while (i < lines.length && QUOTE.test(lines[i])) {
        body.push((QUOTE.exec(lines[i]) as RegExpExecArray)[1]);
        i += 1;
      }
      out.push(<blockquote key={`b${key++}`}>{paragraph(body, "q")}</blockquote>);
      continue;
    }

    if (BULLET.test(line) || NUMBERED.test(line)) {
      const numbered = !BULLET.test(line) && NUMBERED.test(line);
      const items: string[] = [];
      while (i < lines.length) {
        const match = numbered ? NUMBERED.exec(lines[i]) : BULLET.exec(lines[i]);
        if (!match) break;
        items.push(match[2]);
        i += 1;
        // a wrapped continuation line belongs to the item above
        while (i < lines.length && lines[i].trim() && !isBlockStart(lines[i])) {
          items[items.length - 1] += ` ${lines[i].trim()}`;
          i += 1;
        }
      }
      const children = items.map((item, at) => <li key={at}>{inline(item)}</li>);
      out.push(
        numbered ? <ol key={`b${key++}`}>{children}</ol> : <ul key={`b${key++}`}>{children}</ul>,
      );
      continue;
    }

    const body: string[] = [];
    while (i < lines.length && lines[i].trim() && !isBlockStart(lines[i])) {
      body.push(lines[i].trim());
      i += 1;
    }
    out.push(paragraph(body, `b${key++}`));
  }

  return out;
}

function isBlockStart(line: string): boolean {
  return (
    HEADING.test(line) ||
    QUOTE.test(line) ||
    BULLET.test(line) ||
    NUMBERED.test(line) ||
    RULE.test(line) ||
    FENCE.test(line)
  );
}

export function Markdown({ text, className }: { text: string; className?: string }) {
  return <div className={className ? `md ${className}` : "md"}>{blocks(text)}</div>;
}
