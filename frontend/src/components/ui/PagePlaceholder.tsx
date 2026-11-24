import { Sparkles } from 'lucide-react';

interface PagePlaceholderProps {
  title: string;
  description: string;
}

export default function PagePlaceholder({ title, description }: PagePlaceholderProps) {
  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
      <div className="bg-brand-50 text-brand-600 mb-5 flex size-12 items-center justify-center rounded-2xl">
        <Sparkles aria-hidden="true" size={22} />
      </div>
      <p className="text-brand-600 text-xs font-semibold tracking-[0.16em] uppercase">
        Coming soon
      </p>
      <h1 className="mt-2 text-2xl font-bold tracking-tight text-slate-950">{title}</h1>
      <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-600">{description}</p>
    </section>
  );
}
