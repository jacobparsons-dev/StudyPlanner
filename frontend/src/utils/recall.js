export function getRecallColor(probability) {
  if (probability === undefined || probability === null) {
    return "text-slate-400";
  }
  if (probability < 0.4) return "text-pink-400";
  if (probability < 0.7) return "text-violet-400";
  return "text-sky-400";
}