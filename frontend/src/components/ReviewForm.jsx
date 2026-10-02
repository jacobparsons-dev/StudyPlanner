function ReviewForm({
  userAnswer,
  setUserAnswer,
  confidence,
  setConfidence,
  feedback,
  onSubmitReview,
  onNextCard,
}) {
  return (
    <>
      {!feedback && (
        <>
          <div className="mt-6">
            <label className="block">
              <span className="mb-2 block text-sm font-medium text-slate-600">
                Your answer
              </span>

              <textarea
                value={userAnswer}
                onChange={(e) => setUserAnswer(e.target.value)}
                placeholder="Type your answer here..."
                rows="4"
                className="w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-slate-700 outline-none transition focus:border-sky-200"
              />
            </label>
          </div>

          <div className="mt-6">
            <label className="block">
              <span className="mb-2 block text-sm font-medium text-slate-600">
                Confidence
              </span>

              <select
                value={confidence}
                onChange={(e) =>
                  setConfidence(Number(e.target.value))
                }
                className="w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-slate-700 outline-none transition focus:border-pink-200"
              >
                <option value={1}>1 - Very unsure</option>
                <option value={2}>2 - Unsure</option>
                <option value={3}>3 - Neutral</option>
                <option value={4}>4 - Confident</option>
                <option value={5}>5 - Very confident</option>
              </select>
            </label>
          </div>
        </>
      )}

      {feedback && (
        <div
          className={`mt-6 rounded-2xl p-5 ${
            feedback.correct
              ? "bg-sky-50 ring-1 ring-sky-100"
              : "bg-pink-50 ring-1 ring-pink-100"
          }`}
        >
          <p
            className={`text-lg font-semibold ${
              feedback.correct
                ? "text-sky-500"
                : "text-pink-500"
            }`}
          >
            {feedback.correct ? "✓ Correct" : "✗ Not quite"}
          </p>

          <div className="mt-4">
            <p className="text-sm font-medium text-slate-400">
              Your answer
            </p>

            <p className="mt-1 text-slate-700">
              {feedback.user_answer}
            </p>
          </div>

          <div className="mt-4">
            <p className="text-sm font-medium text-slate-400">
              Expected answer
            </p>

            <p className="mt-1 text-slate-700">
              {feedback.expected_answer}
            </p>
          </div>

          <div className="mt-4">
            <p className="text-sm font-medium text-slate-400">
              Confidence
            </p>

            <p className="mt-1 text-slate-700">
              {feedback.confidence} / 5
            </p>
          </div>
        </div>
      )}

      <div className="mt-6 flex flex-wrap gap-3">
        {!feedback && (
          <button
            onClick={onSubmitReview}
            disabled={!userAnswer.trim()}
            className="rounded-2xl bg-pink-300 px-5 py-3 font-medium text-slate-800 shadow-sm transition hover:bg-pink-400 disabled:cursor-not-allowed disabled:opacity-50"
          >
            Submit Answer
          </button>
        )}

        <button
          onClick={onNextCard}
          className="rounded-2xl border border-sky-200 bg-white px-5 py-3 font-medium text-sky-400 transition hover:bg-sky-50"
        >
          {feedback ? "Next Card" : "Skip / Next Card"}
        </button>
      </div>
    </>
  );
}

export default ReviewForm;