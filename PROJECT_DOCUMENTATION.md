# CertiChain — Project Documentation

> **Hackathon Submission — 24th & 25th April 2026**

CertiChain is a two-part system that combines a Learning Management System (LMS) with Blockchain-based NFT Certification. Students complete courses on the LMS, pass examinations, and receive verifiable on-chain ERC-721 NFT certificates on the Ethereum Sepolia Testnet.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Repository Structure](#repository-structure)
4. [Technology Stack](#technology-stack)
5. [Prerequisites](#prerequisites)
6. [Repo 1 — LMS Setup (Django)](#repo-1--lms-setup-django)
7. [Repo 2 — NFT Certification Frontend (React + Vite)](#repo-2--nft-certification-frontend-react--vite)
8. [Environment Variables](#environment-variables)
9. [MetaMask Wallet Setup](#metamask-wallet-setup)
10. [User Accounts & Roles](#user-accounts--roles)
11. [End-to-End Flow](#end-to-end-flow)
12. [Testing Checklist](#testing-checklist)
13. [Key URLs Reference](#key-urls-reference)
14. [Troubleshooting](#troubleshooting)

---

## Project Overview

CertiChain bridges the gap between traditional e-learning and blockchain-verified credentials. The platform consists of two interconnected repositories:

**Repo 1 — LMS (Learning Management System)**
A Django-based platform where teachers create courses with modules, lessons, and video content. Students enroll, complete lessons, watch videos, and take exams. Upon passing with ≥ 75%, students can request a blockchain-verified NFT certificate.

**Repo 2 — NFT Certification Frontend**
A React + Vite application deployed on Vercel that handles the blockchain side — issuing ERC-721 NFT certificates on the Ethereum Sepolia Testnet via MetaMask, verifying certificates by Token ID, sending email confirmations, and enabling certificate download and social sharing.

### How They Connect

When a student completes a course on the LMS and passes the exam, they click "Request Certificate." This sends an email to the student containing a link to the NFT Certification Frontend (hosted on Vercel). The Super Admin / Teacher then uses the NFT Frontend to:
1. Enter the student's wallet address and details
2. Connect MetaMask and issue the certificate on-chain
3. The student automatically receives an email with a verification link and Token ID
4. The student can verify, download, and share the certificate

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CertiChain System                        │
├─────────────────────────────┬───────────────────────────────────┤
│     Repo 1: LMS (Django)    │   Repo 2: NFT Frontend (React)   │
│                             │                                   │
│  ┌───────────────────────┐  │  ┌─────────────────────────────┐  │
│  │  Course Management    │  │  │  Issue Certificate (Mint)   │  │
│  │  Module / Lessons     │  │  │  MetaMask → Sepolia Tx      │  │
│  │  Video Content        │  │  │  ERC-721 NFT Minting        │  │
│  │  Exam System          │  │  └─────────────────────────────┘  │
│  │  Progress Tracking    │  │  ┌─────────────────────────────┐  │
│  │  Certificate Request  │──┼─▶│  Verify Certificate         │  │
│  │  Admin Dashboard      │  │  │  On-Chain Lookup             │  │
│  └───────────────────────┘  │  │  Download / Social Share     │  │
│                             │  └─────────────────────────────┘  │
│  Backend: Django 5.2        │  Frontend: React 19 + Vite 8     │
│  Database: SQLite           │  Blockchain: ethers.js v6        │
│  Templates: Django + TW CSS │  Email: EmailJS                  │
│  Server: localhost:8000     │  Deployed: Vercel                │
└─────────────────────────────┴───────────────────────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │  Ethereum Sepolia  │
                    │  Smart Contract    │
                    │  ERC-721 NFT       │
                    │  Chain ID: 11155111│
                    └───────────────────┘
```

---

## Repository Structure

```
certichain/
├── lms/                          ← Repo 1: Django LMS
│   ├── account/                  # User management & authentication
│   ├── admin_dashboard/          # Administrative interface
│   ├── api/                      # REST API endpoints
│   ├── base/                     # Base models and utilities
│   ├── contact/                  # Contact form
│   ├── course/                   # Course management (models, views)
│   ├── credential/               # Certificate & Badge management
│   │   ├── views.py              # Includes nft_mint & nft_verify views
│   │   └── urls.py               # Routes: /nft/mint/, /nft/verify/
│   ├── dashboard/                # User dashboard
│   ├── exam/                     # Examination system (Excel import, scoring)
│   ├── learning/                 # Learning progress tracking
│   ├── static/                   # Static assets (CSS, JS, abi.json)
│   ├── templates/                # Django HTML templates
│   ├── utilities/                # Helper utilities (QR codes, etc.)
│   ├── skillnetwork/             # Django project settings
│   ├── manage.py                 # Django management script
│   ├── requirements.txt          # Python dependencies
│   └── .env                      # Environment variables (create this)
│
└── nft/                          ← Repo 2: React NFT Frontend
    ├── api/                      # Serverless API (share.js)
    ├── src/
    │   ├── pages/
    │   │   ├── Home.tsx           # Landing page
    │   │   ├── Mint.tsx           # Issue NFT certificate page
    │   │   └── Verify.tsx         # Verify certificate page
    │   ├── App.tsx                # Router & layout
    │   ├── abi.json               # Smart contract ABI
    │   ├── index.css              # Global styles
    │   └── main.tsx               # Entry point
    ├── package.json               # Node dependencies
    ├── vercel.json                # Vercel deployment config
    ├── vite.config.ts             # Vite configuration
    └── .env                       # Environment variables (create this)
```

---

## Technology Stack

| Component | Technology |
|-----------|-----------|
| **LMS Backend** | Django 5.2 · Django REST Framework |
| **LMS Database** | SQLite (development) |
| **LMS Frontend** | Django Templates · Tailwind CSS (CDN) |
| **NFT Frontend** | React 19 · TypeScript · Vite 8 |
| **Blockchain** | ethers.js v6 · Solidity · Ethereum Sepolia Testnet |
| **Smart Contract** | ERC-721 NFT (`0x19EAb7A6Cc39f391E03FDa75bA88619b345A65cB`) |
| **Email Notifications** | EmailJS (client-side, no SMTP server required) |
| **Image Hosting** | ImgBB API (for social sharing of certificates) |
| **File Processing** | pandas · openpyxl (Excel question import) |
| **Animations** | Framer Motion |
| **Icons** | Lucide React |
| **Certificate Export** | html2canvas (PNG download) |
| **Deployment** | Vercel (NFT Frontend) · PythonAnywhere / Local (LMS) |

---

## Prerequisites

Before setting up the project, ensure you have the following installed:

- **Python 3.10+** — [Download](https://www.python.org/downloads/)
- **pip** — Python package manager (comes with Python)
- **Node.js 18+** and **npm** — [Download](https://nodejs.org/)
- **Git** — [Download](https://git-scm.com/)
- **MetaMask** browser extension — [Install](https://metamask.io/)
- **Sepolia ETH** — Free testnet ETH for gas fees (see [MetaMask Setup](#metamask-wallet-setup))
- **A valid email address** — Required for testing certificate email notifications

---

## Repo 1 — LMS Setup (Django)

### Step 1 — Clone the Repository

```bash
git clone https://github.com/sahilansari189/certichain.git
cd certichain/lms
```

### Step 2 — Create a Virtual Environment

```bash
python -m venv env

# Windows
env\Scripts\activate

# macOS / Linux
source env/bin/activate
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

> **Note:** If `mysqlclient` fails to install, remove it from `requirements.txt` — the app uses SQLite by default.

### Step 4 — Configure Environment Variables

Create a `.env` file inside the `lms/` directory:

```env
# ──────────────────────────────────────────────
#  LMS .env — FILL IN YOUR VALUES BELOW
# ──────────────────────────────────────────────

DEBUG=True
SECRET_KEY=<YOUR_DJANGO_SECRET_KEY>
ALLOWED_HOSTS=127.0.0.1,localhost

# Database (SQLite is default — no config needed)
DB_NAME=skillnetwork
DB_USER=root
DB_PASSWORD=

# Email Backend (leave empty if using EmailJS)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

# NFT CertiChain — EmailJS Config
EMAILJS_SERVICE_ID=<YOUR_EMAILJS_SERVICE_ID>
EMAILJS_TEMPLATE_ID=<YOUR_EMAILJS_TEMPLATE_ID>
EMAILJS_PUBLIC_KEY=<YOUR_EMAILJS_PUBLIC_KEY>

# NFT CertiChain — ImgBB for social sharing
IMGBB_KEY=<YOUR_IMGBB_KEY>
```

### Step 5 — Create Required Directories

```bash
# Windows
mkdir media\course_images
mkdir media\exam_file
mkdir logs

# macOS / Linux
mkdir -p media/course_images media/exam_file logs
```

### Step 6 — Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 7 — Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts — enter a **username**, **email**, and **password**. This account will be used to:
- Access the Django Admin Panel (`/admin/`)
- Manage courses, users, and certificates
- Issue NFT certificates to students

### Step 8 — Seed Sample Courses

```bash
python manage.py seed_courses
```

This creates three demo courses:
1. **Code Blocks — CS Fundamentals** (6 modules, 16 lessons, 26 quiz questions)
2. **Blockchain Mastery — From Zero to Web3** (7 modules, 19 lessons, 31 quiz questions)
3. **Web Development Bootcamp** (4 modules, 9 lessons, 13 quiz questions)

### Step 9 — Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### Step 10 — Run the Development Server

```bash
python manage.py runserver
```

The LMS is now available at: **http://127.0.0.1:8000**

---

## Repo 2 — NFT Certification Frontend (React + Vite)

### Step 1 — Navigate to the NFT Directory

```bash
cd certichain/nft
```

### Step 2 — Install Dependencies

```bash
npm install
```

### Step 3 — Configure Environment Variables

Create or edit the `.env` file inside the `nft/` directory:

```env
# ──────────────────────────────────────────────
#  NFT Frontend .env — FILL IN YOUR VALUES BELOW
# ──────────────────────────────────────────────

VITE_EMAILJS_SERVICE_ID="<YOUR_EMAILJS_SERVICE_ID>"
VITE_EMAILJS_TEMPLATE_ID="<YOUR_EMAILJS_TEMPLATE_ID>"
VITE_EMAILJS_PUBLIC_KEY="<YOUR_EMAILJS_PUBLIC_KEY>"
VITE_IMGBB_KEY="<YOUR_IMGBB_KEY>"
```

### Step 4 — Run the Development Server

```bash
npm run dev
```

The NFT Frontend is now available at: **http://localhost:5173**

### Step 5 — Build for Production (Optional)

```bash
npm run build
```

The production build is output to `dist/` and can be deployed to Vercel.

**Live Deployment:** `https://certichain-smoky.vercel.app/`

---

## Environment Variables

Both repos require `.env` files. Below is a summary of all required variables. **Fill in your own values.**

### LMS `.env` (at `certichain/lms/.env`)

```env
# ──────────────────────────────────────────────
#  REPLACE ALL <PLACEHOLDER> VALUES WITH YOUR OWN
# ──────────────────────────────────────────────

DEBUG=True
SECRET_KEY=<YOUR_DJANGO_SECRET_KEY>
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=skillnetwork
DB_USER=root
DB_PASSWORD=

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

EMAILJS_SERVICE_ID=<YOUR_EMAILJS_SERVICE_ID>
EMAILJS_TEMPLATE_ID=<YOUR_EMAILJS_TEMPLATE_ID>
EMAILJS_PUBLIC_KEY=<YOUR_EMAILJS_PUBLIC_KEY>
IMGBB_KEY=<YOUR_IMGBB_KEY>
```

### NFT Frontend `.env` (at `certichain/nft/.env`)

```env
# ──────────────────────────────────────────────
#  REPLACE ALL <PLACEHOLDER> VALUES WITH YOUR OWN
# ──────────────────────────────────────────────

VITE_EMAILJS_SERVICE_ID="<YOUR_EMAILJS_SERVICE_ID>"
VITE_EMAILJS_TEMPLATE_ID="<YOUR_EMAILJS_TEMPLATE_ID>"
VITE_EMAILJS_PUBLIC_KEY="<YOUR_EMAILJS_PUBLIC_KEY>"
VITE_IMGBB_KEY="<YOUR_IMGBB_KEY>"
```

> **You will add your actual keys here.** Space has been left for you to fill in.

---

## MetaMask Wallet Setup

MetaMask is required to issue (mint) NFT certificates on the Ethereum Sepolia Testnet.

### Step 1 — Install MetaMask

1. Go to [https://metamask.io/](https://metamask.io/)
2. Install the browser extension (Chrome / Firefox / Brave / Edge)
3. Create a new wallet or import an existing one
4. **Save your seed phrase securely** — you will need it for recovery

### Step 2 — Switch to Sepolia Test Network

1. Open MetaMask → Click the network dropdown (top-left)
2. Toggle **"Show test networks"** ON (in Settings → Advanced)
3. Select **Sepolia Test Network**
4. Your wallet should now display on the Sepolia network

### Step 3 — Get Free Sepolia ETH

You need Sepolia ETH (testnet ETH) to pay gas fees when minting NFT certificates.

| Faucet | URL |
|--------|-----|
| Sepolia Faucet | [https://sepoliafaucet.com](https://sepoliafaucet.com) |
| Alchemy Faucet | [https://sepoliafaucet.com](https://sepoliafaucet.com) |
| Google Cloud Faucet | [https://cloud.google.com/application/web3/faucet/ethereum/sepolia](https://cloud.google.com/application/web3/faucet/ethereum/sepolia) |

1. Copy your MetaMask wallet address
2. Paste it into any faucet above
3. Request test ETH (usually 0.5 ETH per request)
4. Wait for the transaction to confirm (1–2 minutes)

### Step 4 — Smart Contract Details

| Property | Value |
|----------|-------|
| **Network** | Ethereum Sepolia Testnet |
| **Contract Address** | `0x19EAb7A6Cc39f391E03FDa75bA88619b345A65cB` |
| **Token Standard** | ERC-721 (NFT) |
| **Chain ID** | 11155111 |
| **Explorer** | [View on Etherscan](https://sepolia.etherscan.io/address/0x19EAb7A6Cc39f391E03FDa75bA88619b345A65cB) |

---

## User Accounts & Roles

### Role 1 — Super Admin / Teacher

- Created via `python manage.py createsuperuser`
- Has access to the Django Admin Panel at `/admin/`
- Can create / edit / delete courses, modules, lessons
- Can manage student enrollments and allow access to courses
- Can issue NFT certificates via the NFT Frontend (requires MetaMask)
- Receives certificate request notifications

### Role 2 — Student

- Registers via the LMS registration page at `/register/`
- Can browse and enroll in courses (after admin approval)
- Completes lessons, watches videos, and tracks progress
- Takes exams and must score ≥ 75% to request a certificate
- Receives email confirmation with certificate verification link and Token ID

### Creating Test Accounts

**Super Admin / Teacher:**
```bash
cd certichain/lms
python manage.py createsuperuser

# Enter:
#   Username: admin
#   Email: admin@certichain.io  (use a real email for testing)
#   Password: <your_password>
```

**Student Account:**
1. Open **http://127.0.0.1:8000/register/**
2. Fill in name, email (use a **valid email** — certificate notifications go here), and password
3. Log in at **http://127.0.0.1:8000/login/**

> **Important:** All email IDs must be valid and accessible. Certificate notifications, verification links, and Token IDs are sent to the student's email address. Invalid emails will result in failed notifications.

---

## End-to-End Flow

### Phase 1 — LMS Course Completion

```
1. Super Admin creates superuser account
        ↓
2. Super Admin logs into Django Admin (/admin/)
        ↓
3. Super Admin runs `python manage.py seed_courses` to create sample courses
        ↓
4. Super Admin allows/assigns courses to students from the Admin Panel
        ↓
5. Student registers and logs in to the LMS
        ↓
6. Student enrolls in an available course
        ↓
7. Student completes all modules, watches all videos
        ↓
8. Student takes the Final Examination
        ↓
9. Student scores ≥ 75% → "Request Certificate" button appears
        ↓
10. Student clicks "Request Certificate"
        ↓
11. Student receives an email with a link to the NFT Certification Platform
```

### Phase 2 — Blockchain NFT Certificate Issuance

```
12. Super Admin opens the NFT Frontend (https://certichain-smoky.vercel.app/ or localhost:5173)
        ↓
13. Super Admin navigates to "Issue Certificate" (/mint)
        ↓
14. Super Admin enters:
    - Student's Ethereum wallet address
    - Student's full name
    - Student's email address
    - Course name
    - Issue date
        ↓
15. Super Admin connects MetaMask (must be on Sepolia network)
        ↓
16. Super Admin confirms the transaction in MetaMask
        ↓
17. Certificate is minted as an ERC-721 NFT on Ethereum Sepolia
        ↓
18. Student receives an email automatically via EmailJS containing:
    - Confirmation of certificate issuance
    - Token ID
    - Verification link (https://certichain-smoky.vercel.app/verify)
        ↓
19. Student opens the verification link
        ↓
20. Student enters their Token ID on the Verify page
        ↓
21. Certificate data is fetched from the blockchain and displayed
        ↓
22. Student can:
    - Download certificate as PNG
    - Share on X (Twitter)
    - Share on LinkedIn
```

---

## Testing Checklist

Use this checklist to verify all components are working:

### LMS (Repo 1)

- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created with valid keys
- [ ] Database migrations run successfully
- [ ] Superuser account created
- [ ] Sample courses seeded (`python manage.py seed_courses`)
- [ ] Server starts without errors (`python manage.py runserver`)
- [ ] Admin panel accessible at `/admin/`
- [ ] Student registration works at `/register/`
- [ ] Student login works at `/login/`
- [ ] Courses visible in course catalog
- [ ] Student can enroll in a course (after admin allows it)
- [ ] Lessons and videos load correctly
- [ ] Progress tracking updates as lessons are completed
- [ ] Exam system works with quiz questions
- [ ] Scoring calculates correctly (need ≥ 75%)
- [ ] "Request Certificate" button appears after passing
- [ ] Certificate request email is sent successfully

### NFT Frontend (Repo 2)

- [ ] Dependencies installed (`npm install`)
- [ ] `.env` file created with valid EmailJS and ImgBB keys
- [ ] Dev server starts (`npm run dev`)
- [ ] Home page loads at `http://localhost:5173`
- [ ] "Issue Certificate" page loads at `/mint`
- [ ] "Verify" page loads at `/verify`
- [ ] MetaMask connects successfully
- [ ] MetaMask is on Sepolia network
- [ ] Wallet has sufficient Sepolia ETH for gas
- [ ] Certificate minting transaction completes
- [ ] Token ID is extracted from transaction receipt
- [ ] Email notification sent to student via EmailJS
- [ ] Certificate verification works with Token ID
- [ ] Certificate data displays correctly (name, course, date, owner)
- [ ] Certificate download as PNG works
- [ ] Social sharing (X / LinkedIn) works

### Email Validation

- [ ] All test accounts use valid, accessible email addresses
- [ ] Certificate request email from LMS is received
- [ ] Certificate issuance email from NFT Frontend is received
- [ ] Verification link in email works correctly
- [ ] Token ID in email matches the minted NFT

---

## Key URLs Reference

### LMS (Local — http://127.0.0.1:8000)

| URL | Description |
|-----|-------------|
| `/` | Home page |
| `/login/` | Student / Admin login |
| `/register/` | Student registration |
| `/courses/` | Course catalog |
| `/admin/` | Django Admin Panel |
| `/credentials/certificates/` | My certificates |
| `/credentials/nft/mint/` | Issue NFT certificate (LMS-integrated) |
| `/credentials/nft/verify/` | Verify blockchain certificate (LMS-integrated) |
| `/credentials/badges/` | My badges |

### NFT Frontend (Vercel — https://certichain-smoky.vercel.app)

| URL | Description |
|-----|-------------|
| `/` | Landing page |
| `/mint` | Issue NFT certificate (MetaMask required) |
| `/verify` | Verify certificate by Token ID |

### Blockchain Explorer

| Resource | URL |
|----------|-----|
| Smart Contract | [Etherscan](https://sepolia.etherscan.io/address/0x19EAb7A6Cc39f391E03FDa75bA88619b345A65cB) |
| Transaction Lookup | `https://sepolia.etherscan.io/tx/<TX_HASH>` |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `mysqlclient` install fails | Remove `mysqlclient` from `requirements.txt` — SQLite is used by default |
| MetaMask not detected | Install MetaMask extension and refresh the page |
| "Wrong network" error | Switch MetaMask to Sepolia Test Network |
| Transaction fails | Ensure you have Sepolia ETH and are on the correct network |
| Certificate not found on verify | Confirm the Token ID exists and the transaction was confirmed on-chain |
| Static files not loading | Run `python manage.py collectstatic --noinput` |
| Email not sent | Check EmailJS service/template IDs in `.env` |
| Student can't enroll | Admin must allow/assign the course from the Admin Panel first |
| Exam score not showing | Complete all lessons in the module before attempting the exam |
| Seed command fails | Ensure migrations are run first (`python manage.py migrate`) |
| NFT Frontend build fails | Ensure Node.js 18+ is installed and run `npm install` first |
| `VITE_` env vars not loading | Restart the Vite dev server after changing `.env` |

---

## Third-Party Services

| Service | Purpose | Setup |
|---------|---------|-------|
| **EmailJS** | Client-side email (no SMTP server needed) | [https://www.emailjs.com/](https://www.emailjs.com/) — Create account, set up service & template |
| **ImgBB** | Free image hosting for social sharing | [https://api.imgbb.com/](https://api.imgbb.com/) — Get API key |
| **MetaMask** | Ethereum wallet for signing transactions | [https://metamask.io/](https://metamask.io/) — Browser extension |
| **Sepolia Faucet** | Free testnet ETH | [https://sepoliafaucet.com](https://sepoliafaucet.com) |

---

**CertiChain** — Bridging Academia and Industry Through Technology & Blockchain
