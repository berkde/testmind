import "./Home.css";

const Home = () => {
  return (
    <div className="home-container">
      <div className="home-content">
        <h2 className="home-title">Welcome to testMind</h2>

        <p className="home-description">
          testMind is an AI-assisted tool that converts transition states,
          personas, and requirements from specific applications into structured
          software test combination tables using LLM-powered AI agents.
        </p>

        <div className="home-actions">
          <select id="app-select">
            <option value="">-- Please select an app --</option>
            <option value="opt-1">Bug Database</option>
            <option value="opt-2">Register For Golf Lessons</option>
            <option value="opt-3">Post New Ideas</option>
          </select>

          <button className="submit-button">Get started</button>
        </div>
      </div>
    </div>
  );
};

export default Home;
