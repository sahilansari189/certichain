from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from course.models import Course, Module, Lesson, Skill, DifficultyLevel, Language, OfferedBy, Industry

class Command(BaseCommand):
    help = 'Seed two demo courses with modules and lessons'

    def handle(self, *args, **kwargs):
        instructor, _ = User.objects.get_or_create(
            username='certichain_admin',
            defaults={'first_name': 'CertiChain', 'last_name': 'Admin', 'email': 'admin@certichain.io', 'is_staff': True}
        )

        org, _ = OfferedBy.objects.get_or_create(organization_name='CertiChain', defaults={'description': 'Blockchain-powered learning platform', 'website': 'https://certichain.io'})
        lang, _ = Language.objects.get_or_create(name='English', defaults={'code': 'en'})
        ind_tech, _ = Industry.objects.get_or_create(name='Technology')
        ind_bc, _ = Industry.objects.get_or_create(name='Blockchain & Web3')
        diff_beg, _ = DifficultyLevel.objects.get_or_create(level='Beginner')
        diff_int, _ = DifficultyLevel.objects.get_or_create(level='Intermediate')

        for s in ['Python', 'Excel', 'CLI', 'DSA', 'AI/ML', 'Blockchain', 'Solidity', 'Ethereum', 'Smart Contracts', 'DeFi']:
            Skill.objects.get_or_create(name=s)

        # ── COURSE 1: Code Blocks ──
        c1, created = Course.objects.get_or_create(
            slug='code-blocks-fundamentals',
            defaults={
                'title': 'Code Blocks — CS Fundamentals',
                'description': 'A comprehensive starter course covering Excel, Command Line, Data Structures & Algorithms, AI/ML basics, and Blockchain fundamentals. Perfect for beginners entering the tech world.',
                'instructor': instructor, 'duration': 40, 'course_type': 'course',
                'rating': 4.7, 'review_count': 128, 'enrolled_count': 1520,
                'difficulty_level': diff_beg, 'language': lang, 'offered_by': org, 'industry': ind_tech,
            }
        )
        if created:
            c1.skills.set(Skill.objects.filter(name__in=['Python', 'Excel', 'CLI', 'DSA', 'AI/ML', 'Blockchain']))
            self._seed_code_blocks(c1)
            self.stdout.write(self.style.SUCCESS(f'Created course: {c1.title}'))

        # ── COURSE 2: Blockchain Mastery ──
        c2, created = Course.objects.get_or_create(
            slug='blockchain-mastery',
            defaults={
                'title': 'Blockchain Mastery — From Zero to Web3',
                'description': 'Deep-dive into blockchain technology: cryptography, consensus mechanisms, Ethereum, Solidity smart contracts, DeFi, NFTs, and building dApps. Earn a verifiable on-chain NFT certificate upon completion.',
                'instructor': instructor, 'duration': 60, 'course_type': 'course',
                'rating': 4.9, 'review_count': 87, 'enrolled_count': 940,
                'difficulty_level': diff_int, 'language': lang, 'offered_by': org, 'industry': ind_bc,
            }
        )
        if created:
            c2.skills.set(Skill.objects.filter(name__in=['Blockchain', 'Solidity', 'Ethereum', 'Smart Contracts', 'DeFi']))
            self._seed_blockchain(c2)
            self.stdout.write(self.style.SUCCESS(f'Created course: {c2.title}'))

        self.stdout.write(self.style.SUCCESS('Done seeding courses.'))

    # ─── Code Blocks modules ───
    def _seed_code_blocks(self, course):
        modules = [
            ('Excel Fundamentals', 'Master spreadsheet basics — formulas, charts, pivot tables, and data analysis.', [
                ('Introduction to Spreadsheets', 'Learn what spreadsheets are, the Excel interface, and basic navigation.\n\n## Topics\n- Workbooks vs Worksheets\n- Cells, rows, columns\n- Entering and formatting data\n- Auto-fill and Flash Fill'),
                ('Formulas & Functions', '## Core Formulas\n- `SUM`, `AVERAGE`, `COUNT`, `MAX`, `MIN`\n- `IF`, `VLOOKUP`, `HLOOKUP`\n- `CONCATENATE`, `LEFT`, `RIGHT`, `MID`\n\n## Practice\nBuild a student grade calculator using nested IF statements.'),
                ('Charts & Pivot Tables', '## Data Visualization\n- Bar, Line, Pie charts\n- Formatting chart elements\n\n## Pivot Tables\n- Creating pivot tables from raw data\n- Grouping, filtering, slicing\n- Calculated fields'),
            ]),
            ('Command Line Essentials', 'Navigate and automate using the terminal — Windows CMD, PowerShell, and Linux Bash.', [
                ('Terminal Basics', '## Getting Started\n- Opening the terminal (CMD, PowerShell, Bash)\n- `pwd`, `ls`/`dir`, `cd`, `mkdir`, `rmdir`\n- File operations: `cp`, `mv`, `rm`, `touch`\n- Understanding PATH and environment variables'),
                ('Scripting & Automation', '## Shell Scripting\n- Writing `.sh` and `.bat` scripts\n- Variables, loops, conditionals\n- Piping and redirection (`|`, `>`, `>>`)\n- `grep`, `find`, `awk` basics\n\n## Practical Task\nWrite a script that organizes files by extension into folders.'),
                ('Package Managers & Git', '## Package Managers\n- `pip`, `npm`, `apt`, `brew`\n\n## Git Fundamentals\n- `git init`, `add`, `commit`, `push`, `pull`\n- Branching and merging\n- Resolving merge conflicts'),
            ]),
            ('Data Structures & Algorithms', 'Build strong problem-solving foundations with core DSA concepts in Python.', [
                ('Arrays & Strings', '## Arrays\n- Declaration, traversal, insertion, deletion\n- Two-pointer technique\n- Sliding window\n\n## Strings\n- Reversal, palindrome check\n- Anagram detection\n- String matching algorithms'),
                ('Linked Lists & Stacks', '## Linked Lists\n- Singly vs Doubly linked lists\n- Insertion, deletion, reversal\n\n## Stacks & Queues\n- LIFO vs FIFO\n- Implementation using arrays and linked lists\n- Applications: expression evaluation, BFS'),
                ('Sorting & Searching', '## Sorting\n- Bubble, Selection, Insertion sort\n- Merge sort, Quick sort\n- Time complexity analysis\n\n## Searching\n- Linear search\n- Binary search and its variants\n- Search in rotated arrays'),
                ('Trees & Graphs', '## Trees\n- Binary trees, BST\n- Traversals: Inorder, Preorder, Postorder\n- BFS vs DFS\n\n## Graphs\n- Adjacency list vs matrix\n- BFS, DFS\n- Shortest path (Dijkstra)'),
            ]),
            ('AI & Machine Learning Basics', 'Understand the foundations of artificial intelligence and build your first ML model.', [
                ('What is AI?', '## Overview\n- History of AI\n- Types: Narrow AI vs General AI\n- Real-world applications\n- Ethics in AI\n\n## Key Concepts\n- Training data, features, labels\n- Supervised vs Unsupervised learning\n- Reinforcement learning overview'),
                ('Python for Data Science', '## Libraries\n- NumPy: arrays, operations\n- Pandas: DataFrames, cleaning\n- Matplotlib & Seaborn: visualization\n\n## Hands-On\nLoad a CSV dataset, clean it, and create visualizations.'),
                ('Building Your First ML Model', '## Scikit-Learn Pipeline\n1. Load dataset\n2. Split train/test\n3. Choose algorithm (Linear Regression)\n4. Train the model\n5. Evaluate with metrics (MSE, R²)\n\n## Practice\nPredict house prices using the Boston Housing dataset.'),
            ]),
            ('Blockchain Fundamentals', 'Understand the technology behind Bitcoin, Ethereum, and decentralized systems.', [
                ('What is Blockchain?', '## Core Concepts\n- Distributed ledger technology\n- Blocks, chains, and hashing\n- Consensus mechanisms: PoW, PoS\n- Immutability and transparency\n\n## History\n- Bitcoin whitepaper (2008)\n- Ethereum and smart contracts\n- Current landscape'),
                ('Cryptography Basics', '## Hashing\n- SHA-256\n- Hash properties: deterministic, avalanche effect\n\n## Public Key Cryptography\n- Private key, public key, address\n- Digital signatures\n- Wallets and key management'),
                ('Smart Contracts & dApps', '## Smart Contracts\n- Self-executing code on blockchain\n- Solidity language basics\n- Deploy, interact, verify\n\n## dApps\n- Frontend + smart contract\n- Web3 libraries (ethers.js)\n- MetaMask integration'),
            ]),
            ('Final Examination', 'Comprehensive exam covering all modules.', []),
        ]
        for i, (title, desc, lessons) in enumerate(modules, 1):
            is_exam = (title == 'Final Examination')
            m = Module.objects.create(course=course, title=title, description=desc, order=i, is_final_exam=is_exam, final_exam_time=60 if is_exam else 0)
            for j, (lt, lc) in enumerate(lessons, 1):
                Lesson.objects.create(module=m, title=lt, content=lc, order=j)

    # ─── Blockchain Mastery modules ───
    def _seed_blockchain(self, course):
        modules = [
            ('Introduction to Blockchain', 'Understand the foundational concepts of distributed ledger technology.', [
                ('The Evolution of Digital Trust', '## From Centralized to Decentralized\n- Traditional banking and intermediaries\n- The double-spending problem\n- How blockchain solves trust\n- Key properties: decentralization, transparency, immutability'),
                ('How Blockchain Works', '## Block Structure\n- Header: previous hash, timestamp, nonce\n- Body: transaction data\n- Merkle trees\n\n## Mining & Validation\n- Proof of Work explained\n- Block confirmation\n- Network propagation'),
                ('Types of Blockchains', '## Categories\n- Public: Bitcoin, Ethereum\n- Private: Hyperledger, Corda\n- Consortium: Quorum\n- Sidechains and Layer 2 solutions'),
            ]),
            ('Cryptography & Security', 'Deep-dive into the cryptographic primitives that power blockchain.', [
                ('Hash Functions', '## SHA-256 Deep Dive\n- Properties: deterministic, pre-image resistance\n- Avalanche effect demonstration\n- Merkle trees in blockchain\n- Hash-based data structures'),
                ('Public Key Infrastructure', '## Asymmetric Cryptography\n- RSA vs Elliptic Curve (secp256k1)\n- Key generation process\n- Digital signatures (ECDSA)\n- Address derivation in Ethereum'),
                ('Wallet Security', '## Wallet Types\n- Hot wallets vs Cold wallets\n- HD wallets (BIP-32, BIP-39)\n- Seed phrases and recovery\n- Multi-signature wallets\n- Hardware wallets (Ledger, Trezor)'),
            ]),
            ('Ethereum & EVM', 'Master the Ethereum platform — accounts, gas, and the EVM.', [
                ('Ethereum Architecture', '## Components\n- World state and accounts (EOA vs Contract)\n- Gas system and fee market (EIP-1559)\n- Ethereum Virtual Machine (EVM)\n- State transitions'),
                ('Ethereum Ecosystem', '## Tools & Infrastructure\n- Infura, Alchemy — RPC providers\n- Etherscan — block explorer\n- MetaMask — wallet\n- Testnets: Sepolia, Goerli\n\n## Practice\nSet up MetaMask, get testnet ETH, send a transaction.'),
                ('Token Standards', '## ERC Standards\n- ERC-20: Fungible tokens\n- ERC-721: Non-Fungible Tokens (NFTs)\n- ERC-1155: Multi-token standard\n- ERC-4626: Tokenized vaults'),
            ]),
            ('Solidity Programming', 'Learn to write, test, and deploy smart contracts in Solidity.', [
                ('Solidity Basics', '## Language Fundamentals\n- Data types: uint, int, address, bool, string\n- Variables: state, local, global\n- Functions: visibility, modifiers\n- Control structures\n\n```solidity\npragma solidity ^0.8.0;\ncontract HelloWorld {\n    string public greeting = "Hello, Blockchain!";\n}\n```'),
                ('Advanced Solidity', '## Patterns\n- Inheritance and interfaces\n- Events and logging\n- Error handling (require, revert, assert)\n- Libraries and using-for\n- Proxy patterns for upgradeability'),
                ('Smart Contract Security', '## Common Vulnerabilities\n- Reentrancy attacks\n- Integer overflow/underflow\n- Front-running\n- Access control issues\n\n## Best Practices\n- OpenZeppelin contracts\n- Checks-Effects-Interactions pattern\n- Audit checklist'),
                ('Testing & Deployment', '## Development Tools\n- Hardhat / Foundry setup\n- Writing unit tests\n- Gas optimization techniques\n- Deploying to testnets\n- Verifying on Etherscan'),
            ]),
            ('DeFi & NFTs', 'Explore decentralized finance protocols and non-fungible token ecosystems.', [
                ('DeFi Fundamentals', '## Core Protocols\n- DEXs: Uniswap, AMM model\n- Lending: Aave, Compound\n- Stablecoins: DAI, USDC\n- Yield farming and liquidity mining\n- Flash loans'),
                ('NFT Deep Dive', '## NFT Technology\n- ERC-721 implementation\n- Metadata and IPFS storage\n- Minting mechanics\n- Royalty standards (ERC-2981)\n- NFT marketplaces'),
                ('Building a DeFi Protocol', '## Hands-On Project\n- Design a simple lending protocol\n- Implement deposit/withdraw\n- Interest rate model\n- Liquidation mechanism\n- Frontend integration with ethers.js'),
            ]),
            ('Building dApps', 'Connect smart contracts to modern web frontends and build full-stack dApps.', [
                ('Web3 Frontend Development', '## Stack\n- React + ethers.js / web3.js\n- Connecting MetaMask\n- Reading contract state\n- Sending transactions\n- Event listeners'),
                ('IPFS & Decentralized Storage', '## Storage Solutions\n- IPFS: content-addressable storage\n- Pinning services (Pinata, Infura)\n- Arweave for permanent storage\n- Storing NFT metadata'),
                ('Full-Stack dApp Project', '## Capstone Project\n- Build a certificate verification dApp\n- Solidity contract (ERC-721)\n- React frontend with MetaMask\n- Deploy to Sepolia testnet\n- Verify and share certificates'),
            ]),
            ('Final Examination', 'Comprehensive exam covering all blockchain modules.', []),
        ]
        for i, (title, desc, lessons) in enumerate(modules, 1):
            is_exam = (title == 'Final Examination')
            m = Module.objects.create(course=course, title=title, description=desc, order=i, is_final_exam=is_exam, final_exam_time=90 if is_exam else 0)
            for j, (lt, lc) in enumerate(lessons, 1):
                Lesson.objects.create(module=m, title=lt, content=lc, order=j)


