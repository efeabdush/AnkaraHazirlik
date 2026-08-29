"use client";

import type { QuestionPublic } from "@/lib/api";

type Props = {
  questions: QuestionPublic[];
  answers: Record<string, string>;
  onChange: (id: string, letter: string) => void;
};

export function QuestionList({ questions, answers, onChange }: Props) {
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
