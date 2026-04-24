import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';

const Home = () => {
  return (
    <div>
      <motion.div 
        className="main-grid"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div>
          <h1>Immutable Trust.<br/>Verifiable <span className="text-gradient">Data.</span></h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '1.25rem', marginBottom: '3rem', lineHeight: 1.6, maxWidth: '480px' }}>
            Empowering institutions with blockchain-backed, unforgeable certificates on the Sepolia Network.
          </p>
          <div style={{ display: 'flex', gap: '1.5rem' }}>
            <Link to="/mint" style={{ textDecoration: 'none' }}>
              <button className="btn-primary">
                Issue Certificate
              </button>
            </Link>
            <Link to="/verify" style={{ textDecoration: 'none' }}>
              <button className="btn-outline">
                Verify Registry
              </button>
            </Link>
          </div>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginTop: '2rem' }}>
          <div className="feature-box">
            <div className="feature-title">[ 01 ] Cryptographically Secure</div>
            <p style={{ color: 'var(--text-muted)' }}>Each certificate is a unique token on Ethereum that cannot be duplicated, altered, or forged.</p>
          </div>

          <div className="feature-box">
            <div className="feature-title">[ 02 ] Instant Verification</div>
            <p style={{ color: 'var(--text-muted)' }}>Employers and third parties can cryptographically verify credentials in seconds without intermediaries.</p>
          </div>
          
          <div className="feature-box">
            <div className="feature-title">[ 03 ] Decentralized Identity</div>
            <p style={{ color: 'var(--text-muted)' }}>Students retain absolute custody of their achievements in their own personal Web3 wallets.</p>
          </div>
        </div>
      </motion.div>

      {/* How to Use Section */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        style={{ marginTop: '8rem', marginBottom: '4rem' }}
      >
        <div style={{ borderBottom: '1px solid var(--border)', paddingBottom: '1rem', marginBottom: '3rem' }}>
          <h2 style={{ fontSize: '2rem', textTransform: 'uppercase', letterSpacing: '-0.02em' }}>[ SYSTEM WORKFLOW ]</h2>
        </div>
        
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '2rem' }}>
          
          <div className="feature-box" style={{ background: 'transparent', borderTop: '2px solid var(--accent)' }}>
            <div style={{ fontSize: '3rem', fontFamily: 'JetBrains Mono', color: 'var(--accent)', marginBottom: '1rem', opacity: 0.8 }}>01</div>
            <div className="feature-title" style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>ISSUE CREDENTIAL</div>
            <p style={{ color: 'var(--text-muted)', lineHeight: 1.6 }}>
              The institution fills out the student data and executes a transaction on the Sepolia network to mint the non-fungible certificate.
            </p>
          </div>

          <div className="feature-box" style={{ background: 'transparent', borderTop: '2px solid var(--accent)' }}>
            <div style={{ fontSize: '3rem', fontFamily: 'JetBrains Mono', color: 'var(--accent)', marginBottom: '1rem', opacity: 0.8 }}>02</div>
            <div className="feature-title" style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>AUTO NOTIFY</div>
            <p style={{ color: 'var(--text-muted)', lineHeight: 1.6 }}>
              Upon successful minting, the system automatically dispatches an email to the student containing their unique Token ID.
            </p>
          </div>

          <div className="feature-box" style={{ background: 'transparent', borderTop: '2px solid var(--accent)' }}>
            <div style={{ fontSize: '3rem', fontFamily: 'JetBrains Mono', color: 'var(--accent)', marginBottom: '1rem', opacity: 0.8 }}>03</div>
            <div className="feature-title" style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>VERIFY & SHARE</div>
            <p style={{ color: 'var(--text-muted)', lineHeight: 1.6 }}>
              Students enter their Token ID to view their cryptographic proof, and can instantly share their verified credential to X or LinkedIn.
            </p>
          </div>

        </div>
      </motion.div>
    </div>
  );
};

export default Home;
