import { ArrowLeft } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function NotFoundPage() {
  return (
    <section className="flex min-h-[55vh] flex-col items-center justify-center text-center">
      <p className="text-brand-600 text-sm font-bold tracking-[0.2em] uppercase">404 error</p>
      <h1 className="mt-3 text-4xl font-bold tracking-tight text-slate-950">Page not found</h1>
      <p className="mt-3 max-w-md text-sm leading-6 text-slate-600">
        This page may have moved, or the address might be mistyped.
      </p>
      <Link
        className="bg-brand-600 hover:bg-brand-700 mt-6 inline-flex items-center gap-2 rounded-xl px-4 py-2.5 text-sm font-semibold text-white transition"
        to="/"
      >
        <ArrowLeft aria-hidden="true" size={16} />
        Back to home
      </Link>
    </section>
  );
}
