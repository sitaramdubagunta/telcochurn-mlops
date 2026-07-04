const riskStyles = {
  High: 'border-red-200 bg-red-50 text-red-700',
  Medium: 'border-amber-200 bg-amber-50 text-amber-700',
  Low: 'border-emerald-200 bg-emerald-50 text-emerald-700',
};

export default function PredictionCard({ result }) {
  if (!result) {
    return (
      <section className="rounded-lg border border-dashed border-slate-300 bg-white p-6">
        <p className="text-sm font-semibold text-slate-950">No prediction yet</p>
        <p className="mt-2 text-sm leading-6 text-slate-600">
          Submit a customer profile to see churn probability, risk tier, confidence, and a retention recommendation.
        </p>
      </section>
    );
  }

  const probability = Math.round(result.probability * 100);
  const confidence = Math.round(result.confidence * 100);
  const riskClass = riskStyles[result.risk_level] || riskStyles.Low;

  return (
    <section className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.16em] text-slate-500">
            Prediction Result
          </p>
          <div className="mt-3 flex items-end gap-3">
            <span className="text-5xl font-semibold tracking-tight text-slate-950">
              {probability}%
            </span>
            <span className="pb-2 text-sm font-medium text-slate-500">churn probability</span>
          </div>
        </div>

        <span className={`inline-flex w-fit rounded-full border px-3 py-1 text-sm font-semibold ${riskClass}`}>
          {result.risk_level} Risk
        </span>
      </div>

      <div className="mt-6 h-2 rounded-full bg-slate-100">
        <div
          className="h-2 rounded-full bg-blue-600 transition-all"
          style={{ width: `${probability}%` }}
        />
      </div>

      <div className="mt-6 grid gap-3 sm:grid-cols-3">
        <div className="rounded-md border border-slate-200 bg-slate-50 p-4">
          <p className="text-xs font-semibold uppercase tracking-[0.14em] text-slate-500">Prediction</p>
          <p className="mt-2 text-lg font-semibold text-slate-950">{result.prediction === 'Yes' ? 'Churn' : 'Retain'}</p>
        </div>
        <div className="rounded-md border border-slate-200 bg-slate-50 p-4">
          <p className="text-xs font-semibold uppercase tracking-[0.14em] text-slate-500">Confidence</p>
          <p className="mt-2 text-lg font-semibold text-slate-950">{confidence}%</p>
        </div>
        <div className="rounded-md border border-slate-200 bg-slate-50 p-4">
          <p className="text-xs font-semibold uppercase tracking-[0.14em] text-slate-500">Risk Level</p>
          <p className="mt-2 text-lg font-semibold text-slate-950">{result.risk_level}</p>
        </div>
      </div>

      <div className="mt-5 rounded-md border border-blue-100 bg-blue-50 p-4">
        <p className="text-sm font-semibold text-blue-950">Recommended action</p>
        <p className="mt-1 text-sm leading-6 text-blue-900">{result.recommendation}</p>
      </div>
    </section>
  );
}
