import ReviewForm from "./ReviewForm";
import EmptyState from "./EmptyState";
import { getRecallColor } from "../utils/recall";

function StudyCard({
  currentCard,
  showAnswer,
  setShowAnswer,
  correct,
  confidence,
  setCorrect,
  setConfidence,
  onNextCard,
  onSubmitReview,
}) {
  if (!currentCard) {
    return <EmptyState />;
  }

  return (
    <>
      <div className="mb-5 flex items-center justify-between gap-4">
        <div>
          <p className="text-sm font-medium text-sky-400">
            {currentCard.subject}
          </p>
          <p className="text-sm text-slate-400">{currentCard.topic}</p>
        </div>

        <div className="rounded-full bg-blue-100 px-3 py-1 text-sm font-medium text-sky-500">
          Difficulty {currentCard.difficulty}
        </div>
      </div>

      <h2 className="text-2xl font-semibold leading-snug text-slate-800">
        {currentCard.question}
      </h2>

      <div className="mt-5 rounded-2xl bg-slate-50/80 px-4 py-3 ring-1 ring-slate-100">
        <p className="text-sm text-slate-400">Predicted recall</p>
        <p
          className={`text-2xl font-bold ${getRecallColor(
            currentCard.recall_probability
          )}`}
        >
          {currentCard.recall_probability !== undefined
            ? currentCard.recall_probability.toFixed(2)
            : "N/A"}
        </p>
      </div>

      {!showAnswer ? (
        <div className="mt-6 flex flex-wrap gap-3">
          <button
            onClick={() => setShowAnswer(true)}
            className="rounded-2xl bg-sky-300 px-5 py-3 font-medium text-slate-800 shadow-sm transition hover:bg-sky-400"
          >
            Reveal Answer
          </button>

          <button
            onClick={onNextCard}
            className="rounded-2xl border border-pink-200 bg-white px-5 py-3 font-medium text-pink-400 transition hover:bg-pink-50"
          >
            Skip / Next Card
          </button>
        </div>
      ) : (
        <>
          <div className="mt-6 rounded-2xl bg-rose-50 p-4 ring-1 ring-pink-100">
            <p className="text-sm font-medium text-pink-400">Answer</p>
            <p className="mt-2 text-slate-700">{currentCard.answer}</p>
          </div>

          <ReviewForm
            correct={correct}
            confidence={confidence}
            setCorrect={setCorrect}
            setConfidence={setConfidence}
            onSubmitReview={onSubmitReview}
            onNextCard={onNextCard}
          />
        </>
      )}
    </>
  );
}

export default StudyCard;