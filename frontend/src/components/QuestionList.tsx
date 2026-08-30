"use client";

import type { QuestionPublic } from "@/lib/api";

type Props = {
  questions: QuestionPublic[];
  answers: Record<string, string>;
  onChange: (id: string, letter: string) => void;
  compactLanguage?: boolean;
};

export function QuestionList({ questions, answers, onChange, compactLanguage = false }: Props) {
  if (compactLanguage) {
    return (
      <div className="-mx-1 overflow-x-auto px-1 pb-3">
        <ol className="grid min-w-[64rem] grid-cols-5 gap-3 xl:min-w-0">
          {questions.map((q) => (
            <li key={q.id} className="card rise flex min-h-full flex-col p-4">
              <div className="flex items-start justify-between gap-2 border-b border-[var(--line-soft)] pb-3">
                <p className="text-sm font-semibold leading-5 text-[var(--navy)]">
                  <span className="mr-1.5 font-serif text-[var(--gold)]">{q.order}.</span>
                  {q.stem}
                </p>
                <span className="text-[10px] text-[var(--ink-3)]">{q.points}p</span>
              </div>

              <div className="mt-3 grid flex-1 gap-2">
                {Object.keys(q.options).sort().map((letter) => {
                  const on = answers[q.id] === letter;
                  return (
                    <label
                      key={letter}
                      className={`flex cursor-pointer items-center rounded-xl border px-3 py-2.5 text-sm leading-5 transition ${on ? "border-[var(--navy)] bg-[var(--navy)] text-white shadow-sm" : "border-[var(--line)] bg-white text-[var(--ink)] hover:border-[rgba(28,61,90,.45)] hover:bg-[#fffdf8]"}`}
                    >
                      <input
                        type="radio"
                        className="sr-only"
                        name={q.id}
                        checked={on}
                        onChange={() => onChange(q.id, letter)}
                      />
                      <span>{q.options[letter]}</span>
                    </label>
                  );
                })}
              </div>
            </li>
          ))}
        </ol>
      </div>
    );
  }

  return (
    <ol className="space-y-4">
      {questions.map((q) => (
        <li key={q.id} className="card rise p-5">
          <div className="flex items-start justify-between gap-4">
            <p className="font-medium leading-relaxed text-[var(--navy)]">
              <span className="mr-2 font-serif text-[var(--gold)]">{q.order}.</span>
              {q.stem}
            </p>
            <span className="badge flex-none">{q.points} puan</span>
          </div>

          <div className="mt-4 grid gap-2">
            {Object.keys(q.options).sort().map((letter) => {
              const on = answers[q.id] === letter;
              return (
                <label key={letter} className={`choice ${on ? "choice-on" : ""}`}>
                  <input
                    type="radio"
                    className="sr-only"
                    name={q.id}
                    checked={on}
                    onChange={() => onChange(q.id, letter)}
                  />
                  <span className="choice-letter">{letter}</span>
                  <span className="text-sm leading-relaxed">{q.options[letter]}</span>
                </label>
              );
            })}
          </div>
        </li>
      ))}
    </ol>
  );
}
