# CertiChain LMS — with Blockchain NFT Certification

CertiChain is a comprehensive Django-based Learning Management System with integrated **blockchain NFT certification** powered by Ethereum (Sepolia Testnet). Students complete courses, earn verifiable on-chain credentials as ERC-721 NFTs, and share them across social platforms.

> Built with Django 5.2 · ethers.js v6 · Solidity Smart Contract · EmailJS · Sepolia Testnet

---

## 🚀 Features

### Learning Management
- **Course Management** — Catalog with modules, lessons, and video content
- **Examination System** — Excel-based question import with automated scoring
- **Progress Tracking** — Real-time lesson and module completion monitoring
- **User Management** — Email-based access control and user profiles
- **Admin Dashboard** — Complete administrative oversight
- **Badge System** — Course completion badges

### Blockchain NFT Certification
- **NFT Minting** — Issue certificates as ERC-721 tokens on Ethereum Sepolia
- **On-Chain Verification** — Verify any certificate by Token ID directly from the blockchain
- **MetaMask Integration** — Wallet-based authentication for certificate issuance
- **Email Notifications** — Automatic email to students via EmailJS when certificate is issued
- **Certificate Download** — Download verified certificate as PNG image
- **Social Sharing** — Share certificates on X (Twitter) and LinkedIn via ImgBB

---

## 🛠️ Technology Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Django 5.2 · Django REST Framework |
| **Database** | SQLite (development) |
| **Frontend** | Django Templates · Tailwind CSS (CDN) |
| **Blockchain** | ethers.js v6 (ESM) · Solidity · Sepolia Testnet |
| **Smart Contract** | ERC-721 NFT (`0x19EAb7A6Cc39f391E03FDa75bA88619b345A65cB`) |
| **Email** | EmailJS (client-side, no SMTP server required) |
| **Image Hosting** | ImgBB API (for social sharing) |
| **File Processing** | pandas · openpyxl |
| **Task Queue** | Celery + Redis |

---

## 📋 Prerequisites

