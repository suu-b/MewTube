import "./App.css";

function App() {
  return (
    <section
      id="home"
      className="h-full w-full flex justify-between items-center text-[#1c1c1c] px-10 py-5"
    >
      <div className="flex justify-center flex-col max-w-[40%]">
        <img src="/banner-title.png" alt="" className="w-[60%]" />
        <p className="w-[80%] text-left">
          MewTube is a portal into my becoming. It comprises all the projects I
          am currently undertaking. It is connected to my personal site to track
          my ongoing projects.
        </p>
        <button className="cursor-pointer bg-[#1c1c1c] text-white rounded-lg w-fit px-5 py-2 mt-5">
          Dashboard
        </button>
      </div>
      <img src="/banner.png" alt="banner" className="w-[60%]" />
    </section>
  );
}

export default App;
