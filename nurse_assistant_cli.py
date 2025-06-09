import os
import datetime
from dotenv import load_dotenv
from openai import OpenAI

# Load API key from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def get_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def abbreviate_to_nurse_talk(note):
    # Super simple "abbreviation" for demo purposes; expand as you wish!
    replacements = {
        "patient": "pt",
        "blood pressure": "BP",
        "shortness of breath": "SOB",
        "complains of": "c/o",
        "history of": "h/o",
        "shortness": "SOB"
    }
    for long, short in replacements.items():
        note = note.replace(long, short)
    return note

def ai_query(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
    )
    return response.choices[0].message.content.strip()

def collect_patient_info():
    print("\n--- Patient General Information ---")
    name = input("Patient Name: ")
    age = input("Age: ")
    gender = input("Gender: ")
    allergies = input("Known Allergies: ")
    other = input("Other relevant info: ")
    return {
        "name": name, "age": age, "gender": gender,
        "allergies": allergies, "other": other
    }

def symptom_checker(profile):
    print("\n--- Symptom Checker ---")
    symptom = input("Enter the main symptom: ")
    # Use OpenAI for top 3 suggestions (nurse-focused)
    prompt = (
        f"A {profile['age']} year old {profile['gender']} with the following main symptom: {symptom}. "
        "Give me the 3 most likely nursing-relevant causes (not dramatic WebMD stuff, just common issues):"
    )
    suggestions = ai_query(prompt)
    print("\nTop 3 likely causes:")
    print(suggestions)
    return f"{get_timestamp()} SYMPTOM: {symptom}\n{suggestions}\n"

def documentation_helper(profile):
    print("\n--- Documentation Helper ---")
    doc = input("Enter your documentation notes: ")
    abbr = abbreviate_to_nurse_talk(doc)
    print("\nAbbreviated (nurse talk) notes:\n", abbr)
    return f"{get_timestamp()} DOC: {abbr}\n"

def patient_education(profile):
    print("\n--- Patient Education ---")
    topic = input("Enter education topic (CHF, diabetes, meds, or custom): ")
    if topic.lower() in ["chf", "congestive heart failure"]:
        content = "CHF Education: Watch salt, daily weight, know warning signs (SOB, swelling), meds adherence."
    elif topic.lower() in ["diabetes"]:
        content = "Diabetes Ed: Monitor BG, proper insulin use, signs of hypo/hyperglycemia, healthy eating."
    else:
        prompt = (
            f"Summarize education for a nurse to give a patient on '{topic}', simple and clear, bullet points."
        )
        content = ai_query(prompt)
    print("\nPatient Education Points:\n", content)
    return f"{get_timestamp()} PT ED ({topic}):\n{content}\n"

def custom_question(profile):
    print("\n--- Ask CuraAI (Nurse AI Assistant) ---")
    query = input("Ask your question: ")
    answer = ai_query(query)
    print("\nCuraAI says:\n", answer)
    return ""  # Do not add CuraAI Q&A to notes for privacy

def main():
    print("Welcome to the Nurse Assistant CLI!\n")
    profile = collect_patient_info()
    notes = []

    while True:
        print("\nChoose a module:")
        print("1. Symptom Checker")
        print("2. Documentation Helper")
        print("3. Patient Education")
        print("4. CuraAI (Ask the AI anything)")
        print("5. View/Export Patient Notes")
        print("6. Quit")
        choice = input("Enter a number: ")

        if choice == "1":
            notes.append(symptom_checker(profile))
        elif choice == "2":
            notes.append(documentation_helper(profile))
        elif choice == "3":
            notes.append(patient_education(profile))
        elif choice == "4":
            custom_question(profile)
        elif choice == "5":
            print("\n--- Patient Notes ---")
            for note in notes:
                print(note)
            save = input("Save notes to file? (y/n): ")
            if save.lower() == "y":
                filename = f"notes_{profile['name']}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
                with open(filename, "w") as f:
                    for note in notes:
                        f.write(note + "\n")
                print(f"Notes saved to {filename}")
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()