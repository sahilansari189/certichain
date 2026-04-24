# Changelog — CertiChain LMS

All notable changes to this project are documented in this file.

---

## [1.2.0] — 2026-04-25

### 📧 Certificate Request Flow

**Changed**
- "Request Certificate" button now only sends an email — no download/redirect
- Button shows "Request Sent ✓" (green) after successful request
- Certificate email links to `https://certichain-smoky.vercel.app/` (NFT issuance platform)
- Users receive the Vercel app link via email to claim their blockchain certificate

### 📚 New Course: Web Development Bootcamp

**Added**
- **Course 3: Web Development Bootcamp** (4 modules, 9 lessons, 13 quiz questions)
  - HTML Fundamentals (3 lessons, 3 quiz questions, YouTube videos)
  - CSS Styling (3 lessons, 3 quiz questions, YouTube videos)
  - JavaScript Essentials (3 lessons, 2 quiz questions, YouTube videos)
  - Final Examination — 5 min, 5 comprehensive questions + all module questions
- YouTube video embeds in every lesson using the `video_url` field
- 9 embedded YouTube tutorials covering HTML, CSS, and JavaScript

---

## [1.1.0] — 2026-04-25

### 📝 Quiz & Examination System

**Added**
- MCQ quiz questions for every module (3–4 questions each with 4 options)
- Quizzes attached to the **last lesson** of each module
- Single **Final Examination** module per course (5 min timer)
- Final exam contains ALL module questions + dedicated final questions
- **Course 1** — 16 module quiz questions + 10 final exam questions = 26 total
- **Course 2** — 19 module quiz questions + 12 final exam questions = 31 total

### 🚫 Redis & Celery Removal

**Removed**
- Celery task queue — all email tasks now run synchronously
- Redis message broker dependency
- Removed from requirements: `celery`, `redis`, `amqp`, `billiard`, `click*`, `kombu`, `vine`, `numpy`, `prompt_toolkit`, `wcwidth`, `colorama`, `packaging`
- Removed `skillnetwork/celery.py` configuration
- Removed `CELERY_*` settings from `settings.py`
- Cleaned `skillnetwork/__init__.py` (removed celery app import)

**Changed**
- `account/tasks.py` — Plain functions (removed `@shared_task`, `self.retry`)
- `credential/tasks.py` — Plain functions
- `contact/tasks.py` — Plain functions
- All `.delay()` calls replaced with direct function calls `()`

### 🔐 Login Fix

**Fixed**
- `account/views.py` — Auto-creates `UserInfo` for users without one (e.g. superuser via CLI)
- Prevents `RelatedObjectDoesNotExist` crash on login

### 🧹 PIL/Pillow Removal

**Removed**
- Deleted `generate_qr_code_base64_with_img()` from `utilities/utils.py`
- Removed `pillow` from requirements.txt
- No PIL imports remain in the codebase

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
- Management command `seed_courses` to populate demo courses with quizzes
- **Course 1: Code Blocks — CS Fundamentals** (6 modules, 16 lessons, 26 quiz questions)
  - Excel Fundamentals (3 quiz questions)
  - Command Line Essentials (3 quiz questions)
  - Data Structures & Algorithms (4 quiz questions)
  - AI & Machine Learning Basics (3 quiz questions)
  - Blockchain Fundamentals (3 quiz questions)
  - Final Examination — 5 min, 10 comprehensive questions + all module questions
- **Course 2: Blockchain Mastery — From Zero to Web3** (7 modules, 19 lessons, 31 quiz questions)
  - Introduction to Blockchain (3 quiz questions)
  - Cryptography & Security (3 quiz questions)
  - Ethereum & EVM (3 quiz questions)
  - Solidity Programming (4 quiz questions)
  - DeFi & NFTs (3 quiz questions)
  - Building dApps (3 quiz questions)
  - Final Examination — 5 min, 12 comprehensive questions + all module questions

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

**Removed from requirements.txt**
- `mysqlclient==2.2.7` — Not needed (using SQLite)

**Changed**
- Database config simplified to SQLite only (removed MySQL conditional)
- `account/models.py` — `is_verified` default changed to `True`

---

**CertiChain** — Blockchain-Powered Learning & Certification
