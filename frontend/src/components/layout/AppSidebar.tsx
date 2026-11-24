import {
  AudioLines,
  ChartNoAxesColumnIncreasing,
  House,
  LayoutDashboard,
  Settings,
  Sparkles,
} from 'lucide-react';
import type { LucideIcon } from 'lucide-react';
import { NavLink } from 'react-router-dom';

interface NavigationItem {
  label: string;
  to: string;
  icon: LucideIcon;
}

const navigation: NavigationItem[] = [
  { label: 'Home', to: '/', icon: House },
  { label: 'Dashboard', to: '/dashboard', icon: LayoutDashboard },
  { label: 'Practice', to: '/practice', icon: AudioLines },
  { label: 'Sessions', to: '/sessions', icon: Sparkles },
  { label: 'Progress', to: '/progress', icon: ChartNoAxesColumnIncreasing },
  { label: 'Settings', to: '/settings', icon: Settings },
];

interface AppSidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function AppSidebar({ isOpen, onClose }: AppSidebarProps) {
  return (
    <>
      {isOpen && (
        <button
          aria-label="Close navigation menu"
          className="fixed inset-0 z-30 bg-slate-950/40 lg:hidden"
          onClick={onClose}
          type="button"
        />
      )}
      <aside
        aria-label="Main navigation"
        className={`fixed inset-y-0 left-0 z-40 flex w-72 flex-col border-r border-slate-200 bg-white px-5 py-6 transition-transform duration-200 lg:translate-x-0 ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <NavLink
          aria-label="LinguaAi home"
          className="mb-10 flex items-center gap-3 px-2"
          onClick={onClose}
          to="/"
        >
          <span className="bg-brand-600 shadow-brand-600/20 flex size-11 items-center justify-center rounded-2xl text-white shadow-lg">
            <AudioLines aria-hidden="true" size={23} />
          </span>
          <span>
            <span className="block text-lg font-bold tracking-tight text-slate-950">LinguaAi</span>
            <span className="block text-xs text-slate-500">Learn at your pace</span>
          </span>
        </NavLink>

        <p className="mb-3 px-3 text-[11px] font-semibold tracking-[0.14em] text-slate-400 uppercase">
          Workspace
        </p>
        <nav className="space-y-1" aria-label="Workspace">
          {navigation.map(({ label, to, icon: Icon }) => (
            <NavLink
              key={to}
              end={to === '/'}
              onClick={onClose}
              to={to}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition ${
                  isActive
                    ? 'bg-brand-50 text-brand-700'
                    : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                }`
              }
            >
              <Icon aria-hidden="true" size={19} strokeWidth={1.8} />
              {label}
            </NavLink>
          ))}
        </nav>

        <div className="mt-auto rounded-2xl bg-slate-50 p-4">
          <p className="text-sm font-semibold text-slate-800">Keep your streak going</p>
          <p className="mt-1 text-xs leading-5 text-slate-500">
            A little practice every day adds up.
          </p>
          <div className="mt-4 h-1.5 overflow-hidden rounded-full bg-slate-200">
            <div className="bg-brand-500 h-full w-2/3 rounded-full" />
          </div>
        </div>
      </aside>
    </>
  );
}
