const FormActions = ({ primaryLabel = "Save Changes", onPrimary }) => {
  return (
    <div className="mt-10 flex justify-end gap-4">
      <button
        type="button"
        className="rounded-xl border border-outline-variant px-6 py-2.5 font-semibold text-on-surface-variant transition-colors hover:bg-surface-container-low"
      >
        Cancel
      </button>
      <button
        type="button"
        onClick={onPrimary}
        className="rounded-xl bg-primary px-8 py-2.5 font-semibold text-on-primary shadow-md transition-colors hover:bg-primary-container"
      >
        {primaryLabel}
      </button>
    </div>
  );
};

export default FormActions;