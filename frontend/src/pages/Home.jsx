import { useState } from 'react';

import Header from '../components/Header';
import Footer from '../components/Footer';
import CustomerForm from '../components/CustomerForm';
import PredictionCard from '../components/PredictionCard';
import { predictChurn } from '../services/api';

export default function Home() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (values) => {
    setLoading(true);

    try {
      const response = await predictChurn({
        ...values,
        SeniorCitizen: Number(values.SeniorCitizen),
      });

      setResult(response);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen px-4 py-10 text-slate-900 sm:px-6 lg:px-8">
      <div className="mx-auto flex w-full max-w-5xl flex-col gap-8">
        <Header />

        <section className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
          <div className="h-1 bg-blue-600" />
          <div className="p-6 sm:p-8">
          <div className="mb-6">
            <p className="text-sm font-semibold uppercase tracking-[0.18em] text-slate-500">
              Customer Information
            </p>
            <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-600">
              Submit customer attributes to generate a churn risk prediction.
            </p>
          </div>

          <CustomerForm onSubmit={handleSubmit} loading={loading} />
          </div>
        </section>

        {result ? (
          <PredictionCard
            prediction={result.prediction}
            probability={result.probability}
            metrics={result.metrics}
          />
        ) : null}

        <Footer />
      </div>
    </main>
  );
}