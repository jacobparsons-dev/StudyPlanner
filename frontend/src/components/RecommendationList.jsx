import { getRecallColor } from "../utils/recall";

function RecommendationList({ cards }) {
  return (
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
  );
}

export default RecommendationList;