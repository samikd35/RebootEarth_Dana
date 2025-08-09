#!/usr/bin/env python
"""
Azure OpenAI Integration Example
This script demonstrates how to use the Azure OpenAI service with the deployed GPT-4.1 model.
"""

import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env file (if it exists)
load_dotenv()

# Azure OpenAI Configuration
# Replace these with your actual values or set them as environment variables
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "https://rootcoz.openai.azure.com/")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "YOUR_API_KEY")  # Replace with your actual API key
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt41")  # The deployment name you created

# Configure the OpenAI client for Azure
client = openai.AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version="2023-12-01-preview",  # Use the latest API version
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)

def generate_response(prompt, max_tokens=8000):
    """
    Generate a response using the Azure OpenAI GPT-4.1 model.
    
    Args:
        prompt (str): The user's input prompt
        max_tokens (int): Maximum number of tokens to generate
        
    Returns:
        str: The generated response
    """
    try:
        # Call the Azure OpenAI API
        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT_NAME,  # Use the deployment name, not the model name
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7,
            # With higher token limits, we can process longer conversations
            # and generate more detailed responses
        )
        
        # Extract and return the generated text
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"Error generating response: {str(e)}"

def main():
    """Main function to demonstrate Azure OpenAI integration."""
    print("Azure OpenAI Integration Example")
    print("--------------------------------")
    print("Type 'exit' to quit the program.")
    print("This application is using GPT-4.1 with a 800,000 tokens/minute limit")
    print()
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        
        print("\nGenerating response...\n")
        response = generate_response(user_input)
        print(f"AI: {response}\n")

if __name__ == "__main__":
    main()
