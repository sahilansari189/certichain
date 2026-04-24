# Changelog — CertiChain LMS

All notable changes to this project are documented in this file.

---

## [1.0.0] — 2026-04-25

### 🔗 NFT Blockchain Certification Integration

**Added**
- Integrated blockchain-based NFT certification system directly into the Django LMS
- New template `nft_mint.html` — Issue ERC-721 certificates on Ethereum Sepolia testnet via MetaMask
- New template `nft_verify.html` — Verify any certificate by Token ID with on-chain lookup
- New views `nft_mint` and `nft_verify` in `credential/views.py`
- New URL routes: `/credentials/nft/mint/` and `/credentials/nft/verify/`
- Smart contract ABI file at `static/js/abi.json`
- "Issue NFT Certificate" button on course progress page (appears when grade ≥ 70%)
- "Verify on Blockchain" button on certificate detail and listing pages
- "Blockchain Verify" link added to user dropdown menu in header
- EmailJS integration for automatic student email notifications on mint
- ImgBB integration for certificate image upload and social sharing (X, LinkedIn)
- Certificate download as PNG via html2canvas

**Environment Variables Added**
- `EMAILJS_SERVICE_ID` — EmailJS service identifier
- `EMAILJS_TEMPLATE_ID` — EmailJS template identifier
- `EMAILJS_PUBLIC_KEY` — EmailJS public key
- `IMGBB_KEY` — ImgBB API key for image hosting

---

### 📚 Course Content

**Added**
- Management command `seed_courses` to populate demo courses
- **Course 1: Code Blocks — CS Fundamentals** (6 modules, 16 lessons)
  - Excel Fundamentals
  - Command Line Essentials
  - Data Structures & Algorithms
  - AI & Machine Learning Basics
  - Blockchain Fundamentals
  - Final Examination
- **Course 2: Blockchain Mastery — From Zero to Web3** (7 modules, 19 lessons)
  - Introduction to Blockchain
  - Cryptography & Security
  - Ethereum & EVM
  - Solidity Programming
  - DeFi & NFTs
  - Building dApps
  - Final Examination

---

### 🎨 Rebranding — ASPL SkillVerse → CertiChain

**Changed**
- All user-visible text replaced: "ASPL SkillVerse" → "CertiChain"
- Header logo replaced with CertiChain logo (`certichain_logo.png`)
- Footer branding updated to "CertiChain"
- Page title: "CertiChain - Blockchain-Powered Learning & Certification"
- Login, register, forgot password pages rebranded
- Email templates (verification, enrollment) rebranded
- Certificate templates (cert_v1, cert_v2, cert_v3) rebranded
- Contact page email updated to `support@certichain.io`
- FAQ and overview pages rebranded
- Admin dashboard title rebranded
- Python backend references updated (signals, tasks, management commands)
- README.md fully rewritten for CertiChain

---

### 🛠️ Deployment & Compatibility Fixes

**Fixed**
- Removed top-level `import pandas` from `exam/models.py` (unused import causing numpy crash)
- Moved `import pandas` to lazy import inside `account/models.py` → `create_allowed_emails()`
- Removed `generate_qr_code_base64_with_img()` function (used PIL, was never called)
- Removed all PIL/Pillow usage from the codebase

**Removed from requirements.txt**
- `mysqlclient==2.2.7` — Not needed (using SQLite)
- `pillow==11.3.0` — Not needed (PIL removed from codebase)
- `pandas==2.3.2` — Now lazy-imported only when needed
- `numpy==2.3.3` — Only needed by pandas, not required at install time

**Changed**
- Database config simplified to SQLite only (removed MySQL conditional)
- `account/models.py` — `is_verified` default changed to `True`

---

### 📁 Files Created

| File | Purpose |
|------|---------|
| `templates/credential/certificate/nft_mint.html` | NFT certificate issuance page |
| `templates/credential/certificate/nft_verify.html` | NFT certificate verification page |
| `static/js/abi.json` | Smart contract ABI |
| `static/images/certichain_logo.png` | CertiChain logo |
| `course/management/commands/seed_courses.py` | Course seeding command |
| `CHANGELOG.md` | This file |

### 📁 Files Modified

| File | Changes |
|------|---------|
| `.env` | Added EmailJS and ImgBB keys |
| `skillnetwork/settings.py` | Added NFT config vars, simplified DB to SQLite |
| `credential/views.py` | Added `nft_mint` and `nft_verify` views |
| `credential/urls.py` | Added NFT routes |
| `requirements.txt` | Removed mysqlclient, pillow, pandas, numpy |
| `utilities/utils.py` | Removed PIL-dependent function |
| `exam/models.py` | Removed unused pandas import |
| `account/models.py` | Lazy pandas import, `is_verified=True` |
| `templates/components/header.html` | CertiChain logo + Blockchain Verify link |
| `templates/components/footer.html` | CertiChain branding |
| `templates/base/base.html` | CertiChain title |
| `templates/learning/course_dashboard_progress.html` | NFT certificate section |
| `templates/credential/certificate/certificates.html` | Blockchain links |
| `templates/credential/certificate/certificate_page.html` | Verify button |
| `templates/auth/login.html` | CertiChain branding |
| `templates/auth/register.html` | CertiChain branding |
| `templates/auth/forgot_password.html` | CertiChain branding |
| `templates/base/home.html` | CertiChain branding |
| `README.md` | Full rewrite for CertiChain |

---

**CertiChain** — Blockchain-Powered Learning & Certification
