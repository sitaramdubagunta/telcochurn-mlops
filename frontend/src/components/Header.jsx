export default function Header() {
  return (
    <header className="text-center">
      <div className="mb-5 inline-flex items-center rounded-full border border-blue-100 bg-white px-4 py-1.5 text-xs font-semibold uppercase tracking-[0.22em] text-blue-700 shadow-sm">
        Production MLOps Pipeline
      </div>
      <h1 className="text-3xl font-semibold tracking-tight text-slate-900 sm:text-4xl">
        Telecom Customer Churn Prediction
      </h1>
      <p className="mx-auto mt-3 max-w-2xl text-sm leading-6 text-slate-600 sm:text-base">
        Fast, production-style churn scoring for telecom customer profiles.
      </p>
    </header>
  );
}
