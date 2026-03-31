function Header({ cardsLeft }) {
  return (
    <header className="mb-8">
      <h1 className="text-4xl font-bold tracking-tight text-sky-400">
        Study Planner
      </h1>
      <p className="mt-2 text-slate-500">
        AI-powered adaptive revision with memory modeling
      </p>

      <div className="mt-4 inline-flex rounded-full bg-white/80 px-4 py-2 shadow-sm ring-1 ring-pink-100">
        <span className="text-sm font-medium text-slate-600">
          {cardsLeft} cards left in this session
        </span>
      </div>
    </header>
  );
}

export default Header;