import { useEffect, useState } from "react";
import { getRecommendations, createReview } from "./api";
import Header from "./components/Header";
import StudyCard from "./components/StudyCard";
import RecommendationList from "./components/RecommendationList";
import LoadingScreen from "./components/LoadingScreen";
import StudyItemsManager from "./components/StudyItemsManager";
function App() {
  const [cards, setCards] = useState([]);
  const [currentCard, setCurrentCard] = useState(null);
  const [userAnswer, setUserAnswer] = useState("");
  const [feedback, setFeedback] = useState(null);
  const [confidence, setConfidence] = useState(3);
  const [loading, setLoading] = useState(true);
  const [startTime, setStartTime] = useState(null);

  const resetReviewState = () => {
    setUserAnswer("");
    setFeedback(null);
    setConfidence(3);
  };

  const moveToNextCard = (updatedCards) => {
    setCards(updatedCards);

    if (updatedCards.length > 0) {
      setCurrentCard(updatedCards[0]);
      setStartTime(Date.now());
    } else {
      setCurrentCard(null);
      setStartTime(null);
    }

    resetReviewState();
  };

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

    moveToNextCard(updatedCards);

    if (updatedCards.length === 0) {
      await fetchRecommendations();
    }
  };

  const handleSubmitReview = async () => {
    if (!currentCard || !userAnswer.trim()) return;

    const responseTime = startTime ? (Date.now() - startTime) / 1000 : 0;

    try {
      const result = await createReview({
        item_id: currentCard.item_id,
        user_answer: userAnswer,
        confidence,
        response_time: responseTime,
      });
      setFeedback(result);
    } catch (error) {
      console.error("Failed to submit review:", error);
    }
  };

  if (loading) {
    return <LoadingScreen />;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-pink-50 to-rose-50">
      <div className="mx-auto max-w-6xl px-6 py-10">
        <Header cardsLeft={cards.length} />

        <div className="grid gap-8 lg:grid-cols-[1.45fr_1fr]">
          <section className="rounded-3xl bg-white/90 p-6 shadow-lg ring-1 ring-sky-100 backdrop-blur-sm">
            <StudyCard
              currentCard={currentCard}
              showAnswer={userAnswer}
              setShowAnswer={setUserAnswer}
              confidence={confidence}
              setConfidencet={setConfidence}
              feedback={feedback}
              onNextCard={handleNextCard}
              onSubmitReview={handleSubmitReview}
            />
          </section>

          <RecommendationList cards={cards} />
        </div>
        <div className="mt-8">
          <StudyItemsManager />
        </div>
      </div>
    </div>
  );
}

export default App;