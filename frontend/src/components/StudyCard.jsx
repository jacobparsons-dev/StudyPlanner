import ReviewForm from "./ReviewForm";
import EmptyState from "./EmptyState";
import { getRecallColor } from "../utils/recall";

function StudyCard({
  currentCard,
  userAnswer,
  setUserAnswer,
  confidence,
  setConfidence,
  feedback,
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

          <p className="text-sm text-slate-400">
            {currentCard.topic}
          </p>
        </div>

        <div className="rounded-full bg-blue-100 px-3 py-1 text-sm font-medium text-sky-500">
          Difficulty {currentCard.difficulty}
        </div>
      </div>

      <h2 className="text-2xl font-semibold leading-snug text-slate-800">
        {currentCard.question}
      </h2>

      <div className="mt-5 rounded-2xl bg-slate-50/80 px-4 py-3 ring-1 ring-slate-100">
        <p className="text-sm text-slate-400">
          Predicted recall
        </p>

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

      <ReviewForm
        userAnswer={userAnswer}
        setUserAnswer={setUserAnswer}
        confidence={confidence}
        setConfidence={setConfidence}
        feedback={feedback}
        onSubmitReview={onSubmitReview}
        onNextCard={onNextCard}
      />
    </>
  );
}

export default StudyCard;