import "./App.css";
import { GiInvertedDice5 } from "react-icons/gi";
import { GoLinkExternal } from "react-icons/go";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import Accordion from "@mui/material/Accordion";
import AccordionSummary from "@mui/material/AccordionSummary";
import AccordionDetails from "@mui/material/AccordionDetails";
import Typography from "@mui/material/Typography";
import { IoMdArrowDropdown } from "react-icons/io";

const theme = createTheme({
  palette: {
    mode: "light",
    primary: { main: "#1c1c1c" },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <section id="home" className="h-full w-full text-[#1c1c1c] px-10 py-5">
        <div className="flex justify-between items-center">
          <div className="flex justify-center flex-col max-w-[40%]">
            <img src="/banner-title.png" alt="" className="w-[60%]" />
            <p className="w-[80%] text-left">
              MewTube is a portal into my becoming. It comprises all the
              projects I am currently undertaking. It is connected to my
              personal site to track my ongoing projects.
            </p>
            <button className="cursor-pointer bg-[#1c1c1c] text-white rounded-lg w-fit px-5 py-2 mt-5">
              Exploration
            </button>
          </div>
          <img src="/banner.png" alt="banner" className="w-[60%]" />
        </div>
        <div className="my-8">
          <div className="flex justify-center items-center">
            <h1 className="text-5xl font-bold text-center">Random roll</h1>
            <GiInvertedDice5 size={50} className="mx-5 dice-roll" />
          </div>
          <p className="text-center mt-3">
            A random video from MewTube's curated lists
          </p>
        </div>

        <div className="py-8 flex justify-between items-center">
          <iframe
            className="rounded-lg w-[48vw] h-[500px]"
            src="https://www.youtube.com/embed/HX6iBZkucRk"
            title="7 Books to Change Your Life in 2025 (No Self-Help)"
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
            referrerpolicy="strict-origin-when-cross-origin"
            allowfullscreen
          />
          <div className="w-1/2 p-10 text-lg">
            <img src="/home-arrow.png" alt="" className="w-28" />
            <p>
              Lorem ipsum dolor sit amet consectetur adipisicing elit. In, quia
              rem? Numquam adipisci odio, rem neque veritatis nulla sapiente ad
              quo ratione incidunt fuga doloremque itaque dolor fugiat similique
              voluptates. Perspiciatis unde laboriosam nulla, delectus dolores
              ex illum earum voluptate incidunt necessitatibus aliquid eum!
              Tempora excepturi quasi debitis architecto, beatae enim tenetur
              voluptates ipsum id animi assumenda iste accusantium vitae tempore
              provident praesentium nihil cupiditate placeat aut, quos earum
              laboriosam vero dolores incidunt.
            </p>
            <button className="cursor-pointer bg-[#1c1c1c] text-white rounded-lg w-fit px-5 py-2 mt-5">
              Roll the dice!
            </button>
          </div>
        </div>

        <div className="flex flex-col justify-center items-center">
          <img
            src="/mew.gif"
            alt="Mew excited waiting for you"
            className="w-52"
          />
          <textarea
            className="bg-slate-200 rounded-lg text-slate-700 p-8 w-[50%] h-[300px] text-2xl"
            type="text"
            placeholder="Ask Mew to look for something... He seems excited :D You can ask something related to ongoing projects and mew may search it through the index and the articles."
          ></textarea>
        </div>

        <div className="flex flex-wrap gap-8 justify-center items-center p-10 px-20 my-8">
          <div className="w-100 h-94 bg-slate-200 shadow rounded-lg p-8 cursor-pointer hover:shadow-lg">
            <h1 className="text-3xl text-slate-700 font-semibold">
              A Project On Impressionism
            </h1>
            <p className="mt-4 text-slate-600 text">
              Lorem ipsum, dolor sit amet consectetur adipisicing elit.
              Distinctio quas reprehenderit, consequuntur non ex quae recusandae
              ipsam a veniam in est officiis error nisi, accusantium sint ab ut
              laboriosam dignissimos!
            </p>
            <button className="flex items-center justify-center gap-1 cursor-pointer bg-[#1c1c1c] text-white rounded-lg w-fit px-5 py-2 mt-5">
              Read on the site <GoLinkExternal />
            </button>
          </div>
          <div className="w-100 h-94 bg-slate-200 shadow rounded-lg p-8 cursor-pointer hover:shadow-lg">
            <h1 className="text-3xl text-slate-700 font-semibold">
              A Project On Impressionism
            </h1>
            <p className="mt-4 text-slate-600 text">
              Lorem ipsum, dolor sit amet consectetur adipisicing elit.
              Distinctio quas reprehenderit, consequuntur non ex quae recusandae
              ipsam a veniam in est officiis error nisi, accusantium sint ab ut
              laboriosam dignissimos!
            </p>
            <button className="flex items-center justify-center gap-1 cursor-pointer bg-[#1c1c1c] text-white rounded-lg w-fit px-5 py-2 mt-5">
              Read on the site <GoLinkExternal />
            </button>
          </div>
          <div className="w-100 h-94 bg-slate-200 shadow rounded-lg p-8 cursor-pointer hover:shadow-lg">
            <h1 className="text-3xl text-slate-700 font-semibold">
              A Project On Impressionism
            </h1>
            <p className="mt-4 text-slate-600 text">
              Lorem ipsum, dolor sit amet consectetur adipisicing elit.
              Distinctio quas reprehenderit, consequuntur non ex quae recusandae
              ipsam a veniam in est officiis error nisi, accusantium sint ab ut
              laboriosam dignissimos!
            </p>
            <button className="flex items-center justify-center gap-1  cursor-pointer bg-[#1c1c1c] text-white rounded-lg w-fit px-5 py-2 mt-5">
              Read on the site <GoLinkExternal />
            </button>
          </div>
          <div className="w-100 h-94 bg-slate-200 shadow rounded-lg p-8 cursor-pointer hover:shadow-lg">
            <h1 className="text-3xl text-slate-700 font-semibold">
              A Project On Impressionism
            </h1>
            <p className="mt-4 text-slate-600 text">
              Lorem ipsum, dolor sit amet consectetur adipisicing elit.
              Distinctio quas reprehenderit, consequuntur non ex quae recusandae
              ipsam a veniam in est officiis error nisi, accusantium sint ab ut
              laboriosam dignissimos!
            </p>
            <button className="flex items-center justify-center gap-1 cursor-pointer bg-[#1c1c1c] text-white rounded-lg w-fit px-5 py-2 mt-5">
              Read on the site <GoLinkExternal />
            </button>
          </div>
          <div className="w-100 h-94 bg-slate-200 shadow rounded-lg p-8 cursor-pointer hover:shadow-lg">
            <h1 className="text-3xl text-slate-700 font-semibold">
              A Project On Impressionism
            </h1>
            <p className="mt-4 text-slate-600 text">
              Lorem ipsum, dolor sit amet consectetur adipisicing elit.
              Distinctio quas reprehenderit, consequuntur non ex quae recusandae
              ipsam a veniam in est officiis error nisi, accusantium sint ab ut
              laboriosam dignissimos!
            </p>
            <button className="flex items-center justify-center gap-1 cursor-pointer bg-[#1c1c1c] text-white rounded-lg w-fit px-5 py-2 mt-5">
              Read on the site <GoLinkExternal />
            </button>
          </div>
        </div>

        <div className="flex justify-center gap-5">
          <div>
            <iframe
              className="rounded-lg w-[48vw] h-[500px]"
              src="https://www.youtube.com/embed/HX6iBZkucRk"
              title="7 Books to Change Your Life in 2025 (No Self-Help)"
              frameborder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
              referrerpolicy="strict-origin-when-cross-origin"
              allowfullscreen
            />
          </div>
          <div>
            <div>
              <h1 className="text-3xl font-semibold text-slate-800">
                Some more Suggestions
              </h1>
              <div>
                <Accordion className="shadow-xl my-5 rounded-lg">
                  <AccordionSummary
                    expandIcon={<IoMdArrowDropdown color="white" />}
                    aria-controls="panel1-content"
                    id="panel1-header"
                    sx={{
                      backgroundColor: "#1c1c1c",
                      color: "whitesmoke",
                      borderRadius: "5px",
                    }}
                  >
                    <Typography component="span">Accordion 1</Typography>
                  </AccordionSummary>
                  <iframe
                    className="rounded-lg w-[50%] h-[250px] mx-auto mt-8"
                    src="https://www.youtube.com/embed/HX6iBZkucRk"
                    title="7 Books to Change Your Life in 2025 (No Self-Help)"
                    frameborder="0"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                    referrerpolicy="strict-origin-when-cross-origin"
                    allowfullscreen
                  />
                  <AccordionDetails className="w-[80%] mx-auto">
                    <Typography>
                      Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                      Suspendisse malesuada lacus ex, sit amet blandit leo
                      lobortis eget.
                    </Typography>
                  </AccordionDetails>
                </Accordion>
              </div>
            </div>
          </div>
        </div>
      </section>
    </ThemeProvider>
  );
}

export default App;
