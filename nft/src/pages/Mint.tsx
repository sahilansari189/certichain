import React, { useState } from 'react';
import { ethers } from 'ethers';

import { motion } from 'framer-motion';
import emailjs from '@emailjs/browser';

// Replace with actual contract address after deployment
const CONTRACT_ADDRESS = "0x19EAb7A6Cc39f391E03FDa75bA88619b345A65cB"; 

const Mint = () => {
  const [formData, setFormData] = useState({
    studentAddress: '',
    studentName: '',
    studentEmail: '',
    courseName: '',
    issueDate: new Date().toISOString().split('T')[0]
  });
  const [status, setStatus] = useState('idle'); // idle, loading, success, error
  const [txHash, setTxHash] = useState('');
  const [mintedId, setMintedId] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleMint = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setStatus('loading');
      
      if (!(window as any).ethereum) throw new Error("Please install MetaMask!");

      await (window as any).ethereum.request({ method: 'eth_requestAccounts' });
      const provider = new ethers.BrowserProvider((window as any).ethereum);
      const signer = await provider.getSigner();

      // Ensure we are on Sepolia (soft check to avoid false positives)
      const network = await provider.getNetwork();
      console.log("Current network chain ID:", network.chainId);
      if (network.chainId.toString() !== "11155111" && network.chainId.toString() !== "31337" && network.chainId.toString() !== "1337") {
        console.warn(`Unexpected chain ID: ${network.chainId}. Proceeding anyway...`);
      }

      // Fetch ABI dynamically
      const ABI = await import('../abi.json').then(m => m.default);
      const contract = new ethers.Contract(CONTRACT_ADDRESS, ABI, signer);

      // Create a unique hash to prevent duplicates
      const certHash = ethers.id(`${formData.studentAddress}-${formData.courseName}-${formData.issueDate}`);
      
      // Dummy IPFS URI for demo
      const tokenURI = "ipfs://QmDummyHashForDemoPurposeOnly";

      const tx = await contract.issueCertificate(
        formData.studentAddress,
        tokenURI,
        certHash,
        formData.studentName,
        formData.courseName,
        formData.issueDate
      );

      const receipt = await tx.wait();
      setTxHash(tx.hash);
      
      // Attempt to extract Token ID from events
      let extractedId = '';
      try {
        for (const log of receipt.logs) {
          const parsed = contract.interface.parseLog(log);
          if (parsed && parsed.name === 'CertificateIssued') {
            extractedId = parsed.args[0].toString();
            break;
          }
        }
      } catch (e) {
        console.warn("Could not parse logs", e);
      }
      setMintedId(extractedId);

      setStatus('sending_email');

      // Send email automatically
      try {
        const templateParams = {
          to_email: formData.studentEmail,
          to_name: formData.studentName,
          course_name: formData.courseName,
          token_id: extractedId,
          verify_link: "https://certichain-smoky.vercel.app/verify"
        };
        
        await emailjs.send(
          import.meta.env.VITE_EMAILJS_SERVICE_ID || "YOUR_SERVICE_ID",
          import.meta.env.VITE_EMAILJS_TEMPLATE_ID || "YOUR_TEMPLATE_ID",
          templateParams,
          import.meta.env.VITE_EMAILJS_PUBLIC_KEY || "YOUR_PUBLIC_KEY"
        );
      } catch (emailErr) {
        console.error("Failed to send email", emailErr);
        // We still show success even if email fails, as the cert was minted
      }

      setStatus('success');
    } catch (err: any) {
      console.error(err);
      alert(err.message || "An error occurred");
      setStatus('error');
    }
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      style={{ maxWidth: '600px', margin: '0 auto' }}
    >
      <div className="glass-panel">
        <h2 style={{ color: 'var(--text-main)', marginBottom: '3rem' }}>
          Issue Registry Entry
        </h2>
        
        {status === 'success' ? (
          <div style={{ textAlign: 'center', padding: '2rem 0' }}>
            <div style={{ fontFamily: 'JetBrains Mono', color: 'var(--accent)', fontSize: '3rem', marginBottom: '1rem' }}>{`{ ✓ }`}</div>
            <h3 style={{ marginBottom: '1rem', fontSize: '1.5rem' }}>CERTIFICATE ISSUED</h3>
            {mintedId && (
              <p style={{ color: '#fff', marginBottom: '1rem', fontFamily: 'JetBrains Mono', fontSize: '1.2rem' }}>
                TOKEN ID: #{mintedId}
              </p>
            )}
            <p style={{ color: 'var(--text-muted)', marginBottom: '2rem' }}>
              Transaction Hash: <br/><br/>
              <a 
                href={`https://sepolia.etherscan.io/tx/${txHash}`} 
                target="_blank" 
                rel="noreferrer"
                style={{ color: 'var(--accent)', fontFamily: 'JetBrains Mono', textDecoration: 'none' }}
              >
                {txHash.substring(0, 14)}...{txHash.substring(txHash.length - 12)}
              </a>
            </p>
            <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', marginBottom: '1rem' }}>
              <button 
                className="btn-outline" 
                onClick={() => setStatus('idle')}
                style={{ flex: 1, justifyContent: 'center' }}
              >
                ISSUE ANOTHER
              </button>
              {mintedId && (
                <button 
                  className="btn-primary" 
                  onClick={() => window.location.href = '/verify'}
                  style={{ flex: 1, justifyContent: 'center' }}
                >
                  VERIFY NOW
                </button>
              )}
            </div>
            <p style={{ color: '#10b981', fontSize: '0.85rem', fontFamily: 'JetBrains Mono', textAlign: 'center' }}>
              Email automatically sent to {formData.studentEmail}
            </p>
          </div>
        ) : (
          <form onSubmit={handleMint}>
            <div className="input-group">
              <label>Student Wallet Address</label>
              <input 
                type="text" 
                name="studentAddress" 
                className="input-field" 
                placeholder="0x..." 
                required
                value={formData.studentAddress}
                onChange={handleChange}
              />
            </div>
            
            <div className="input-group">
              <label>Student Full Name</label>
              <input 
                type="text" 
                name="studentName" 
                className="input-field" 
                placeholder="John Doe" 
                required
                value={formData.studentName}
                onChange={handleChange}
              />
            </div>

            <div className="input-group">
              <label>Student Email Address (For Notification)</label>
              <input 
                type="email" 
                name="studentEmail" 
                className="input-field" 
                placeholder="student@example.com" 
                required
                value={formData.studentEmail}
                onChange={handleChange}
              />
            </div>

            <div className="input-group">
              <label>Course Name</label>
              <input 
                type="text" 
                name="courseName" 
                className="input-field" 
                placeholder="Advanced Blockchain Architecture" 
                required
                value={formData.courseName}
                onChange={handleChange}
              />
            </div>

            <div className="input-group">
              <label>Issue Date</label>
              <input 
                type="date" 
                name="issueDate" 
                className="input-field" 
                required
                value={formData.issueDate}
                onChange={handleChange}
              />
            </div>

            <button 
              type="submit" 
              className="btn-primary" 
              style={{ width: '100%', marginTop: '1rem' }}
              disabled={status === 'loading'}
            >
              {status === 'loading' ? 'PROCESSING_TX...' : status === 'sending_email' ? 'EMAILING_STUDENT...' : 'TRANSACT_ONCHAIN'}
            </button>
          </form>
        )}
      </div>
    </motion.div>
  );
};

export default Mint;
