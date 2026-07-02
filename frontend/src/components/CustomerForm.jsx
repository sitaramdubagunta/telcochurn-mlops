import { useForm } from 'react-hook-form';

const selectOptions = {
  gender: ['Female', 'Male'],
  SeniorCitizen: ['0', '1'],
  Partner: ['Yes', 'No'],
  Dependents: ['Yes', 'No'],
  PhoneService: ['Yes', 'No'],
  MultipleLines: ['No', 'Yes', 'No phone service'],
  InternetService: ['DSL', 'Fiber optic', 'No'],
  OnlineSecurity: ['Yes', 'No', 'No internet service'],
  OnlineBackup: ['Yes', 'No', 'No internet service'],
  DeviceProtection: ['Yes', 'No', 'No internet service'],
  TechSupport: ['Yes', 'No', 'No internet service'],
  StreamingTV: ['Yes', 'No', 'No internet service'],
  StreamingMovies: ['Yes', 'No', 'No internet service'],
  Contract: ['Month-to-month', 'One year', 'Two year'],
  PaperlessBilling: ['Yes', 'No'],
  PaymentMethod: [
    'Electronic check',
    'Mailed check',
    'Bank transfer (automatic)',
    'Credit card (automatic)',
  ],
};

const defaultValues = {
  gender: 'Female',
  SeniorCitizen: '0',
  Partner: 'No',
  Dependents: 'No',
  tenure: 1,
  PhoneService: 'Yes',
  MultipleLines: 'No',
  InternetService: 'DSL',
  OnlineSecurity: 'No',
  OnlineBackup: 'No',
  DeviceProtection: 'No',
  TechSupport: 'No',
  StreamingTV: 'No',
  StreamingMovies: 'No',
  Contract: 'Month-to-month',
  PaperlessBilling: 'Yes',
  PaymentMethod: 'Electronic check',
  MonthlyCharges: 70,
  TotalCharges: 70,
};

function Field({ label, children, fullWidth = false }) {
  return (
    <label className={fullWidth ? 'md:col-span-2' : ''}>
      <span className="mb-2 block text-sm font-medium text-slate-700">{label}</span>
      {children}
    </label>
  );
}

function SelectInput({ name, register, options }) {
  return (
    <select
      {...register(name)}
      className="w-full rounded-xl border border-slate-300 bg-white px-3 py-2.5 text-sm text-slate-900 shadow-sm outline-none transition hover:border-slate-400 focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
    >
      {options.map((option) => (
        <option key={option} value={option}>
          {option}
        </option>
      ))}
    </select>
  );
}

function NumberInput({ name, register, step = '1', min = '0' }) {
  return (
    <input
      type="number"
      min={min}
      step={step}
      {...register(name, { valueAsNumber: true })}
      className="w-full rounded-xl border border-slate-300 bg-white px-3 py-2.5 text-sm text-slate-900 shadow-sm outline-none transition hover:border-slate-400 focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
    />
  );
}

export default function CustomerForm({ onSubmit, loading }) {
  const { register, handleSubmit } = useForm({ defaultValues });

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <div className="grid gap-4 md:grid-cols-2">
        <Field label="Gender">
          <SelectInput name="gender" register={register} options={selectOptions.gender} />
        </Field>
        <Field label="Senior Citizen">
          <SelectInput name="SeniorCitizen" register={register} options={selectOptions.SeniorCitizen} />
        </Field>
        <Field label="Partner">
          <SelectInput name="Partner" register={register} options={selectOptions.Partner} />
        </Field>
        <Field label="Dependents">
          <SelectInput name="Dependents" register={register} options={selectOptions.Dependents} />
        </Field>
        <Field label="Tenure">
          <NumberInput name="tenure" register={register} min="0" />
        </Field>
        <Field label="Phone Service">
          <SelectInput name="PhoneService" register={register} options={selectOptions.PhoneService} />
        </Field>
        <Field label="Multiple Lines">
          <SelectInput name="MultipleLines" register={register} options={selectOptions.MultipleLines} />
        </Field>
        <Field label="Internet Service">
          <SelectInput name="InternetService" register={register} options={selectOptions.InternetService} />
        </Field>
        <Field label="Online Security">
          <SelectInput name="OnlineSecurity" register={register} options={selectOptions.OnlineSecurity} />
        </Field>
        <Field label="Online Backup">
          <SelectInput name="OnlineBackup" register={register} options={selectOptions.OnlineBackup} />
        </Field>
        <Field label="Device Protection">
          <SelectInput name="DeviceProtection" register={register} options={selectOptions.DeviceProtection} />
        </Field>
        <Field label="Tech Support">
          <SelectInput name="TechSupport" register={register} options={selectOptions.TechSupport} />
        </Field>
        <Field label="Streaming TV">
          <SelectInput name="StreamingTV" register={register} options={selectOptions.StreamingTV} />
        </Field>
        <Field label="Streaming Movies">
          <SelectInput name="StreamingMovies" register={register} options={selectOptions.StreamingMovies} />
        </Field>
        <Field label="Contract">
          <SelectInput name="Contract" register={register} options={selectOptions.Contract} />
        </Field>
        <Field label="Paperless Billing">
          <SelectInput name="PaperlessBilling" register={register} options={selectOptions.PaperlessBilling} />
        </Field>
        <Field label="Payment Method" fullWidth>
          <SelectInput name="PaymentMethod" register={register} options={selectOptions.PaymentMethod} />
        </Field>
        <Field label="Monthly Charges">
          <NumberInput name="MonthlyCharges" register={register} step="0.01" min="0" />
        </Field>
        <Field label="Total Charges">
          <NumberInput name="TotalCharges" register={register} step="0.01" min="0" />
        </Field>
      </div>

      <button
        type="submit"
        disabled={loading}
        className="inline-flex w-full items-center justify-center rounded-xl bg-blue-600 px-4 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-blue-400"
      >
        {loading ? (
          <span className="inline-flex items-center gap-2">
            <span className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
            Predicting
          </span>
        ) : (
          'Predict Churn'
        )}
      </button>
    </form>
  );
}