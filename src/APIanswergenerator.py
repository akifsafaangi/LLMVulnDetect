import os
import openai

# Set your OpenAI API key
openai.api_key = "sk-..."

# Generates a solution based on the prompt file using GPT-4
def generate_solution_from_prompt(prompt_path):
    exploit_id = os.path.basename(prompt_path).split("_")[1].split(".")[0]
    folder = os.path.dirname(prompt_path)
    solution_path = os.path.join(folder, f"{exploit_id}_solution.txt")

    # Read the prompt content
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt = f.read()

    try:
        # Send the prompt to GPT-4
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a cybersecurity expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )
        solution = response['choices'][0]['message']['content']

        # Save the response to a solution file
        with open(solution_path, "w", encoding="utf-8") as out:
            out.write(solution)

        print(f"[✓] Solution saved: {solution_path}")
    except Exception as e:
        print(f"[!] Error processing {prompt_path}: {e}")

# Scans all prompt files in the exploit directory and processes them
def run_on_all_prompts(base_folder="exploits"):
    for service_dir in os.listdir(base_folder):
        service_path = os.path.join(base_folder, service_dir)
        if not os.path.isdir(service_path):
            continue

        for exploit_dir in os.listdir(service_path):
            exploit_path = os.path.join(service_path, exploit_dir)
            if not os.path.isdir(exploit_path):
                continue

            prompt_file = os.path.join(exploit_path, f"prompt_{exploit_dir}.txt")
            if os.path.exists(prompt_file):
                generate_solution_from_prompt(prompt_file)

# Main execution
if __name__ == "__main__":
    run_on_all_prompts()
