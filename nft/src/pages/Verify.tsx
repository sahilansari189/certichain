import React, { useState, useRef } from 'react';
import { ethers } from 'ethers';
import html2canvas from 'html2canvas';
import { Loader2 } from 'lucide-react';
import { motion } from 'framer-motion';

const CONTRACT_ADDRESS = "0x19EAb7A6Cc39f391E03FDa75bA88619b345A65cB";

const Verify = () => {
  const [tokenId, setTokenId] = useState('');
  const [status, setStatus] = useState<'idle' | 'loading' | 'valid' | 'invalid'>('idle');
  const [certData, setCertData] = useState<any>(null);
  const [uploadingPlatform, setUploadingPlatform] = useState<string | null>(null);
  const certificateRef = useRef<HTMLDivElement>(null);

  const downloadImage = async () => {
    if (certificateRef.current) {
      const canvas = await html2canvas(certificateRef.current, {
        backgroundColor: '#000',
        scale: 2 // High resolution
      });
      const image = canvas.toDataURL("image/png");
      const link = document.createElement('a');
      link.href = image;
      link.download = `Certificate_${tokenId}.png`;
      link.click();
    }
  };

  const uploadAndShare = async (platform: 'x' | 'linkedin') => {
    if (!certificateRef.current) return;
    
    setUploadingPlatform(platform);
    try {
      const canvas = await html2canvas(certificateRef.current, { backgroundColor: '#000', scale: 2 });
      const base64Image = canvas.toDataURL("image/png").split(',')[1];
      
      const formData = new FormData();
      formData.append("image", base64Image);
      
      // Upload to ImgBB for a free temporary public image URL
      const imgbbKey = import.meta.env.VITE_IMGBB_KEY || "YOUR_IMGBB_KEY";
      const res = await fetch(`https://api.imgbb.com/1/upload?key=${imgbbKey}`, {
        method: 'POST',
        body: formData
      });
      
      const data = await res.json();
      if (!data.success) throw new Error("Upload failed");
      
      const imageUrl = data.data.url;
      
      if (platform === 'x') {
        const text = `I just verified my credential for ${certData.courseName} on the blockchain! Check out my official certificate: ${imageUrl}`;
        window.open(`https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}`, '_blank');
      } else {
        // LinkedIn share URL
        window.open(`https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(imageUrl)}`, '_blank');
      }
    } catch (err) {
      console.error(err);
      alert("Auto-upload failed. Please click DOWNLOAD instead.");
    }
    setUploadingPlatform(null);
  };

  const handleVerify = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!tokenId) return;

    try {
      setStatus('loading');
      
      let provider;
      if ((window as any).ethereum) {
        provider = new ethers.BrowserProvider((window as any).ethereum);
      } else {
        // Fallback to public RPC if no wallet
        provider = new ethers.JsonRpcProvider("https://rpc.sepolia.org");
      }

      const ABI = await import('../abi.json').then(m => m.default);
      const contract = new ethers.Contract(CONTRACT_ADDRESS, ABI, provider);

      // We need to fetch the events or state to get the data
      // For this demo, we will query the CertificateIssued event for the tokenId
      const filter = contract.filters.CertificateIssued(BigInt(tokenId));
      const events = await contract.queryFilter(filter);

      if (events.length > 0) {
        const event = events[0] as any;
        const owner = await contract.ownerOf(tokenId);
        
        setCertData({
          tokenId: tokenId,
          studentName: event.args[1],
          courseName: event.args[2],
          issueDate: event.args[3],
          owner: owner
        });
        setStatus('valid');
      } else {
        setStatus('invalid');
      }
    } catch (err) {
      console.error(err);
      setStatus('invalid');
    }
  };

  return (
    <motion.div 
      className="main-grid"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="glass-panel">
        <h2 style={{ color: 'var(--text-main)', marginBottom: '3rem' }}>
          Verify Registry
        </h2>
        <p style={{ color: 'var(--text-muted)', marginBottom: '2rem', fontFamily: 'JetBrains Mono', fontSize: '0.9rem' }}>
          QUERY BLOCKCHAIN STATE FOR TOKEN ID
        </p>

        <form onSubmit={handleVerify}>
          <div className="input-group">
            <input 
              type="number" 
              className="input-field" 
              placeholder="e.g. 0" 
              value={tokenId}
              onChange={(e) => setTokenId(e.target.value)}
              required
            />
          </div>
          <button 
            type="submit" 
            className="btn-primary"
            disabled={status === 'loading'}
          >
            {status === 'loading' ? 'QUERYING...' : 'VERIFY_NOW'}
          </button>
        </form>
      </div>

      <div className="cert-card-preview">
        {status === 'idle' && (
          <div style={{ textAlign: 'center', color: 'var(--text-muted)', padding: '2rem 0' }}>
            <div style={{ fontFamily: 'JetBrains Mono', fontSize: '2rem', opacity: 0.5, marginBottom: '1rem' }}>{`{ ? }`}</div>
            <p style={{ fontFamily: 'JetBrains Mono', textTransform: 'uppercase' }}>Waiting for query input</p>
          </div>
        )}

        {status === 'loading' && (
          <div style={{ textAlign: 'center', padding: '2rem 0' }}>
            <Loader2 size={48} className="loader" style={{ margin: '0 auto 1rem', borderTopColor: 'var(--accent)' }} />
            <p style={{ fontFamily: 'JetBrains Mono', textTransform: 'uppercase', color: 'var(--accent)' }}>Reading node data...</p>
          </div>
        )}

        {status === 'valid' && certData && (
          <motion.div 
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
              <span className="status-badge">✓ VERIFIED AUTHENTIC</span>
              <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem', fontFamily: 'JetBrains Mono' }}>ID_#{certData.tokenId}</span>
            </div>

            {/* Visual Certificate Card */}
            <div className="certificate-visual" ref={certificateRef} style={{ padding: '4rem', margin: '2rem 0' }}>
              <div className="cert-header">CERTIFICATE OF COMPLETION</div>
              <div className="cert-title">{certData.courseName}</div>
              
              <div style={{ margin: '3rem 0' }}>
                <div className="cert-awarded-to">AWARDED TO</div>
                <div className="cert-name">{certData.studentName}</div>
              </div>

              <div className="cert-footer">
                <div>
                  <span style={{ display: 'block', marginBottom: '0.25rem', color: 'var(--text-muted)' }}>ISSUED ON</span>
                  <span style={{ color: '#fff' }}>{certData.issueDate}</span>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <span style={{ display: 'block', marginBottom: '0.25rem', color: 'var(--text-muted)' }}>VERIFIED CUSTODIAN</span>
                  <span style={{ color: 'var(--accent)' }}>{certData.owner.substring(0,6)}...{certData.owner.substring(38)}</span>
                </div>
              </div>

              <div className="cert-seal">
                SECURE<br/>ONCHAIN<br/>RECORD
              </div>
            </div>

            {/* Social Sharing Actions */}
            <div className="social-actions" style={{ flexDirection: 'column', alignItems: 'center' }}>
              <button 
                onClick={downloadImage}
                className="btn-primary"
                style={{ width: '100%', maxWidth: '400px', justifyContent: 'center' }}
                disabled={!!uploadingPlatform}
              >
                [ ↓ ] DOWNLOAD CERTIFICATE AS PNG
              </button>
              <div style={{ display: 'flex', gap: '1rem', width: '100%', maxWidth: '400px' }}>
                <button 
                  onClick={() => uploadAndShare('x')}
                  className="btn-social"
                  style={{ flex: 1, justifyContent: 'center' }}
                  disabled={!!uploadingPlatform}
                >
                  {uploadingPlatform === 'x' ? <Loader2 className="loader" size={16} /> : '[ X ] SHARE'}
                </button>
                <button 
                  onClick={() => uploadAndShare('linkedin')}
                  className="btn-social"
                  style={{ flex: 1, justifyContent: 'center' }}
                  disabled={!!uploadingPlatform}
                >
                  {uploadingPlatform === 'linkedin' ? <Loader2 className="loader" size={16} /> : '[ IN ] SHARE'}
                </button>
              </div>
            </div>
            
          </motion.div>
        )}

        {status === 'invalid' && (
          <motion.div 
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            style={{ textAlign: 'center' }}
          >
            <div style={{ fontFamily: 'JetBrains Mono', color: '#ff3333', fontSize: '3rem', marginBottom: '1rem' }}>{`{ ✗ }`}</div>
            <h3 style={{ marginBottom: '1rem', textTransform: 'uppercase', fontSize: '1.5rem' }}>RECORD NOT FOUND</h3>
            <p style={{ color: 'var(--text-muted)', marginBottom: '2rem' }}>
              No valid registry entry exists for this ID on the Sepolia chain.
            </p>
            <div>
              <span className="status-badge invalid">✗ UNVERIFIED</span>
            </div>
          </motion.div>
        )}
      </div>
    </motion.div>
  );
};

export default Verify;
