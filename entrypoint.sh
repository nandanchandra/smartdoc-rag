#!/bin/sh

/bin/ollama serve &
pid=$!

echo "🚀 Ollama is running..."

echo "📥 Downloading mistral model..."

ollama pull mistral

echo "✅ mistral model downloaded successfully!"

ollama run mistral

echo "🚀 mistral model running!"

wait $pid