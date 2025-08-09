#!/usr/bin/env python
"""
Azure OpenAI Multi-Model Integration Example
This script demonstrates how to use multiple Azure OpenAI models with the same API key.
"""

import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "https://rootcoz.openai.azure.com/")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "YOUR_API_KEY")

# Model deployment names
GPT41_DEPLOYMENT = "gpt41"          # GPT-4.1 deployment (5000 capacity)
GPT41_NANO_DEPLOYMENT = "gpt41nano" # GPT-4.1-nano deployment (150000 capacity)
GPT41_MINI_DEPLOYMENT = "gpt41mini" # GPT-4.1-mini deployment (50 capacity)

# Configure the OpenAI client for Azure
client = openai.AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version="2023-12-01-preview",
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)

def generate_response(prompt, model_deployment=GPT41_DEPLOYMENT, max_tokens=8000):
    """
    Generate a response using the specified Azure OpenAI model.
    
    Args:
        prompt (str): The user's input prompt
        model_deployment (str): The deployment name of the model to use
        max_tokens (int): Maximum number of tokens to generate
        
    Returns:
        str: The generated response
    """
    try:
        # Call the Azure OpenAI API with the specified model deployment
        response = client.chat.completions.create(
            model=model_deployment,  # Use the deployment name, not the model name
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7,
        )
        
        # Extract and return the generated text
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"Error generating response: {str(e)}"

def compare_models(prompt):
    """
    Compare responses from all three models for the same prompt.
    
    Args:
        prompt (str): The user's input prompt
        
    Returns:
        tuple: Responses from all three models
    """
    print(f"Prompt: {prompt}")
    print("\nGenerating responses from all models...\n")
    
    # Get response from GPT-4.1
    print(f"Using {GPT41_DEPLOYMENT} (GPT-4.1):")
    gpt41_response = generate_response(prompt, GPT41_DEPLOYMENT)
    print(f"Response: {gpt41_response}\n")
    
    # Get response from GPT-4.1-nano
    print(f"Using {GPT41_NANO_DEPLOYMENT} (GPT-4.1-nano):")
    gpt41_nano_response = generate_response(prompt, GPT41_NANO_DEPLOYMENT)
    print(f"Response: {gpt41_nano_response}\n")
    
    # Get response from GPT-4.1-mini
    print(f"Using {GPT41_MINI_DEPLOYMENT} (GPT-4.1-mini):")
    gpt41_mini_response = generate_response(prompt, GPT41_MINI_DEPLOYMENT)
    print(f"Response: {gpt41_mini_response}\n")
    
    return gpt41_response, gpt41_nano_response, gpt41_mini_response

def main():
    """Main function to demonstrate Azure OpenAI multi-model integration."""
    print("Azure OpenAI Multi-Model Integration Example")
    print("-------------------------------------------")
    print(f"Model 1: {GPT41_DEPLOYMENT} (GPT-4.1) - 5000 capacity")
    print(f"Model 2: {GPT41_NANO_DEPLOYMENT} (GPT-4.1-nano) - 150000 capacity")
    print(f"Model 3: {GPT41_MINI_DEPLOYMENT} (GPT-4.1-mini) - 50 capacity")
    print("All models use the same API key from the same Azure OpenAI resource.")
    print("\nOptions:")
    print("1. Use GPT-4.1")
    print("2. Use GPT-4.1-nano")
    print("3. Use GPT-4.1-mini")
    print("4. Compare all models")
    print("5. Exit")
    print()
    
    while True:
        try:
            choice = input("Enter your choice (1-5): ")
            
            if choice == "5":
                print("Goodbye!")
                break
            
            prompt = input("Enter your prompt: ")
            
            if choice == "1":
                print("\nGenerating response using GPT-4.1...\n")
                response = generate_response(prompt, GPT41_DEPLOYMENT)
                print(f"Response: {response}\n")
            elif choice == "2":
                print("\nGenerating response using GPT-4.1-nano...\n")
                response = generate_response(prompt, GPT41_NANO_DEPLOYMENT)
                print(f"Response: {response}\n")
            elif choice == "3":
                print("\nGenerating response using GPT-4.1-mini...\n")
                response = generate_response(prompt, GPT41_MINI_DEPLOYMENT)
                print(f"Response: {response}\n")
            elif choice == "4":
                compare_models(prompt)
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")
        
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
