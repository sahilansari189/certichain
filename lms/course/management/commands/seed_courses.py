from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from course.models import Course, Module, Lesson, Skill, DifficultyLevel, Language, OfferedBy, Industry
from exam.models import Question, Option

class Command(BaseCommand):
    help = 'Seed two demo courses with modules, lessons, and quiz questions'

    def _create_question(self, text, options):
        """Create a question with options. options = [(text, is_correct), ...]"""
        q = Question.objects.create(question=text)
        for opt_text, correct in options:
            Option.objects.create(question=q, option=opt_text, is_correct=correct)
        return q

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
        # --- Module quiz questions ---
        excel_quiz = [
            ('What does the SUM function do in Excel?', [('Adds all values in a range', True), ('Finds the average', False), ('Counts cells', False), ('Finds maximum value', False)]),
            ('Which function searches for a value in the first column and returns a value in the same row?', [('HLOOKUP', False), ('VLOOKUP', True), ('INDEX', False), ('MATCH', False)]),
            ('What is a Pivot Table used for?', [('Creating charts', False), ('Summarizing and analyzing large datasets', True), ('Writing macros', False), ('Formatting cells', False)]),
        ]
        cli_quiz = [
            ('Which command lists files in a directory on Linux?', [('dir', False), ('ls', True), ('list', False), ('show', False)]),
            ('What does the pipe operator (|) do in the command line?', [('Deletes files', False), ('Passes output of one command as input to another', True), ('Creates a new directory', False), ('Opens a file', False)]),
            ('Which command initializes a new Git repository?', [('git start', False), ('git new', False), ('git init', True), ('git create', False)]),
        ]
        dsa_quiz = [
            ('What is the time complexity of binary search?', [('O(n)', False), ('O(n²)', False), ('O(log n)', True), ('O(1)', False)]),
            ('Which data structure uses LIFO (Last In, First Out)?', [('Queue', False), ('Array', False), ('Stack', True), ('Linked List', False)]),
            ('What traversal visits root → left → right?', [('Inorder', False), ('Preorder', True), ('Postorder', False), ('Level order', False)]),
            ('What is the worst-case time complexity of Quick Sort?', [('O(n log n)', False), ('O(n)', False), ('O(n²)', True), ('O(log n)', False)]),
        ]
        aiml_quiz = [
            ('Which type of learning uses labeled data?', [('Unsupervised', False), ('Reinforcement', False), ('Supervised', True), ('Transfer', False)]),
            ('What Python library is primarily used for numerical arrays?', [('Pandas', False), ('NumPy', True), ('Matplotlib', False), ('Scikit-learn', False)]),
            ('What metric measures the average squared difference between predictions and actual values?', [('R² Score', False), ('Accuracy', False), ('Mean Squared Error (MSE)', True), ('F1 Score', False)]),
        ]
        bc_quiz = [
            ('What problem does blockchain solve in digital transactions?', [('Scalability', False), ('Double spending', True), ('User interface', False), ('Data compression', False)]),
            ('What is SHA-256?', [('An encryption algorithm', False), ('A hash function', True), ('A consensus mechanism', False), ('A smart contract language', False)]),
            ('What does a smart contract do?', [('Mines cryptocurrency', False), ('Stores private keys', False), ('Self-executes when conditions are met', True), ('Sends emails', False)]),
        ]
        # Full course final exam (mix from all modules)
        final_exam_q = [
            ('In Excel, what does the CONCATENATE function do?', [('Adds numbers', False), ('Joins text strings together', True), ('Creates charts', False), ('Sorts data', False)]),
            ('What does "cd .." do in the terminal?', [('Creates a directory', False), ('Moves up one directory', True), ('Deletes a file', False), ('Lists files', False)]),
            ('What is the time complexity of Merge Sort?', [('O(n)', False), ('O(n²)', False), ('O(n log n)', True), ('O(log n)', False)]),
            ('Which algorithm is used for finding the shortest path in a graph?', [('Binary Search', False), ('Bubble Sort', False), ('Dijkstra', True), ('Quick Sort', False)]),
            ('What is the difference between supervised and unsupervised learning?', [('Supervised uses labeled data, unsupervised does not', True), ('They are the same', False), ('Unsupervised requires more data', False), ('Supervised is faster', False)]),
            ('What is a blockchain block composed of?', [('Only transactions', False), ('Header and body with transaction data', True), ('Only hash values', False), ('Smart contracts only', False)]),
            ('What consensus mechanism does Bitcoin use?', [('Proof of Stake', False), ('Proof of Work', True), ('Delegated PoS', False), ('Proof of Authority', False)]),
            ('What is a linked list?', [('A sequential array', False), ('A collection of nodes where each points to the next', True), ('A type of hash table', False), ('A binary tree', False)]),
            ('What library is used for data manipulation in Python?', [('NumPy', False), ('Flask', False), ('Pandas', True), ('Django', False)]),
            ('What does EVM stand for?', [('Ethereum Virtual Machine', True), ('Encrypted Virtual Memory', False), ('External Validation Module', False), ('Ethereum Verified Miner', False)]),
        ]

        modules = [
            ('Excel Fundamentals', 'Master spreadsheet basics — formulas, charts, pivot tables, and data analysis.', [
                ('Introduction to Spreadsheets', 'Learn what spreadsheets are, the Excel interface, and basic navigation.\n\n## Topics\n- Workbooks vs Worksheets\n- Cells, rows, columns\n- Entering and formatting data\n- Auto-fill and Flash Fill'),
                ('Formulas & Functions', '## Core Formulas\n- `SUM`, `AVERAGE`, `COUNT`, `MAX`, `MIN`\n- `IF`, `VLOOKUP`, `HLOOKUP`\n- `CONCATENATE`, `LEFT`, `RIGHT`, `MID`\n\n## Practice\nBuild a student grade calculator using nested IF statements.'),
                ('Charts & Pivot Tables', '## Data Visualization\n- Bar, Line, Pie charts\n- Formatting chart elements\n\n## Pivot Tables\n- Creating pivot tables from raw data\n- Grouping, filtering, slicing\n- Calculated fields'),
            ], excel_quiz),
            ('Command Line Essentials', 'Navigate and automate using the terminal — Windows CMD, PowerShell, and Linux Bash.', [
                ('Terminal Basics', '## Getting Started\n- Opening the terminal (CMD, PowerShell, Bash)\n- `pwd`, `ls`/`dir`, `cd`, `mkdir`, `rmdir`\n- File operations: `cp`, `mv`, `rm`, `touch`\n- Understanding PATH and environment variables'),
                ('Scripting & Automation', '## Shell Scripting\n- Writing `.sh` and `.bat` scripts\n- Variables, loops, conditionals\n- Piping and redirection (`|`, `>`, `>>`)\n- `grep`, `find`, `awk` basics\n\n## Practical Task\nWrite a script that organizes files by extension into folders.'),
                ('Package Managers & Git', '## Package Managers\n- `pip`, `npm`, `apt`, `brew`\n\n## Git Fundamentals\n- `git init`, `add`, `commit`, `push`, `pull`\n- Branching and merging\n- Resolving merge conflicts'),
            ], cli_quiz),
            ('Data Structures & Algorithms', 'Build strong problem-solving foundations with core DSA concepts in Python.', [
                ('Arrays & Strings', '## Arrays\n- Declaration, traversal, insertion, deletion\n- Two-pointer technique\n- Sliding window\n\n## Strings\n- Reversal, palindrome check\n- Anagram detection\n- String matching algorithms'),
                ('Linked Lists & Stacks', '## Linked Lists\n- Singly vs Doubly linked lists\n- Insertion, deletion, reversal\n\n## Stacks & Queues\n- LIFO vs FIFO\n- Implementation using arrays and linked lists\n- Applications: expression evaluation, BFS'),
                ('Sorting & Searching', '## Sorting\n- Bubble, Selection, Insertion sort\n- Merge sort, Quick sort\n- Time complexity analysis\n\n## Searching\n- Linear search\n- Binary search and its variants\n- Search in rotated arrays'),
                ('Trees & Graphs', '## Trees\n- Binary trees, BST\n- Traversals: Inorder, Preorder, Postorder\n- BFS vs DFS\n\n## Graphs\n- Adjacency list vs matrix\n- BFS, DFS\n- Shortest path (Dijkstra)'),
            ], dsa_quiz),
            ('AI & Machine Learning Basics', 'Understand the foundations of artificial intelligence and build your first ML model.', [
                ('What is AI?', '## Overview\n- History of AI\n- Types: Narrow AI vs General AI\n- Real-world applications\n- Ethics in AI\n\n## Key Concepts\n- Training data, features, labels\n- Supervised vs Unsupervised learning\n- Reinforcement learning overview'),
                ('Python for Data Science', '## Libraries\n- NumPy: arrays, operations\n- Pandas: DataFrames, cleaning\n- Matplotlib & Seaborn: visualization\n\n## Hands-On\nLoad a CSV dataset, clean it, and create visualizations.'),
                ('Building Your First ML Model', '## Scikit-Learn Pipeline\n1. Load dataset\n2. Split train/test\n3. Choose algorithm (Linear Regression)\n4. Train the model\n5. Evaluate with metrics (MSE, R²)\n\n## Practice\nPredict house prices using the Boston Housing dataset.'),
            ], aiml_quiz),
            ('Blockchain Fundamentals', 'Understand the technology behind Bitcoin, Ethereum, and decentralized systems.', [
                ('What is Blockchain?', '## Core Concepts\n- Distributed ledger technology\n- Blocks, chains, and hashing\n- Consensus mechanisms: PoW, PoS\n- Immutability and transparency\n\n## History\n- Bitcoin whitepaper (2008)\n- Ethereum and smart contracts\n- Current landscape'),
                ('Cryptography Basics', '## Hashing\n- SHA-256\n- Hash properties: deterministic, avalanche effect\n\n## Public Key Cryptography\n- Private key, public key, address\n- Digital signatures\n- Wallets and key management'),
                ('Smart Contracts & dApps', '## Smart Contracts\n- Self-executing code on blockchain\n- Solidity language basics\n- Deploy, interact, verify\n\n## dApps\n- Frontend + smart contract\n- Web3 libraries (ethers.js)\n- MetaMask integration'),
            ], bc_quiz),
            ('Final Examination', 'Comprehensive exam covering all modules.', [], final_exam_q),
        ]
        all_questions = []
        for i, (title, desc, lessons, quiz) in enumerate(modules, 1):
            is_exam = (title == 'Final Examination')
            m = Module.objects.create(course=course, title=title, description=desc, order=i, is_final_exam=is_exam, final_exam_time=5 if is_exam else 0)
            questions = [self._create_question(q, opts) for q, opts in quiz]
            if not is_exam:
                all_questions.extend(questions)
            for j, (lt, lc) in enumerate(lessons, 1):
                lesson = Lesson.objects.create(module=m, title=lt, content=lc, order=j)
                # Attach quiz only to the last lesson of the module
                if j == len(lessons):
                    lesson.questions.set(questions)
            if is_exam:
                # Final exam gets ALL questions from every module
                all_final = all_questions + questions
                exam_lesson = Lesson.objects.create(module=m, title='Final Exam — All Modules', content='Answer all questions below. You need 70% to pass and earn your certificate.', order=1)
                exam_lesson.questions.set(all_final)

    # ─── Blockchain Mastery modules ───
    def _seed_blockchain(self, course):
        intro_quiz = [
            ('What is a distributed ledger?', [('A single centralized database', False), ('A database replicated across multiple nodes', True), ('A type of cryptocurrency', False), ('A mining algorithm', False)]),
            ('What problem did the Bitcoin whitepaper solve?', [('Fast transactions', False), ('The double-spending problem', True), ('Smart contracts', False), ('Data storage', False)]),
            ('Which is NOT a type of blockchain?', [('Public', False), ('Private', False), ('Consortium', False), ('Recursive', True)]),
        ]
        crypto_quiz = [
            ('What is the avalanche effect in hashing?', [('Small input change produces completely different output', True), ('Hash gets larger over time', False), ('Multiple inputs produce the same hash', False), ('Hashing becomes slower', False)]),
            ('What curve does Ethereum use for cryptography?', [('RSA-2048', False), ('secp256k1', True), ('P-256', False), ('Curve25519', False)]),
            ('What is a seed phrase used for?', [('Mining blocks', False), ('Recovering a wallet', True), ('Signing transactions', False), ('Deploying contracts', False)]),
        ]
        eth_quiz = [
            ('What are the two types of Ethereum accounts?', [('Mining and Staking', False), ('EOA and Contract', True), ('Public and Private', False), ('Hot and Cold', False)]),
            ('What did EIP-1559 introduce?', [('Proof of Stake', False), ('Base fee and priority fee model', True), ('Smart contracts', False), ('Layer 2 scaling', False)]),
            ('Which is the ERC standard for NFTs?', [('ERC-20', False), ('ERC-721', True), ('ERC-1155', False), ('ERC-4626', False)]),
        ]
        solidity_quiz = [
            ('What is the correct way to declare a public unsigned integer in Solidity?', [('int public x;', False), ('uint public x;', True), ('public uint x;', False), ('var x = uint;', False)]),
            ('What keyword is used to handle errors in Solidity?', [('try/catch', False), ('require', True), ('if/else', False), ('throw', False)]),
            ('What is a reentrancy attack?', [('Calling a function too many times', False), ('A contract calling back into the caller before state update', True), ('Overflow of integers', False), ('Gas limit exceeded', False)]),
            ('What tool is used for Solidity testing and deployment?', [('Webpack', False), ('Hardhat', True), ('Docker', False), ('Kubernetes', False)]),
        ]
        defi_quiz = [
            ('What does AMM stand for?', [('Automated Market Maker', True), ('Advanced Mining Module', False), ('Algorithmic Money Manager', False), ('Automated Minting Machine', False)]),
            ('What is a flash loan?', [('A long-term lending protocol', False), ('A loan that must be borrowed and repaid in one transaction', True), ('A type of stablecoin', False), ('A mining reward', False)]),
            ('What ERC standard handles royalties for NFTs?', [('ERC-20', False), ('ERC-721', False), ('ERC-2981', True), ('ERC-1155', False)]),
        ]
        dapp_quiz = [
            ('What JavaScript library is commonly used to interact with Ethereum?', [('jQuery', False), ('ethers.js', True), ('React', False), ('Express', False)]),
            ('What does IPFS stand for?', [('Internet Protocol File System', False), ('InterPlanetary File System', True), ('Internal Private File Storage', False), ('Integrated Public File Service', False)]),
            ('What is MetaMask?', [('A blockchain', False), ('A browser wallet extension for Ethereum', True), ('A smart contract language', False), ('A mining software', False)]),
        ]
        # Full course final exam
        final_exam_q = [
            ('What is the main innovation of blockchain technology?', [('Faster databases', False), ('Decentralized, trustless consensus', True), ('Better user interfaces', False), ('Cloud computing', False)]),
            ('What hashing algorithm does Bitcoin use?', [('MD5', False), ('SHA-256', True), ('SHA-3', False), ('RIPEMD-160', False)]),
            ('What is gas in Ethereum?', [('A cryptocurrency', False), ('A unit measuring computational effort', True), ('A type of token', False), ('A consensus mechanism', False)]),
            ('What does the "view" keyword mean in a Solidity function?', [('The function can modify state', False), ('The function only reads state without modifying it', True), ('The function is private', False), ('The function costs no gas to deploy', False)]),
            ('What is the Checks-Effects-Interactions pattern used for?', [('Gas optimization', False), ('Preventing reentrancy attacks', True), ('Deploying contracts', False), ('Token transfers', False)]),
            ('What is a DEX?', [('Digital Exchange Xchange', False), ('Decentralized Exchange', True), ('Data Encryption Xfer', False), ('Distributed Ethereum Exchange', False)]),
            ('What is the purpose of ERC-721?', [('Fungible token standard', False), ('Non-Fungible Token standard', True), ('Governance token standard', False), ('Stablecoin standard', False)]),
            ('What does IPFS use to identify content?', [('URLs', False), ('Content-based hashes (CID)', True), ('IP addresses', False), ('Domain names', False)]),
            ('What is a Merkle tree?', [('A type of blockchain', False), ('A hash-based data structure for efficient verification', True), ('A consensus algorithm', False), ('A cryptographic key', False)]),
            ('What is the purpose of the nonce in a block header?', [('Stores transaction data', False), ('A value miners change to find valid hash', True), ('Records the block timestamp', False), ('Holds the previous block hash', False)]),
            ('What is a proxy pattern in Solidity?', [('A way to hide contract code', False), ('A pattern enabling contract upgradeability', True), ('A security vulnerability', False), ('A testing framework', False)]),
            ('What is yield farming?', [('Mining cryptocurrency', False), ('Providing liquidity to earn rewards', True), ('Creating NFTs', False), ('Building dApps', False)]),
        ]

        modules = [
            ('Introduction to Blockchain', 'Understand the foundational concepts of distributed ledger technology.', [
                ('The Evolution of Digital Trust', '## From Centralized to Decentralized\n- Traditional banking and intermediaries\n- The double-spending problem\n- How blockchain solves trust\n- Key properties: decentralization, transparency, immutability'),
                ('How Blockchain Works', '## Block Structure\n- Header: previous hash, timestamp, nonce\n- Body: transaction data\n- Merkle trees\n\n## Mining & Validation\n- Proof of Work explained\n- Block confirmation\n- Network propagation'),
                ('Types of Blockchains', '## Categories\n- Public: Bitcoin, Ethereum\n- Private: Hyperledger, Corda\n- Consortium: Quorum\n- Sidechains and Layer 2 solutions'),
            ], intro_quiz),
            ('Cryptography & Security', 'Deep-dive into the cryptographic primitives that power blockchain.', [
                ('Hash Functions', '## SHA-256 Deep Dive\n- Properties: deterministic, pre-image resistance\n- Avalanche effect demonstration\n- Merkle trees in blockchain\n- Hash-based data structures'),
                ('Public Key Infrastructure', '## Asymmetric Cryptography\n- RSA vs Elliptic Curve (secp256k1)\n- Key generation process\n- Digital signatures (ECDSA)\n- Address derivation in Ethereum'),
                ('Wallet Security', '## Wallet Types\n- Hot wallets vs Cold wallets\n- HD wallets (BIP-32, BIP-39)\n- Seed phrases and recovery\n- Multi-signature wallets\n- Hardware wallets (Ledger, Trezor)'),
            ], crypto_quiz),
            ('Ethereum & EVM', 'Master the Ethereum platform — accounts, gas, and the EVM.', [
                ('Ethereum Architecture', '## Components\n- World state and accounts (EOA vs Contract)\n- Gas system and fee market (EIP-1559)\n- Ethereum Virtual Machine (EVM)\n- State transitions'),
                ('Ethereum Ecosystem', '## Tools & Infrastructure\n- Infura, Alchemy — RPC providers\n- Etherscan — block explorer\n- MetaMask — wallet\n- Testnets: Sepolia, Goerli\n\n## Practice\nSet up MetaMask, get testnet ETH, send a transaction.'),
                ('Token Standards', '## ERC Standards\n- ERC-20: Fungible tokens\n- ERC-721: Non-Fungible Tokens (NFTs)\n- ERC-1155: Multi-token standard\n- ERC-4626: Tokenized vaults'),
            ], eth_quiz),
            ('Solidity Programming', 'Learn to write, test, and deploy smart contracts in Solidity.', [
                ('Solidity Basics', '## Language Fundamentals\n- Data types: uint, int, address, bool, string\n- Variables: state, local, global\n- Functions: visibility, modifiers\n- Control structures\n\n```solidity\npragma solidity ^0.8.0;\ncontract HelloWorld {\n    string public greeting = "Hello, Blockchain!";\n}\n```'),
                ('Advanced Solidity', '## Patterns\n- Inheritance and interfaces\n- Events and logging\n- Error handling (require, revert, assert)\n- Libraries and using-for\n- Proxy patterns for upgradeability'),
                ('Smart Contract Security', '## Common Vulnerabilities\n- Reentrancy attacks\n- Integer overflow/underflow\n- Front-running\n- Access control issues\n\n## Best Practices\n- OpenZeppelin contracts\n- Checks-Effects-Interactions pattern\n- Audit checklist'),
                ('Testing & Deployment', '## Development Tools\n- Hardhat / Foundry setup\n- Writing unit tests\n- Gas optimization techniques\n- Deploying to testnets\n- Verifying on Etherscan'),
            ], solidity_quiz),
            ('DeFi & NFTs', 'Explore decentralized finance protocols and non-fungible token ecosystems.', [
                ('DeFi Fundamentals', '## Core Protocols\n- DEXs: Uniswap, AMM model\n- Lending: Aave, Compound\n- Stablecoins: DAI, USDC\n- Yield farming and liquidity mining\n- Flash loans'),
                ('NFT Deep Dive', '## NFT Technology\n- ERC-721 implementation\n- Metadata and IPFS storage\n- Minting mechanics\n- Royalty standards (ERC-2981)\n- NFT marketplaces'),
                ('Building a DeFi Protocol', '## Hands-On Project\n- Design a simple lending protocol\n- Implement deposit/withdraw\n- Interest rate model\n- Liquidation mechanism\n- Frontend integration with ethers.js'),
            ], defi_quiz),
            ('Building dApps', 'Connect smart contracts to modern web frontends and build full-stack dApps.', [
                ('Web3 Frontend Development', '## Stack\n- React + ethers.js / web3.js\n- Connecting MetaMask\n- Reading contract state\n- Sending transactions\n- Event listeners'),
                ('IPFS & Decentralized Storage', '## Storage Solutions\n- IPFS: content-addressable storage\n- Pinning services (Pinata, Infura)\n- Arweave for permanent storage\n- Storing NFT metadata'),
                ('Full-Stack dApp Project', '## Capstone Project\n- Build a certificate verification dApp\n- Solidity contract (ERC-721)\n- React frontend with MetaMask\n- Deploy to Sepolia testnet\n- Verify and share certificates'),
            ], dapp_quiz),
            ('Final Examination', 'Comprehensive exam covering all blockchain modules.', [], final_exam_q),
        ]
        all_questions = []
        for i, (title, desc, lessons, quiz) in enumerate(modules, 1):
            is_exam = (title == 'Final Examination')
            m = Module.objects.create(course=course, title=title, description=desc, order=i, is_final_exam=is_exam, final_exam_time=5 if is_exam else 0)
            questions = [self._create_question(q, opts) for q, opts in quiz]
            if not is_exam:
                all_questions.extend(questions)
            for j, (lt, lc) in enumerate(lessons, 1):
                lesson = Lesson.objects.create(module=m, title=lt, content=lc, order=j)
                if j == len(lessons):
                    lesson.questions.set(questions)
            if is_exam:
                all_final = all_questions + questions
                exam_lesson = Lesson.objects.create(module=m, title='Final Exam — Blockchain Mastery', content='Answer all questions below. You need 70% to pass and earn your blockchain NFT certificate.', order=1)
                exam_lesson.questions.set(all_final)
