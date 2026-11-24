import { ArrowRight, AudioLines, ChartNoAxesColumnIncreasing, Clock3 } from 'lucide-react';
import { Link } from 'react-router-dom';

const highlights = [
  {
    icon: AudioLines,
    title: 'Practice with purpose',
    description: 'Build a steady routine with focused language practice.',
    to: '/practice',
  },
  {
    icon: Clock3,
    title: 'Pick up where you left off',
    description: 'Your learning sessions will be easy to find in one place.',
    to: '/sessions',
  },
  {
    icon: ChartNoAxesColumnIncreasing,
    title: 'See your progress',
    description: 'A clear view of your learning journey is on the way.',
    to: '/progress',
  },
];

export default function HomePage() {
  return (
    <div className="space-y-8">
      <section className="relative overflow-hidden rounded-3xl bg-slate-950 px-6 py-10 text-white sm:px-10 sm:py-14">
        <div className="bg-brand-500/30 absolute -top-20 -right-10 size-72 rounded-full blur-3xl" />
        <div className="relative max-w-2xl">
          <p className="text-brand-200 text-sm font-semibold">A new way to find your words</p>
          <h1 className="mt-4 text-3xl font-bold tracking-tight sm:text-5xl">
            Make language learning part of your day.
          </h1>
          <p className="mt-4 max-w-xl text-sm leading-6 text-slate-300 sm:text-base">
            LinguaAi is your home for focused practice, learning sessions, and steady progress. Your
            personal learning tools are taking shape.
          </p>
          <Link
            className="hover:bg-brand-50 mt-7 inline-flex items-center gap-2 rounded-xl bg-white px-4 py-2.5 text-sm font-semibold text-slate-950 transition"
            to="/dashboard"
          >
            Explore your dashboard
            <ArrowRight aria-hidden="true" size={17} />
          </Link>
        </div>
      </section>

      <section>
        <div className="mb-4">
          <h2 className="text-lg font-bold text-slate-950">Your learning space</h2>
          <p className="mt-1 text-sm text-slate-500">Everything you need, coming together.</p>
        </div>
        <div className="grid gap-4 md:grid-cols-3">
          {highlights.map(({ icon: Icon, title, description, to }) => (
            <Link
              className="group hover:border-brand-200 rounded-2xl border border-slate-200 bg-white p-5 transition hover:-translate-y-0.5 hover:shadow-md"
              key={title}
              to={to}
            >
              <span className="bg-brand-50 text-brand-600 flex size-10 items-center justify-center rounded-xl">
                <Icon aria-hidden="true" size={20} />
              </span>
              <h3 className="mt-4 font-semibold text-slate-900">{title}</h3>
              <p className="mt-1 text-sm leading-6 text-slate-500">{description}</p>
              <span className="text-brand-700 mt-4 inline-flex items-center gap-1 text-sm font-semibold">
                Explore <ArrowRight aria-hidden="true" size={15} />
              </span>
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
}
