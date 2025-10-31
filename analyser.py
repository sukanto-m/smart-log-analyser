import json
import argparse
import subprocess

def analyse_with_llm(error_text):
    """Send error to LLM and get explanation"""

    prompt = f"Explain this log error in simple terms: {error_text}"

    result = subprocess.run(["ollama", "run", "llama3.2", prompt], 
                            capture_output=True, text=True)
    
    return result.stdout


def generate_summary(errors):
    """Generate an overall summary of the errors"""

    "\n".join(errors)

    prompt = f"Here are multiple log errors. Provide a brief summary of the overall issue:\n\n{errors}"

    result = subprocess.run(["ollama", "run", "llama3.2", prompt], 
                            capture_output=True, text=True)
    
    return result.stdout


def main():
    """
    
    Parse command line arguments and run Llamma

    """

    parser = argparse.ArgumentParser(description="Analyze log files with AI")

    parser.add_argument("filename", help="Path to the log file")

    args = parser.parse_args()

    filename = args.filename

    error_keywords = ["ERROR", "FATAL", "Exception", "CRITICAL"]

    with open(filename, 'r') as file:
        errors = []
        for line in file:
            if any(keyword in line for keyword in error_keywords):
                #print(f"Found error: {line}") #for testing
                errors.append(line.strip())
    
    # After collecting errors
    print(f"\nFound {len(errors)} error(s). Analyzing with LLM...\n")

    for error in errors:
        print(f"Error: {error}")
        analysis = analyse_with_llm(error)
        print(f"Analysis: {analysis}\n")
        print("-" * 80)  # Separator line

    print("Here is a summary of the errors found: \n")
    error_summary = generate_summary(errors)
    print(error_summary)    




if __name__ == "__main__":
    main()