const statusStyles = {
  Yes: {
    ring: 'border-red-200 bg-white',
    label: 'Likely to Churn',
    accent: 'bg-red-600',
    text: 'text-red-700',
  },
  No: {
    ring: 'border-emerald-200 bg-white',
    label: 'Not Likely to Churn',
    accent: 'bg-emerald-600',
    text: 'text-emerald-700',
  },
};

export default function PredictionCard({ prediction, probability, metrics }) {
  if (!prediction) {
    return null;
  }

  const styles = statusStyles[prediction] ?? statusStyles.No;
  const percentage = Math.max(0, Math.min(100, Math.round(probability * 100)));

  const metricItems = metrics
    ? [
        { label: 'Accuracy', value: metrics.accuracy },
        { label: 'Precision', value: metrics.precision },
        { label: 'Recall', value: metrics.recall },
        { label: 'F1 Score', value: metrics.f1 },
        { label: 'ROC-AUC', value: metrics.roc_auc },
      ]
    : [];

  return (
    <section className={`overflow-hidden rounded-xl border bg-white shadow-sm ${styles.ring}`}>
      <div className={`h-1 ${styles.accent}`} />
      <div className="p-6">
        <div className="flex items-start justify-between gap-4">
          <div>
            <p className="text-sm font-medium uppercase tracking-[0.18em] text-slate-500">
              Prediction
            </p>
            <h2 className={`mt-2 text-2xl font-semibold ${styles.text}`}>
              {styles.label}
            </h2>
          </div>

          <span className={`rounded-full px-3 py-1 text-sm font-semibold ${styles.text} bg-white`}>
            {prediction}
          </span>
        </div>

        <div className="mt-6 space-y-3">
          <div className="flex items-center justify-between text-sm">
            <span className="font-medium text-slate-700">Probability</span>
            <span className="font-semibold text-slate-900">{percentage}%</span>
          </div>
          <div className="h-2 w-full rounded-full bg-slate-100">
            <div
              className={`h-2 rounded-full ${styles.accent}`}
              style={{ width: `${percentage}%` }}
            />
          </div>
        </div>

        {metricItems.length ? (
          <div className="mt-6 border-t border-slate-200 pt-6">
            <div className="mb-4 flex items-center justify-between gap-3">
              <h3 className="text-sm font-semibold uppercase tracking-[0.18em] text-slate-500">
                Model Metrics
              </h3>
              <p className="text-xs text-slate-500">
                Validation scores from the trained pipeline
              </p>
            </div>

            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-5">
              {metricItems.map((metric) => (
                <div key={metric.label} className="rounded-xl border border-slate-200 bg-slate-50 px-4 py-3">
                  <p className="text-xs font-medium uppercase tracking-[0.16em] text-slate-500">
                    {metric.label}
                  </p>
                  <p className="mt-2 text-lg font-semibold text-slate-900">
                    {(metric.value * 100).toFixed(1)}%
                  </p>
                </div>
              ))}
            </div>
          </div>
        ) : null}
        </div>
    </section>
  );
}