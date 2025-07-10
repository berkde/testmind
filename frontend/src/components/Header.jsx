import { Link } from "react-router-dom";
import "./Header.css";

const Header = () => {
  return (
    <header className="header-container">
      <div className="header-content">
        <div className="logo">
          <Link to="/" className="logo-link">
            <h1>testMind</h1>
          </Link>
        </div>
        
        <nav className="nav">
          <ul className="nav-list">
            <li className="nav-list-item">
              <Link to="/" className="nav-link">Home</Link>
            </li>
            <li className="nav-list-item">
              <Link to="/about" className="nav-link">About</Link>
            </li>
            <li className="nav-list-item">
              <Link to="/contact" className="nav-link">Contact</Link>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;
