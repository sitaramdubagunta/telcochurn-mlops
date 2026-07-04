function StatusBadge({ label, tone = 'neutral' }) {
  const tones = {
    healthy: 'border-emerald-200 bg-emerald-50 text-emerald-700',
    degraded: 'border-amber-200 bg-amber-50 text-amber-700',
    neutral: 'border-slate-200 bg-white text-slate-700',
  };

  return (
    <span className={`inline-flex items-center rounded-full border px-3 py-1 text-xs font-semibold ${tones[tone]}`}>
      {label}
    </span>
  );
}

export default function Header({ metadata }) {
  const health = metadata?.health;
  const model = metadata?.model_info;
  const isHealthy = health?.status === 'healthy';

  return (
    <header className="flex flex-col gap-5 border-b border-slate-200 pb-6 lg:flex-row lg:items-end lg:justify-between">
      <div>
        <p className="text-sm font-semibold uppercase tracking-[0.18em] text-blue-700">
          Production MLOps Pipeline
        </p>
        <h1 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950 sm:text-4xl">
          Telecom Churn Operations
        </h1>
        <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-600 sm:text-base">
          Score customer churn risk, inspect model health, and review prediction activity from one operational dashboard.
        </p>
      </div>

      <div className="flex flex-wrap gap-2">
        <StatusBadge
          label={isHealthy ? 'API Healthy' : 'API Degraded'}
          tone={isHealthy ? 'healthy' : 'degraded'}
        />
        <StatusBadge label={`Model ${model?.version ?? 'local'}`} />
      </div>
    </header>
  );
}
