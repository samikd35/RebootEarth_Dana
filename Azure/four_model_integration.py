#!/usr/bin/env python
"""
Azure OpenAI Four-Model Integration Example
This script demonstrates how to use all four Azure OpenAI models with the same API key.
"""

import os
import openai
from dotenv import load_dotenv
import time

# Load environment variables from .env file
load_dotenv()

# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "https://rootcoz.openai.azure.com/")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "YOUR_API_KEY")

# Model deployment names
GPT41_DEPLOYMENT = "gpt41"          # GPT-4.1 deployment
GPT41_NANO_DEPLOYMENT = "gpt41nano" # GPT-4.1-nano deployment
GPT41_MINI_DEPLOYMENT = "gpt41mini" # GPT-4.1-mini deployment
EMBEDDING_DEPLOYMENT = "embedding3"  # text-embedding-3-small deployment

# Configure the OpenAI client for Azure
client = openai.AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version="2023-12-01-preview",
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)

def generate_response(prompt, model_deployment, max_tokens=1000):
    """
    Generate a response using the specified Azure OpenAI model.
    
    Args:
        prompt (str): The user's input prompt
        model_deployment (str): The deployment name of the model to use
        max_tokens (int): Maximum number of tokens to generate
        
    Returns:
        tuple: (response_text, response_time)
    """
    try:
        start_time = time.time()
        
        # Call the Azure OpenAI API with the specified model deployment
        response = client.chat.completions.create(
            model=model_deployment,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7,
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        # Extract and return the generated text
        return response.choices[0].message.content.strip(), response_time
    
    except Exception as e:
        return f"Error generating response: {str(e)}", 0

def get_embedding(text):
    """
    Generate an embedding for the given text using text-embedding-3-small.
    
    Args:
        text (str): The text to generate an embedding for
        
    Returns:
        tuple: (embedding_vector, response_time)
    """
    try:
        start_time = time.time()
        
        response = client.embeddings.create(
            model=EMBEDDING_DEPLOYMENT,
            input=text
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        # Extract the embedding vector
        embedding = response.data[0].embedding
        return embedding, response_time
    
    except Exception as e:
        return None, 0

def compare_all_chat_models(prompt):
    """
    Compare responses from all three chat models for the same prompt.
    
    Args:
        prompt (str): The user's input prompt
    """
    print(f"Prompt: {prompt}")
    print("=" * 80)
    
    models = [
        (GPT41_DEPLOYMENT, "GPT-4.1", "5000 capacity"),
        (GPT41_NANO_DEPLOYMENT, "GPT-4.1-nano", "150000 capacity"),
        (GPT41_MINI_DEPLOYMENT, "GPT-4.1-mini", "50 capacity")
    ]
    
    for deployment, model_name, capacity in models:
        print(f"\n🤖 {model_name} ({capacity}):")
        print("-" * 40)
        
        response, response_time = generate_response(prompt, deployment)
        print(f"Response: {response}")
        print(f"⏱️ Response time: {response_time:.2f} seconds")

def demonstrate_embedding_with_chat(text):
    """
    Demonstrate embedding generation and then use the embedding info with chat models.
    
    Args:
        text (str): The text to analyze
    """
    print(f"Analyzing text: '{text}'")
    print("=" * 80)
    
    # Generate embedding
    print("\n📊 Generating embedding...")
    embedding, embed_time = get_embedding(text)
    
    if embedding:
        print(f"✅ Generated {len(embedding)}-dimensional embedding")
        print(f"⏱️ Embedding time: {embed_time:.2f} seconds")
        print(f"First 5 dimensions: {embedding[:5]}")
        
        # Use chat models to analyze the text
        analysis_prompt = f"Analyze this text and provide insights: '{text}'"
        print(f"\n🔍 Getting analysis from chat models...")
        compare_all_chat_models(analysis_prompt)
    else:
        print("❌ Failed to generate embedding")

def main():
    """Main function to demonstrate Azure OpenAI four-model integration."""
    print("Azure OpenAI Four-Model Integration Example")
    print("==========================================")
    print("Available Models:")
    print(f"1. {GPT41_DEPLOYMENT} (GPT-4.1) - 5000 capacity")
    print(f"2. {GPT41_NANO_DEPLOYMENT} (GPT-4.1-nano) - 150000 capacity")
    print(f"3. {GPT41_MINI_DEPLOYMENT} (GPT-4.1-mini) - 50 capacity")
    print(f"4. {EMBEDDING_DEPLOYMENT} (text-embedding-3-small) - 9307 capacity")
    print("\nAll models use the same API key from the same Azure OpenAI resource.")
    print("\nOptions:")
    print("1. Use GPT-4.1")
    print("2. Use GPT-4.1-nano")
    print("3. Use GPT-4.1-mini")
    print("4. Compare all chat models")
    print("5. Generate embedding")
    print("6. Analyze text with embedding + chat models")
    print("7. Exit")
    print()
    
    while True:
        try:
            choice = input("Enter your choice (1-7): ")
            
            if choice == "7":
                print("Goodbye!")
                break
            
            if choice in ["1", "2", "3"]:
                prompt = input("Enter your prompt: ")
                
                if choice == "1":
                    model_deployment = GPT41_DEPLOYMENT
                    model_name = "GPT-4.1"
                elif choice == "2":
                    model_deployment = GPT41_NANO_DEPLOYMENT
                    model_name = "GPT-4.1-nano"
                else:  # choice == "3"
                    model_deployment = GPT41_MINI_DEPLOYMENT
                    model_name = "GPT-4.1-mini"
                
                print(f"\nGenerating response using {model_name}...")
                response, response_time = generate_response(prompt, model_deployment)
                print(f"Response: {response}")
                print(f"⏱️ Response time: {response_time:.2f} seconds\n")
            
            elif choice == "4":
                prompt = input("Enter your prompt: ")
                compare_all_chat_models(prompt)
                print()
            
            elif choice == "5":
                text = input("Enter text to embed: ")
                embedding, embed_time = get_embedding(text)
                if embedding:
                    print(f"Generated {len(embedding)}-dimensional embedding vector")
                    print(f"⏱️ Embedding time: {embed_time:.2f} seconds")
                    print(f"First 10 dimensions: {embedding[:10]}")
                print()
            
            elif choice == "6":
                text = input("Enter text to analyze: ")
                demonstrate_embedding_with_chat(text)
                print()
            
            else:
                print("Invalid choice. Please enter a number between 1 and 7.")
        
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
