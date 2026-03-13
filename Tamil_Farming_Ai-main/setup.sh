#!/bin/bash
echo ""
echo "🌾 உழவன் குரல் — Setup"
echo "========================"
echo ""
echo "📦 Installing Python dependencies..."
pip3 install gtts faiss-cpu sentence-transformers requests deep-translator --break-system-packages

echo ""
echo "📚 Building FAISS knowledge index..."
cd "$(dirname "$0")"
python3 build_index.py
echo "✅ FAISS index built!"

echo ""
echo "📦 Installing Node dependencies..."
npm install

echo ""
echo "✅ Setup complete!"
echo "   Now run: npm start"
echo "   Then open: http://localhost:3001"
echo ""
