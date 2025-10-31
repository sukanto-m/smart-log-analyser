import json
import argparse
import subprocess
from datetime import datetime

def analyse_with_llm(error_text):
    """Send error to LLM and get explanation"""

    prompt = f"""Analyze this log error and respond in this format:
SEVERITY: [LOW/MEDIUM/HIGH/CRITICAL]

EXPLANATION:
[Your explanation in simple terms]

Error: {error_text}"""

    result = subprocess.run(["ollama", "run", "llama3.2", prompt], 
                            capture_output=True, text=True)
    
    return result.stdout

def colorize_severity(text):
    """Add color to text based on severity level"""
    
    colors = {
        'LOW': '\033[92m',      # Green
        'MEDIUM': '\033[93m',   # Yellow
        'HIGH': '\033[91m',     # Red
        'CRITICAL': '\033[95m'  # Magenta
    }
    reset = '\033[0m'  # Reset color
    
    for severity, color in colors.items():
        if severity in text:
            colored_severity = f"{color}{severity}{reset}"
            text = text.replace(severity, colored_severity)
            break
    return text    


def generate_summary(errors):
    """Generate an overall summary of the errors"""

    "\n".join(errors)

    prompt = f"Here are multiple log errors. Provide a brief summary of the overall issue:\n\n{errors}"

    result = subprocess.run(["ollama", "run", "llama3.2", prompt], 
                            capture_output=True, text=True)
    
    return result.stdout

def save_report(filename, errors, analyses, summary):
    """Save the analysis report to a file"""
    
    with open(filename, "w") as file:
        file.write("=" * 80 + "\n")
        file.write("SMART LOG ANALYZER REPORT\n")
        file.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write("=" * 80 + "\n\n")

        # Write each error and its analysis
        for i, (error, analysis) in enumerate(zip(errors, analyses), 1):
            file.write(f"ERROR #{i}:\n")
            file.write(f"{error}\n\n")
            file.write(f"ANALYSIS:\n{analysis}\n")
            file.write("-" * 80 + "\n\n")
        
        # Write summary at the end
        file.write("OVERALL SUMMARY:\n")
        file.write(f"{summary}\n")

        file.write("\n" + "=" * 80 + "\n")
        file.write("END OF REPORT\n") 


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

    analyses = []

    for error in errors:
        print(f"Error: {error}")
        analysis = analyse_with_llm(error)
        colored_analysis = colorize_severity(analysis)
        analyses.append(analysis)
        print(f"Analysis: {colored_analysis}\n")
        print("-" * 80)  # Separator line

    print("Here is a summary of the errors found: \n")
    error_summary = generate_summary(errors)
    print(error_summary)

    report_filename = "log_analysis_report.txt"
    save_report(report_filename, errors, analyses, error_summary)
    print(f"\nReport saved to: {report_filename}")




if __name__ == "__main__":
    main()