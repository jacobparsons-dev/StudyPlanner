import { useEffect, useState } from "react";
import { getRecommendations, createReview } from "./api";

function App() {
  const [cards, setCards] = useState([]);
  const [currentCard, setCurrentCard] = useState(null);
  const [showAnswer, setShowAnswer] = useState(false);
  const [correct, setCorrect] = useState(1);
  const [confidence, setConfidence] = useState(3);
  const [loading, setLoading] = useState(true);

  const fetchRecommendations = async () => {
    try {
      setLoading(true);
      const data = await getRecommendations();
      console.log("Recommendations:", data);
      setCards(data);
      setCurrentCard(data.length > 0 ? data[0] : null);
    } catch (error) {
      console.error("Failed to fetch recommendations:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRecommendations();
  }, []);

  const handleSubmitReview = async () => {
    if (!currentCard) return;

    try {
      await createReview({
        item_id: currentCard.item_id,
        correct,
        confidence,
        response_time: 5.0,
      });

      setShowAnswer(false);
      setCorrect(1);
      setConfidence(3);
      await fetchRecommendations();
    } catch (error) {
      console.error("Failed to submit review:", error);
    }
  };

  if (loading) {
    return <div style={{ padding: "2rem" }}>Loading...</div>;
  }

  return (
    <div
      style={{
        maxWidth: "800px",
        margin: "0 auto",
        padding: "2rem",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <h1>Study Planner</h1>
      <p>AI-powered adaptive revision</p>

      {currentCard ? (
        <div
          style={{
            border: "1px solid #ccc",
            borderRadius: "12px",
            padding: "1.5rem",
            marginBottom: "2rem",
          }}
        >
          <h2>Review Card</h2>
          <p>
            <strong>Subject:</strong> {currentCard.subject}
          </p>
          <p>
            <strong>Topic:</strong> {currentCard.topic}
          </p>
          <p>
            <strong>Question:</strong> {currentCard.question}
          </p>
          <p>
            <strong>Predicted Recall:</strong>{" "}
            {currentCard.recall_probability !== undefined
              ? currentCard.recall_probability.toFixed(2)
              : "N/A"}
          </p>

          {!showAnswer ? (
            <button onClick={() => setShowAnswer(true)}>Reveal Answer</button>
          ) : (
            <>
              <p>
                <strong>Answer:</strong> {currentCard.answer}
              </p>

              <div style={{ marginTop: "1rem" }}>
                <label>
                  Correct:
                  <select
                    value={correct}
                    onChange={(e) => setCorrect(Number(e.target.value))}
                    style={{ marginLeft: "0.5rem" }}
                  >
                    <option value={1}>Yes</option>
                    <option value={0}>No</option>
                  </select>
                </label>
              </div>

              <div style={{ marginTop: "1rem" }}>
                <label>
                  Confidence:
                  <select
                    value={confidence}
                    onChange={(e) => setConfidence(Number(e.target.value))}
                    style={{ marginLeft: "0.5rem" }}
                  >
                    <option value={1}>1</option>
                    <option value={2}>2</option>
                    <option value={3}>3</option>
                    <option value={4}>4</option>
                    <option value={5}>5</option>
                  </select>
                </label>
              </div>

              <button onClick={handleSubmitReview} style={{ marginTop: "1rem" }}>
                Submit Review
              </button>
            </>
          )}
        </div>
      ) : (
        <p>No cards available.</p>
      )}

      <div>
        <h2>Next 5 Cards</h2>
        {cards.map((card) => (
          <div
            key={card.item_id}
            style={{
              border: "1px solid #ddd",
              borderRadius: "8px",
              padding: "1rem",
              marginBottom: "0.75rem",
            }}
          >
            <p>
              <strong>{card.question}</strong>
            </p>
            <p>
              {card.subject} · {card.topic}
            </p>
            <p>
              Recall probability:{" "}
              {card.recall_probability !== undefined
                ? card.recall_probability.toFixed(2)
                : "N/A"}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;