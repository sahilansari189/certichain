import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { ShieldCheck } from 'lucide-react';
import Home from './pages/Home';
import Mint from './pages/Mint';
import Verify from './pages/Verify';

function App() {
  return (
    <Router>
      <div className="app-container">
        <header className="header">
          <Link to="/" className="logo">
            <ShieldCheck size={32} color="var(--primary)" />
            <span>Certi<span className="text-gradient">Chain</span></span>
          </Link>
          <nav className="nav-links">
            <Link to="/" className="nav-link">Home</Link>
            <Link to="/mint" className="nav-link">Issue Certificate</Link>
            <Link to="/verify" className="nav-link">Verify</Link>
          </nav>
        </header>

        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/mint" element={<Mint />} />
            <Route path="/verify" element={<Verify />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
