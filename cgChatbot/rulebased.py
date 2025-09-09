import re
import random

class CareerChatbot:
    def __init__(self, name="CareerBot"):
        self.name = name
        self.memory = {}
        self.rules = self._load_rules()
        self.fallback_responses = [
            "That's interesting, tell me more about your career goals!",
            "I see, can you explain what field you are interested in?",
            "Hmm, let's talk more about your study plans.",
            "Got it 👍, continue please..."
        ]

    def _load_rules(self):
        """Define regex-based rules and responses for career and student guidance."""
        return [
            # Greetings and name
            (r"(.*)my name is (.*)", ["Hello {name}, nice to meet you! What career are you aiming for?"]),
            (r"(hi|hey|hello|hola|holla)(.*)", ["Hello 👋", "Hey there!", "Hi! Excited to talk about your career?"]),
            (r"(.*) your name ?", [f"My name is {self.name}, your career assistant."]),
            (r"how are you(.*)", ["I'm doing great 😃, and ready to guide your career!", "I’m fine! How about you?"]),

            # Help command
            (r"(.*)help(.*)", [
                "I can help with career guidance, admissions, scholarships, study tips, course selection, and more. Try asking: 'What is the admission process?', 'How can I get a scholarship?', or 'What skills do I need for data science?'"
            ]),

            # Admissions
            (r"(.*)(admission|apply|application process|how to get admission)(.*)", [
                "The admission process usually involves submitting an application form, academic transcripts, and sometimes entrance exams or interviews. Which program are you interested in?"
            ]),

            # Scholarships
            (r"(.*)(scholarship|scholarships|financial aid|fee concession)(.*)", [
                "Many universities offer scholarships based on merit or need. Check the university website or contact the admissions office for details. Need tips on applying?"
            ]),

            # Study tips
            (r"(.*)(study tips|how to study|exam preparation|improve study habits)(.*)", [
                "Effective study tips: set a schedule, take regular breaks, practice past papers, and teach others what you learn. Want more personalized advice?"
            ]),

            # Course selection
            (r"(.*)(which course|select a major|choose a course|best course)(.*)", [
                "Choosing a course depends on your interests and strengths. Tell me what subjects you enjoy or your career goals, and I can suggest options."
            ]),

            # Career-specific rules
            (r"(.*)career guidance(.*)", [
                "Sure! Tell me about your field (e.g., software, medical, business) and I’ll suggest options."
            ]),
            (r"(.*)best career in (software|cs|computer science)(.*)", [
                "In Computer Science, you can go for Web Development 🌐, Data Science 📊, AI 🤖, or Cybersecurity 🔐."
            ]),
            (r"(.*)best career in (business|commerce)(.*)", [
                "In Business, great options include Marketing 📈, Finance 💵, Entrepreneurship 🚀, and Supply Chain 📦."
            ]),
            (r"(.*)scope of (ai|artificial intelligence)(.*)", [
                "AI has huge scope in automation, machine learning, robotics, and data-driven decision-making."
            ]),
            (r"(.*)scope of (software|cs|computer science)(.*)", [
                "Computer Science has global scope: Software Development, Cloud Computing, Cybersecurity, AI, and more."
            ]),
            (r"(.*)skills for (web developer|frontend|backend)(.*)", [
                "For Web Development: HTML, CSS, JavaScript, React, Node.js, and problem-solving skills are must!"
            ]),
            (r"(.*)skills for (data science|ai|ml)(.*)", [
                "For AI/Data Science: Python, Statistics, Machine Learning, Deep Learning, and SQL are key skills."
            ]),
            (r"(.*)how to write (cv|resume)(.*)", [
                "Keep your CV short (1-2 pages), highlight your skills, projects, and add a clear career objective."
            ]),

            # Farewell
            (r"(.*) (quit|exit)", ["Goodbye 👋, best of luck with your career!"]),
        ]

    def _match_rule(self, user_input):
        """Match user input against defined rules."""
        for pattern, responses in self.rules:
            match = re.match(pattern, user_input.lower())
            if match:
                response = random.choice(responses)

                # Store name if provided
                if "my name is" in pattern:
                    name = match.group(2).strip().capitalize()
                    self.memory["name"] = name
                    response = response.format(name=name)

                # Personalize response if {name} is used
                if "{name}" in response:
                    response = response.format(name=self.memory.get("name", "there"))

                return response
        # If user's name is known, personalize fallback
        if "name" in self.memory:
            return f"{self.memory['name']}, {random.choice(self.fallback_responses)}"
        return random.choice(self.fallback_responses)

    def chat(self):
        """Start conversation loop."""
        print(f"{self.name}: Hi! I’m {self.name}. Type 'help' to see what I can do, or 'quit' to exit.")
        while True:
            user_input = input("You: ").strip()
            if not user_input:
                print(f"{self.name}: Please say something 🙂")
                continue

            if user_input.lower() in ["quit", "exit"]:
                farewell = f"Goodbye 👋, it was great chatting with you!"
                if "name" in self.memory:
                    farewell = f"Goodbye {self.memory['name']} 👋, it was great chatting with you!"
                print(f"{self.name}: {farewell}")
                break

            response = self._match_rule(user_input)
            print(f"{self.name}: {response}")


if __name__ == "__main__":
    bot = CareerChatbot()
    bot.chat()
