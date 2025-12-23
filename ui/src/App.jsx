import "./App.css";

function App() {
  return (
    <div className="min-h-screen">
      <div className="py-5 text-center">
        <div className="flex justify-between gap-2 p-3">
          <h1 className="bg-purple-700 font-bold text-white px-5 py-3">
            MewTube
          </h1>
          <div className="flex w-full w-full items-center gap-2">
            <input type="text" placeholder="Email" className="w-full" />
            <button type="submit" variant="outline">
              Search
            </button>
          </div>
        </div>
      </div>
      <div className="relative h-[45vh]">
        <img src="/assets/banner.jpg" className="w-full h-full object-cover" />
        Search
        <div className="absolute inset-0 bg-black/40" />
        <div className="absolute inset-0 flex items-center px-12">
          <div>
            <img src="/assets/mew.gif" className="w-28 mb-6" />
            <h2 className="text-5xl font-bold text-slate-200">MewTube</h2>
            <p className="text-xl text-slate-200">
              Intriguing content, from your interests
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
