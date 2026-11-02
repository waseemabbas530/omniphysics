
function App() {
  return (
    <main className="min-h-screen bg-slate-950 flex items-center justify-center p-6">
      <div className="max-w-lg w-full rounded-2xl border border-slate-700 bg-slate-900 p-8 text-center shadow-2xl">
        <h1 className="text-4xl font-bold text-white mb-4">
          OmniPhysics
        </h1>

        <p className="text-slate-300 text-lg mb-6">
          Explore physics through interactive 3D simulations.
        </p>

        <button className="rounded-lg bg-blue-600 px-6 py-3 font-semibold text-white hover:bg-blue-700 transition">
          Start Exploring
        </button>

        <p className="mt-6 text-sm text-green-400">
          Tailwind CSS is working!
        </p>
      </div>
    </main>
  )
}

export default App
