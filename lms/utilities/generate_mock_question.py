import pandas as pd
import random

# Sample data for questions and answers
questions = [
    ("Who developed the Python programming language?", ["Guido van Rossum", "James Gosling", "Dennis Ritchie", "Bjarne Stroustrup"], "A"),
    ("Which company developed the Windows operating system?", ["Apple", "Microsoft", "IBM", "Google"], "B"),
    ("What does CPU stand for?", ["Central Process Unit", "Central Processing Unit", "Computer Personal Unit", "Central Processor Utility"], "B"),
    ("What is the capital of France?", ["Berlin", "London", "Paris", "Madrid"], "C"),
    ("Which data structure uses FIFO order?", ["Stack", "Queue", "Tree", "Graph"], "B"),
    ("Which planet is known as the Red Planet?", ["Earth", "Venus", "Mars", "Jupiter"], "C"),
    ("Which protocol is used to send emails?", ["HTTP", "FTP", "SMTP", "IMAP"], "C"),
    ("Who is the founder of Microsoft?", ["Steve Jobs", "Bill Gates", "Larry Page", "Elon Musk"], "B"),
    ("Which gas is essential for respiration?", ["Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen"], "A"),
    ("Which one is an operating system?", ["Python", "Linux", "HTML", "CSS"], "B"),
    ("Which symbol is used to denote comments in Python?", ["//", "#", "/* */", "--"], "B"),
    ("Which device is used to input data into a computer?", ["Monitor", "Keyboard", "Printer", "Speaker"], "B"),
    ("Which planet is closest to the Sun?", ["Mercury", "Venus", "Earth", "Mars"], "A"),
    ("What is the chemical symbol of water?", ["H2O", "O2", "CO2", "HO"], "A"),
    ("Which of these is a mammal?", ["Snake", "Shark", "Whale", "Frog"], "C"),
    ("Which company owns Android OS?", ["Apple", "Microsoft", "Google", "IBM"], "C"),
    ("Which keyword is used to define a function in Python?", ["func", "def", "function", "lambda"], "B"),
    ("Which one is a web browser?", ["Chrome", "Windows", "Linux", "Android"], "A"),
    ("Which ocean is the largest?", ["Atlantic", "Indian", "Arctic", "Pacific"], "D"),
    ("Who painted the Mona Lisa?", ["Vincent Van Gogh", "Leonardo da Vinci", "Pablo Picasso", "Michelangelo"], "B"),
]

if __name__ == "__main__":
    # Shuffle and take 20
    random.shuffle(questions)
    selected_questions = questions[:20]

    # Convert to DataFrame
    df = pd.DataFrame(selected_questions, columns=["Question", "Options", "Answer"])
    df[["A", "B", "C", "D"]] = pd.DataFrame(df["Options"].tolist(), index=df.index)
    df = df[["Question", "A", "B", "C", "D", "Answer"]]

    # Save to Excel
    file_path = "utilities\\mock_questions.csv"
    df.to_csv(file_path, index=False)

    print(file_path)


