import { useEffect, useState } from "react";
import { getRecommendations, createReview } from "./api";

function App() {
  const [cards, setCards] = useState([]);
  const [currentCard, setCurrentCard] = useState(null);
  const [showAnswer, setShowAnswer] = useState(false);
  const [correct, setCorrect] = useState(1);
  const [confidence, setConfidence] = useState(3);
  const [loading, setLoading] = useState(true);
  const [startTime, setStartTime] = useState(null);

  const fetchRecommendations = async () => {
    try {
      setLoading(true);
      const data = await getRecommendations();
      setCards(data);

      if (data.length > 0) {
        setCurrentCard(data[0]);
        setStartTime(Date.now());
      } else {
        setCurrentCard(null);
        setStartTime(null);
      }

      setShowAnswer(false);
    } catch (error) {
      console.error("Failed to fetch recommendations:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRecommendations();
  }, []);

  const handleNextCard = async () => {
    if (!currentCard) return;

    try {
      await createReview({
        item_id: currentCard.item_id,
        correct: 0,
        confidence: 1,
        response_time: 0,
      });
    } catch (error) {
      console.error("Failed to skip:", error);
    }

    const updatedCards = cards.filter(
      (card) => card.item_id !== currentCard.item_id
    );

    setCards(updatedCards);

    if (updatedCards.length > 0) {
      setCurrentCard(updatedCards[0]);
      setStartTime(Date.now());
    } else {
      setCurrentCard(null);
      setStartTime(null);
    }

    setShowAnswer(false);
    setCorrect(1);
    setConfidence(3);

    if (updatedCards.length === 0) {
      await fetchRecommendations();
    }
  };

  const handleSubmitReview = async () => {
    if (!currentCard) return;

    const responseTime = startTime ? (Date.now() - startTime) / 1000 : 0;

    try {
      await createReview({
        item_id: currentCard.item_id,
        correct,
        confidence,
        response_time: responseTime,
      });

      const updatedCards = cards.filter(
        (card) => card.item_id !== currentCard.item_id
      );

      setCards(updatedCards);

      if (updatedCards.length > 0) {
        setCurrentCard(updatedCards[0]);
        setStartTime(Date.now());
      } else {
        setCurrentCard(null);
        setStartTime(null);
      }

      setShowAnswer(false);
      setCorrect(1);
      setConfidence(3);

      if (updatedCards.length === 0) {
        await fetchRecommendations();
      }
    } catch (error) {
      console.error("Failed to submit review:", error);
    }
  };

  const getRecallColor = (probability) => {
    if (probability === undefined || probability === null) {
      return "text-slate-400";
    }
    if (probability < 0.4) return "text-pink-400";
    if (probability < 0.7) return "text-violet-400";
    return "text-sky-400";
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-pink-50 to-rose-50 flex items-center justify-center">
        <p className="text-lg text-slate-500">Loading...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-pink-50 to-rose-50">
      <div className="mx-auto max-w-6xl px-6 py-10">
        <header className="mb-8">
          <h1 className="text-4xl font-bold tracking-tight text-sky-400">
            Study Planner
          </h1>
          <p className="mt-2 text-slate-500">
            AI-powered adaptive revision with memory modeling
          </p>

          <div className="mt-4 inline-flex rounded-full bg-white/80 px-4 py-2 shadow-sm ring-1 ring-pink-100">
            <span className="text-sm font-medium text-slate-600">
              {cards.length} cards left in this session
            </span>
          </div>
        </header>

        <div className="grid gap-8 lg:grid-cols-[1.45fr_1fr]">
          <section className="rounded-3xl bg-white/90 p-6 shadow-lg ring-1 ring-sky-100 backdrop-blur-sm">
            {currentCard ? (
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
                      onClick={handleNextCard}
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
                          <option value={4}>4</option>
                          <option value={5}>5</option>
                        </select>
                      </label>
                    </div>

                    <div className="mt-6 flex flex-wrap gap-3">
                      <button
                        onClick={handleSubmitReview}
                        className="rounded-2xl bg-pink-300 px-5 py-3 font-medium text-slate-800 shadow-sm transition hover:bg-pink-400"
                      >
                        Submit Review
                      </button>

                      <button
                        onClick={handleNextCard}
                        className="rounded-2xl border border-sky-200 bg-white px-5 py-3 font-medium text-sky-400 transition hover:bg-sky-50"
                      >
                        Skip / Next Card
                      </button>
                    </div>
                  </>
                )}
              </>
            ) : (
              <div className="rounded-2xl bg-slate-50 p-8 text-center">
                <p className="text-slate-500">No cards available.</p>
              </div>
            )}
          </section>

          <aside className="rounded-3xl bg-white/90 p-6 shadow-lg ring-1 ring-pink-100 backdrop-blur-sm">
            <h2 className="text-xl font-semibold text-slate-800">
              Next recommended cards
            </h2>

            <div className="mt-5 space-y-4">
              {cards.map((card) => (
                <div
                  key={card.item_id}
                  className="rounded-2xl border border-slate-100 bg-slate-50/80 p-4"
                >
                  <p className="font-medium text-slate-800">{card.question}</p>
                  <p className="mt-1 text-sm text-slate-400">
                    {card.subject} · {card.topic}
                  </p>
                  <p className="mt-3 text-sm text-slate-500">
                    Recall probability:{" "}
                    <span
                      className={`font-semibold ${getRecallColor(
                        card.recall_probability
                      )}`}
                    >
                      {card.recall_probability !== undefined
                        ? card.recall_probability.toFixed(2)
                        : "N/A"}
                    </span>
                  </p>
                </div>
              ))}
            </div>
          </aside>
        </div>
      </div>
    </div>
  );
}

export default App;