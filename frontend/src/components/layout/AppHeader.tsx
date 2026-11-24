import { Bell, Menu, Search } from 'lucide-react';
import { useLocation } from 'react-router-dom';

const pageTitles: Record<string, string> = {
  '/': 'Home',
  '/login': 'Sign in',
  '/register': 'Create account',
  '/dashboard': 'Dashboard',
  '/practice': 'Practice',
  '/sessions': 'Sessions',
  '/progress': 'Your progress',
  '/settings': 'Settings',
};

interface AppHeaderProps {
  onMenuClick: () => void;
}

export default function AppHeader({ onMenuClick }: AppHeaderProps) {
  const { pathname } = useLocation();
  const title = pageTitles[pathname] ?? 'Page not found';

  return (
    <header className="sticky top-0 z-20 flex h-16 items-center justify-between border-b border-slate-200/80 bg-white/90 px-4 backdrop-blur sm:px-6 lg:px-10">
      <div className="flex items-center gap-3">
        <button
          aria-label="Open navigation menu"
          className="inline-flex size-10 items-center justify-center rounded-xl text-slate-600 transition hover:bg-slate-100 lg:hidden"
          onClick={onMenuClick}
          type="button"
        >
          <Menu aria-hidden="true" size={20} />
        </button>
        <div>
          <p className="text-sm font-semibold text-slate-900">{title}</p>
          <p className="hidden text-xs text-slate-500 sm:block">Your personal language workspace</p>
        </div>
      </div>

      <div className="flex items-center gap-2 sm:gap-3">
        <button
          aria-label="Search (coming soon)"
          className="inline-flex size-10 items-center justify-center rounded-xl text-slate-500 transition hover:bg-slate-100 hover:text-slate-800"
          type="button"
        >
          <Search aria-hidden="true" size={19} />
        </button>
        <button
          aria-label="Notifications (coming soon)"
          className="relative inline-flex size-10 items-center justify-center rounded-xl text-slate-500 transition hover:bg-slate-100 hover:text-slate-800"
          type="button"
        >
          <Bell aria-hidden="true" size={19} />
        </button>
        <div
          aria-label="Demo profile"
          className="bg-brand-100 text-brand-700 ml-1 flex size-9 items-center justify-center rounded-full text-xs font-bold"
          role="img"
        >
          LA
        </div>
      </div>
    </header>
  );
}
