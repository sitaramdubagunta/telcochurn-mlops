import { useEffect, useMemo, useState } from 'react';

import Header from '../components/Header';
import Footer from '../components/Footer';
import CustomerForm from '../components/CustomerForm';
import PredictionCard from '../components/PredictionCard';
import { getMetadata, getSamplePayload, predictChurn } from '../services/api';
// eslint-disable-next-line react-hooks/set-state-in-effect
useEffect(() => {
  loadDashboardData();
}, []);
function formatPercent(value) {
  return typeof value === 'number' ? `${(value * 100).toFixed(1)}%` : 'Unavailable';
}

function formatDate(value) {
  if (!value) {
    return 'Unavailable';
  }

  return new Intl.DateTimeFormat(undefined, {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(new Date(value));
}

function StatCard({ label, value }) {
  return (
    <div className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
      <p className="text-xs font-semibold uppercase tracking-[0.14em] text-slate-500">{label}</p>
      <p className="mt-2 text-2xl font-semibold text-slate-950">{value}</p>
    </div>
  );
}

function SkeletonStats() {
  return (
    <div className="grid gap-4 md:grid-cols-3 xl:grid-cols-6">
      {Array.from({ length: 6 }).map((_, index) => (
        <div key={index} className="h-24 animate-pulse rounded-lg border border-slate-200 bg-slate-100" />
      ))}
    </div>
  );
}

function ErrorBanner({ message, onRetry }) {
  return (
    <div className="flex flex-col gap-3 rounded-lg border border-red-200 bg-red-50 p-4 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <p className="text-sm font-semibold text-red-900">Backend unavailable</p>
        <p className="mt-1 text-sm text-red-700">{message}</p>
      </div>
      <button
        type="button"
        onClick={onRetry}
        className="w-fit rounded-md border border-red-300 bg-white px-3 py-2 text-sm font-semibold text-red-700 transition hover:bg-red-100"
      >
        Retry
      </button>
    </div>
  );
}

function ModelInfo({ model }) {
  const rows = [
    ['Algorithm', model?.algorithm],
    ['Version', model?.version],
    ['Training Date', formatDate(model?.training_timestamp)],
    ['Feature Count', model?.feature_count ?? 'Unavailable'],
  ];

  return (
    <section className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
      <h2 className="text-base font-semibold text-slate-950">Model Information</h2>
      <div className="mt-5 grid gap-4 sm:grid-cols-2">
        {rows.map(([label, value]) => (
          <div key={label}>
            <p className="text-xs font-semibold uppercase tracking-[0.14em] text-slate-500">{label}</p>
            <p className="mt-1 text-sm font-medium text-slate-900">{value}</p>
          </div>
        ))}
      </div>
    </section>
  );
}

function PredictionHistory({ history, onClear }) {
  return (
    <section className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex items-center justify-between gap-4">
        <h2 className="text-base font-semibold text-slate-950">Session Prediction History</h2>
        <button
          type="button"
          onClick={onClear}
          disabled={!history.length}
          className="rounded-md border border-slate-300 px-3 py-2 text-sm font-semibold text-slate-700 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-50"
        >
          Clear
        </button>
      </div>

      {history.length ? (
        <div className="mt-5 overflow-x-auto">
          <table className="w-full min-w-[560px] text-left text-sm">
            <thead className="border-b border-slate-200 text-xs uppercase tracking-[0.14em] text-slate-500">
              <tr>
                <th className="py-3 font-semibold">Prediction</th>
                <th className="py-3 font-semibold">Probability</th>
                <th className="py-3 font-semibold">Risk</th>
                <th className="py-3 font-semibold">Timestamp</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {history.map((item) => (
                <tr key={item.id}>
                  <td className="py-3 font-medium text-slate-950">{item.prediction === 'Yes' ? 'Churn' : 'Retain'}</td>
                  <td className="py-3 text-slate-700">{Math.round(item.probability * 100)}%</td>
                  <td className="py-3 text-slate-700">{item.risk_level}</td>
                  <td className="py-3 text-slate-700">{formatDate(item.timestamp)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p className="mt-5 rounded-md border border-dashed border-slate-300 bg-slate-50 p-4 text-sm text-slate-600">
          Predictions made during this browser session will appear here.
        </p>
      )}
    </section>
  );
}

export default function Home() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [metadata, setMetadata] = useState(null);
  const [samplePayload, setSamplePayload] = useState(null);
  const [metadataLoading, setMetadataLoading] = useState(true);
  const [error, setError] = useState(null);
  const [history, setHistory] = useState([]);

  const loadDashboardData = async () => {
    setMetadataLoading(true);
    setError(null);

    try {
      const [metadataResponse, sampleResponse] = await Promise.all([
        getMetadata(),
        getSamplePayload(),
      ]);
      setMetadata(metadataResponse);
      setSamplePayload(sampleResponse);
    } catch (requestError) {
      setError(requestError?.message || 'Unable to reach the prediction API.');
      setMetadata(null);
    } finally {
      setMetadataLoading(false);
    }
  };

  useEffect(() => {
    loadDashboardData();
  }, []);

  const stats = useMemo(() => {
    const metrics = metadata?.metrics || {};
    const model = metadata?.model_info || {};

    return [
      ['Accuracy', formatPercent(metrics.accuracy)],
      ['Precision', formatPercent(metrics.precision)],
      ['Recall', formatPercent(metrics.recall)],
      ['ROC AUC', formatPercent(metrics.roc_auc)],
      ['Model Version', model.version || 'local'],
      ['Last Training', formatDate(model.training_timestamp)],
    ];
  }, [metadata]);

  const handleSubmit = async (values) => {
    setLoading(true);
    setError(null);

    try {
      const response = await predictChurn({
        ...values,
        SeniorCitizen: Number(values.SeniorCitizen),
      });

      setResult(response);
      setHistory((items) => [
        {
          id: crypto.randomUUID(),
          timestamp: new Date().toISOString(),
          ...response,
        },
        ...items,
      ]);
    } catch (requestError) {
      setError(requestError?.response?.data?.detail || requestError?.message || 'Prediction request failed.');
    } finally {
      setLoading(false);
    }
  };

  const backendUnavailable = Boolean(error && !metadata);

  return (
    <main className="min-h-screen px-4 py-8 text-slate-900 sm:px-6 lg:px-8">
      <div className="mx-auto flex w-full max-w-7xl flex-col gap-6">
        <Header metadata={metadata} />

        {error ? <ErrorBanner message={error} onRetry={loadDashboardData} /> : null}

        {metadataLoading ? (
          <SkeletonStats />
        ) : (
          <section className="grid gap-4 md:grid-cols-3 xl:grid-cols-6">
            {stats.map(([label, value]) => (
              <StatCard key={label} label={label} value={value} />
            ))}
          </section>
        )}

        <section className="grid gap-6 xl:grid-cols-[minmax(0,1.35fr)_minmax(360px,0.65fr)]">
          <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
            <div className="mb-6">
              <h2 className="text-base font-semibold text-slate-950">Customer Prediction</h2>
              <p className="mt-2 text-sm leading-6 text-slate-600">
                Enter customer, service, and billing details to generate a live churn-risk score.
              </p>
            </div>

            <CustomerForm
              onSubmit={handleSubmit}
              loading={loading}
              disabled={backendUnavailable}
              samplePayload={samplePayload}
            />
          </div>

          <div className="flex flex-col gap-6">
            <PredictionCard result={result} />
            <ModelInfo model={metadata?.model_info} />
          </div>
        </section>

        <PredictionHistory history={history} onClear={() => setHistory([])} />

        <Footer />
      </div>
    </main>
  );
}
