#!/usr/bin/env python
"""
Azure OpenAI Embedding Example
This script demonstrates how to use the text-embedding-3-small model to generate embeddings.
"""

import os
import numpy as np
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "https://rootcoz.openai.azure.com/")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "YOUR_API_KEY")
EMBEDDING_DEPLOYMENT = "embedding3"  # text-embedding-3-small deployment name

# Configure the OpenAI client for Azure
client = openai.AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version="2023-12-01-preview",
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)

def get_embedding(text):
    """
    Generate an embedding for the given text using text-embedding-3-small.
    
    Args:
        text (str): The text to generate an embedding for
        
    Returns:
        list: The embedding vector
    """
    try:
        response = client.embeddings.create(
            model=EMBEDDING_DEPLOYMENT,
            input=text
        )
        
        # Extract the embedding vector
        embedding = response.data[0].embedding
        return embedding
    
    except Exception as e:
        print(f"Error generating embedding: {str(e)}")
        return None

def cosine_similarity(a, b):
    """
    Calculate the cosine similarity between two vectors.
    
    Args:
        a (list): First vector
        b (list): Second vector
        
    Returns:
        float: Cosine similarity (between -1 and 1)
    """
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def demonstrate_embeddings():
    """
    Demonstrate how to use embeddings for semantic similarity.
    """
    print("Generating embeddings for sample texts...")
    
    texts = [
        "I love machine learning and artificial intelligence",
        "Deep learning models are transforming the tech industry",
        "The weather is nice today",
        "It's sunny outside with clear skies",
        "Azure OpenAI provides powerful language models"
    ]
    
    # Generate embeddings for all texts
    embeddings = []
    for text in texts:
        embedding = get_embedding(text)
        if embedding:
            embeddings.append(embedding)
            print(f"Generated embedding for: '{text}'")
    
    print("\nCalculating similarities between texts:")
    
    # Calculate similarities between all pairs of texts
    for i in range(len(texts)):
        for j in range(i+1, len(texts)):
            similarity = cosine_similarity(embeddings[i], embeddings[j])
            print(f"Similarity between '{texts[i]}' and '{texts[j]}': {similarity:.4f}")

def main():
    """Main function to demonstrate Azure OpenAI embedding capabilities."""
    print("Azure OpenAI Embedding Example")
    print("-----------------------------")
    print(f"Using deployment: {EMBEDDING_DEPLOYMENT} (text-embedding-3-small)")
    print("This model generates 1536-dimensional embeddings for text")
    print()
    
    while True:
        print("\nOptions:")
        print("1. Generate embedding for a single text")
        print("2. Compare similarity between two texts")
        print("3. Run embedding demonstration")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == "1":
            text = input("Enter text to embed: ")
            embedding = get_embedding(text)
            if embedding:
                print(f"Generated {len(embedding)}-dimensional embedding vector")
                print(f"First 5 dimensions: {embedding[:5]}")
        
        elif choice == "2":
            text1 = input("Enter first text: ")
            text2 = input("Enter second text: ")
            
            embedding1 = get_embedding(text1)
            embedding2 = get_embedding(text2)
            
            if embedding1 and embedding2:
                similarity = cosine_similarity(embedding1, embedding2)
                print(f"Similarity between the two texts: {similarity:.4f}")
                print(f"The texts are {'similar' if similarity > 0.7 else 'not very similar'}")
        
        elif choice == "3":
            demonstrate_embeddings()
        
        elif choice == "4":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()
