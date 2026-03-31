function ReviewForm({
  correct,
  confidence,
  setCorrect,
  setConfidence,
  onSubmitReview,
  onNextCard,
}) {
  return (
    <>
      <div className="mt-6 grid gap-4 sm:grid-cols-2">
        <label className="block">
          <span className="mb-2 block text-sm font-medium text-slate-600">
            Correct
          </span>
          <select
            value={correct}
            onChange={(e) => setCorrect(Number(e.target.value))}
            className="w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-slate-700 outline-none transition focus:border-sky-200"
          >
            <option value={1}>Yes</option>
            <option value={0}>No</option>
          </select>
        </label>

        <label className="block">
          <span className="mb-2 block text-sm font-medium text-slate-600">
            Confidence
          </span>
          <select
            value={confidence}
            onChange={(e) => setConfidence(Number(e.target.value))}
            className="w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-slate-700 outline-none transition focus:border-pink-200"
          >
            <option value={1}>1</option>
            <option value={2}>2</option>
            <option value={3}>3</option>
          </select>
        </label>
      </div>

      <div className="mt-6 flex flex-wrap gap-3">
        <button
          onClick={onSubmitReview}
          className="rounded-2xl bg-pink-300 px-5 py-3 font-medium text-slate-800 shadow-sm transition hover:bg-pink-400"
        >
          Submit Review
        </button>

        <button
          onClick={onNextCard}
          className="rounded-2xl border border-sky-200 bg-white px-5 py-3 font-medium text-sky-400 transition hover:bg-sky-50"
        >
          Skip / Next Card
        </button>
      </div>
    </>
  );
}

export default ReviewForm;