import random
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Example comments data
comments = [
    "I love this!",
    "This is a great product!",
    "Terrible customer service.",
    "Worst purchase ever.",
    "Highly recommended.",
    "Your smile is contagious.",
    "I bet you can make even the crankiest babies smile.",
    "You have the best laugh.",
    "You light up the room.",
    "You have a great sense of humor.",
    "If you were a cartoon character, you'd be the one that gets bluebirds to sing on your shoulders.",
    "You're like sunshine on a rainy day.",
    "You bring out the best in other people.",
    "There's just something about you that shines.",
    "Colors seem brighter when you're around.",
    "You always know how to have fun.",
    "Jokes are funnier when you tell them.",
    "You're the best at finding silver linings.",
    "You always know what to say to make me feel better.",
    "Being around you is like a happy little vacation.",
    "You're more fun than bubble wrap.",
    "You're like a breath of fresh air.",
    "You're someone's reason to smile."
]

# Tokenize comments
words = [comment.split() for comment in comments]

# Create a dictionary of transitions
transitions = {}
for comment in words:
    for i in range(len(comment) - 1):
        current_word = comment[i]
        next_word = comment[i + 1]
        if current_word in transitions:
            transitions[current_word].append(next_word)
        else:
            transitions[current_word] = [next_word]

# Function to generate comments
def generate_comment(seed_word, next_words):
    current_word = seed_word
    generated_comment = seed_word
    for _ in range(next_words):
        if current_word in transitions:
            next_word = random.choice(transitions[current_word])
            generated_comment += " " + next_word
            current_word = next_word
        else:
            break
    return generated_comment

# API endpoint to generate comments
@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    seed_word = data.get('seed_word')
    next_words = int(data.get('next_words', 5))  # Convert next_words to integer
    
    if not seed_word:
        return jsonify({'error': 'seed_word is required'}), 400
    
    generated_comment = generate_comment(seed_word, next_words)
    return jsonify({'generated_comment': generated_comment})

# Serve the web interface
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
