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

function Field({ label, children, error, fullWidth = false }) {
  return (
    <label className={fullWidth ? 'md:col-span-2' : ''}>
      <span className="mb-2 block text-sm font-medium text-slate-700">{label}</span>
      {children}
      {error ? <span className="mt-1 block text-xs font-medium text-red-600">{error}</span> : null}
    </label>
  );
}

function SelectInput({ name, register, options, disabled }) {
  return (
    <select
      disabled={disabled}
      {...register(name, { required: 'Required' })}
      className="w-full rounded-md border border-slate-300 bg-white px-3 py-2.5 text-sm text-slate-900 shadow-sm outline-none transition hover:border-slate-400 focus:border-blue-500 focus:ring-2 focus:ring-blue-100 disabled:cursor-not-allowed disabled:bg-slate-100"
    >
      {options.map((option) => (
        <option key={option} value={option}>
          {option}
        </option>
      ))}
    </select>
  );
}

function NumberInput({ name, register, step = '1', min = '0', disabled }) {
  return (
    <input
      type="number"
      min={min}
      step={step}
      disabled={disabled}
      {...register(name, {
        valueAsNumber: true,
        required: 'Required',
        min: { value: Number(min), message: `Must be at least ${min}` },
      })}
      className="w-full rounded-md border border-slate-300 bg-white px-3 py-2.5 text-sm text-slate-900 shadow-sm outline-none transition hover:border-slate-400 focus:border-blue-500 focus:ring-2 focus:ring-blue-100 disabled:cursor-not-allowed disabled:bg-slate-100"
    />
  );
}

function FormSection({ title, children }) {
  return (
    <fieldset className="space-y-4">
      <legend className="text-sm font-semibold text-slate-950">{title}</legend>
      <div className="grid gap-4 md:grid-cols-2">{children}</div>
    </fieldset>
  );
}

export default function CustomerForm({ onSubmit, loading, disabled, samplePayload }) {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm({ defaultValues });

  const fillSample = () => {
    reset(samplePayload || defaultValues);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <FormSection title="Customer Profile">
        <Field label="Gender" error={errors.gender?.message}>
          <SelectInput disabled={disabled} name="gender" register={register} options={selectOptions.gender} />
        </Field>
        <Field label="Senior Citizen" error={errors.SeniorCitizen?.message}>
          <SelectInput disabled={disabled} name="SeniorCitizen" register={register} options={selectOptions.SeniorCitizen} />
        </Field>
        <Field label="Partner" error={errors.Partner?.message}>
          <SelectInput disabled={disabled} name="Partner" register={register} options={selectOptions.Partner} />
        </Field>
        <Field label="Dependents" error={errors.Dependents?.message}>
          <SelectInput disabled={disabled} name="Dependents" register={register} options={selectOptions.Dependents} />
        </Field>
        <Field label="Tenure" error={errors.tenure?.message}>
          <NumberInput disabled={disabled} name="tenure" register={register} min="0" />
        </Field>
      </FormSection>

      <FormSection title="Services">
        <Field label="Phone Service" error={errors.PhoneService?.message}>
          <SelectInput disabled={disabled} name="PhoneService" register={register} options={selectOptions.PhoneService} />
        </Field>
        <Field label="Multiple Lines" error={errors.MultipleLines?.message}>
          <SelectInput disabled={disabled} name="MultipleLines" register={register} options={selectOptions.MultipleLines} />
        </Field>
        <Field label="Internet Service" error={errors.InternetService?.message}>
          <SelectInput disabled={disabled} name="InternetService" register={register} options={selectOptions.InternetService} />
        </Field>
        <Field label="Online Security" error={errors.OnlineSecurity?.message}>
          <SelectInput disabled={disabled} name="OnlineSecurity" register={register} options={selectOptions.OnlineSecurity} />
        </Field>
        <Field label="Online Backup" error={errors.OnlineBackup?.message}>
          <SelectInput disabled={disabled} name="OnlineBackup" register={register} options={selectOptions.OnlineBackup} />
        </Field>
        <Field label="Device Protection" error={errors.DeviceProtection?.message}>
          <SelectInput disabled={disabled} name="DeviceProtection" register={register} options={selectOptions.DeviceProtection} />
        </Field>
        <Field label="Tech Support" error={errors.TechSupport?.message}>
          <SelectInput disabled={disabled} name="TechSupport" register={register} options={selectOptions.TechSupport} />
        </Field>
        <Field label="Streaming TV" error={errors.StreamingTV?.message}>
          <SelectInput disabled={disabled} name="StreamingTV" register={register} options={selectOptions.StreamingTV} />
        </Field>
        <Field label="Streaming Movies" error={errors.StreamingMovies?.message}>
          <SelectInput disabled={disabled} name="StreamingMovies" register={register} options={selectOptions.StreamingMovies} />
        </Field>
      </FormSection>

      <FormSection title="Billing">
        <Field label="Contract" error={errors.Contract?.message}>
          <SelectInput disabled={disabled} name="Contract" register={register} options={selectOptions.Contract} />
        </Field>
        <Field label="Paperless Billing" error={errors.PaperlessBilling?.message}>
          <SelectInput disabled={disabled} name="PaperlessBilling" register={register} options={selectOptions.PaperlessBilling} />
        </Field>
        <Field label="Payment Method" error={errors.PaymentMethod?.message} fullWidth>
          <SelectInput disabled={disabled} name="PaymentMethod" register={register} options={selectOptions.PaymentMethod} />
        </Field>
        <Field label="Monthly Charges" error={errors.MonthlyCharges?.message}>
          <NumberInput disabled={disabled} name="MonthlyCharges" register={register} step="0.01" min="0" />
        </Field>
        <Field label="Total Charges" error={errors.TotalCharges?.message}>
          <NumberInput disabled={disabled} name="TotalCharges" register={register} step="0.01" min="0" />
        </Field>
      </FormSection>

      <div className="grid gap-3 sm:grid-cols-[1fr_auto_auto]">
        <button
          type="submit"
          disabled={loading || disabled}
          className="inline-flex items-center justify-center rounded-md bg-slate-950 px-4 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-400"
        >
          {loading ? 'Scoring customer...' : 'Predict Churn'}
        </button>
        <button
          type="button"
          onClick={fillSample}
          disabled={loading || disabled}
          className="rounded-md border border-slate-300 bg-white px-4 py-3 text-sm font-semibold text-slate-700 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:bg-slate-100"
        >
          Fill Example
        </button>
        <button
          type="button"
          onClick={() => reset(defaultValues)}
          disabled={loading}
          className="rounded-md border border-slate-300 bg-white px-4 py-3 text-sm font-semibold text-slate-700 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:bg-slate-100"
        >
          Reset
        </button>
      </div>
    </form>
  );
}