- **Python 3.10+**
- **pip** (Python package manager)
- **Git**
- **MetaMask** browser extension (for NFT certificate issuance)
- **Sepolia ETH** (testnet ETH for gas fees — get free from [Sepolia Faucet](https://sepoliafaucet.com))

---

## 🔧 Installation & Setup

### Step 1 — Clone the Repository

```bash
git clone <repository-url>
cd LMS-main/lms
```

### Step 2 — Create Virtual Environment

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

> **Note:** If `mysqlclient` fails to install (you don't need MySQL), you can safely remove it from `requirements.txt` since the app uses SQLite by default.

### Step 4 — Configure Environment Variables

Create a `.env` file in the `lms/` directory (or edit the existing one):

```env
DEBUG=True
SECRET_KEY=django-insecure-your-secret-key-here
ALLOWED_HOSTS=127.0.0.1,localhost

# Database (SQLite is used by default, no config needed)
DB_NAME=skillnetwork
DB_USER=root
DB_PASSWORD=

# Email (leave empty if using EmailJS for notifications)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

# NFT CertiChain - EmailJS Config
EMAILJS_SERVICE_ID=service_r4syblj
EMAILJS_TEMPLATE_ID=template_gwsybzl
EMAILJS_PUBLIC_KEY=4bZcOmG5_layrcNks

# NFT CertiChain - ImgBB for social sharing
IMGBB_KEY=f703d6a4653a008354daf33d4dda0aef
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

Follow the prompts to set username, email, and password.

### Step 8 — Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### Step 9 — Run Development Server

```bash
python manage.py runserver
```

The application will be available at: **http://127.0.0.1:8000**

---

## 🎓 How to Use

### For Administrators / Teachers

1. **Login** at `http://127.0.0.1:8000/login/`
2. **Access Admin Panel** at `http://127.0.0.1:8000/admin/` to create courses, modules, lessons
3. **Upload Exam Questions** via Excel files (format below)
4. **Issue NFT Certificates** — Navigate to any student's completed course → Click "Issue NFT Certificate"
5. **Verify Certificates** — Use the "Blockchain Verify" page from the navigation dropdown

### For Students

1. **Register / Login** to the platform
2. **Browse Courses** and enroll
3. **Complete Lessons** and track progress on the dashboard
4. **Take Exams** — Achieve 70%+ to qualify for certification
5. **Request Certificate** — Two options appear on the Progress page:
   - **Blockchain Certificate (NFT)** — Mint an on-chain credential
   - **LMS Certificate** — Traditional PDF/image certificate
6. **Verify Certificate** — Enter Token ID on the Verify page to view and download
7. **Share** — Share verified certificates on X (Twitter) and LinkedIn

### NFT Certificate Flow

```
Student Passes Exam (70%+)
        ↓
Progress Page shows "Issue NFT Certificate" button
        ↓
Opens Mint Page with student info pre-filled
        ↓
Teacher connects MetaMask wallet
        ↓
Confirm transaction on Sepolia Testnet
        ↓
Certificate minted as ERC-721 NFT
        ↓
Student receives email notification via EmailJS
        ↓
Student verifies certificate by Token ID
        ↓
Download as PNG or Share on Social Media
```

### Excel Question Format

For importing exam questions, use this Excel format:

| Question | A | B | C | D | Answer |
|----------|---|---|---|---|--------|
| What is Python? | A language | A snake | A framework | A database | A |

---

## 📁 Project Structure

```
lms/
├── account/              # User management & authentication
├── admin_dashboard/      # Administrative interface
├── api/                  # REST API endpoints
├── base/                 # Base models and utilities
├── credential/           # Certificate & Badge management
│   ├── views.py          # Includes nft_mint & nft_verify views
│   └── urls.py           # Routes: /nft/mint/, /nft/verify/
├── course/               # Course management system
├── dashboard/            # User dashboard
├── exam/                 # Examination system
├── learning/             # Learning progress tracking
├── media/                # Uploaded files (course images, exams)
├── static/
│   └── js/
│       └── abi.json      # Smart contract ABI for blockchain interaction
├── templates/
│   ├── base/             # Base HTML templates
│   ├── components/       # Header, footer, toast components
│   ├── credential/
│   │   └── certificate/
│   │       ├── nft_mint.html     # NFT certificate issuance page
│   │       ├── nft_verify.html   # NFT certificate verification page
│   │       ├── certificates.html # Certificate listing
│   │       └── certificate_page.html
│   └── learning/
│       ├── course_dashboard_home.html
│       └── course_dashboard_progress.html  # NFT button integrated here
├── utilities/            # Helper utilities (QR codes, etc.)
├── skillnetwork/         # Django project settings
├── .env                  # Environment variables
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

---

## 🔗 Key URLs

| URL | Description |
|-----|-------------|
| `/` | Home page |
| `/login/` | User login |
| `/register/` | User registration |
| `/courses/` | Course catalog |
| `/admin/` | Django admin panel |
| `/credentials/certificates/` | My certificates |
| `/credentials/nft/mint/` | Issue NFT certificate |
| `/credentials/nft/verify/` | Verify blockchain certificate |
| `/credentials/badges/` | My badges |

---

## ⛓️ Blockchain Configuration

### Smart Contract

| Property | Value |
|----------|-------|
| **Network** | Ethereum Sepolia Testnet |
| **Contract Address** | `0x19EAb7A6Cc39f391E03FDa75bA88619b345A65cB` |
| **Token Standard** | ERC-721 (NFT) |
| **Chain ID** | 11155111 |

### MetaMask Setup

1. Install [MetaMask](https://metamask.io/) browser extension
2. Add **Sepolia Test Network** (usually available by default in test networks)
3. Get free Sepolia ETH from a faucet:
   - [sepoliafaucet.com](https://sepoliafaucet.com)
   - [Alchemy Sepolia Faucet](https://sepoliafaucet.com/)
4. Ensure MetaMask is connected to Sepolia when issuing certificates

### Third-Party Services

| Service | Purpose | Config Key |
|---------|---------|------------|
| **EmailJS** | Student email notifications | `EMAILJS_SERVICE_ID`, `EMAILJS_TEMPLATE_ID`, `EMAILJS_PUBLIC_KEY` |
| **ImgBB** | Certificate image hosting for social sharing | `IMGBB_KEY` |

> These services are configured client-side (in the browser). No server-side SMTP setup is required.

---

## 🚀 Deployment (Vercel)

### Environment Variables

Set these in your Vercel dashboard under **Settings → Environment Variables**:

```
SECRET_KEY=<your-production-secret-key>
ALLOWED_HOSTS=your-domain.vercel.app
DEBUG=False
EMAILJS_SERVICE_ID=service_r4syblj
EMAILJS_TEMPLATE_ID=template_gwsybzl
EMAILJS_PUBLIC_KEY=4bZcOmG5_layrcNks
IMGBB_KEY=f703d6a4653a008354daf33d4dda0aef
```

### Build Command

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| `mysqlclient` install fails | Remove `mysqlclient==2.2.7` from `requirements.txt` (SQLite is used) |
| MetaMask not detected | Install MetaMask extension and refresh the page |
| Transaction fails | Ensure you have Sepolia ETH and are on the Sepolia network |
| Certificate not found on verify | Confirm the Token ID exists and the transaction was confirmed |
| Static files not loading | Run `python manage.py collectstatic --noinput` |
| Email not sent | Check EmailJS service/template IDs in `.env` |

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📄 License

This project is proprietary software by CertiChain

## 📞 Support

For support and queries, contact CertiChain

---

**CertiChain LMS** — Bridging Academia and Industry Through Technology & Blockchain

