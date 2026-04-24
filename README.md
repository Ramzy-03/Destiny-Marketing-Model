# 🚀 Destiny – Autonomous AI Digital Marketing Manager

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> **An autonomous AI-powered digital marketing agent** that plans, creates, executes, and continuously improves full marketing campaigns across multiple platforms.

---

## 🎯 Executive Summary

**Destiny** is a graduation project in **AI Systems Engineering** that demonstrates a real-world implementation of an **autonomous agentic AI system**.

Unlike traditional automation tools or chatbots, Destiny operates as a **decision-making marketing manager** that can:

- Understand business goals  
- Plan full marketing strategies  
- Generate high-quality content  
- Execute campaigns across platforms  
- Learn from results and improve over time  

The system integrates **machine learning**, **LLM-based reasoning**, and **persistent memory** into a single intelligent workflow.

---

## ✨ Key Features

| Feature | Description |
|--------|------------|
| 🤖 Autonomous Agent | Plans, executes, and evaluates tasks without human intervention |
| 🧠 Hybrid Learning System | Random Forest models + real-time adaptive learning |
| ✍️ AI Content Generation | Claude API for blogs, ads, emails, and social content |
| 📱 Multi-Platform Execution | Facebook, Instagram, LinkedIn, Twitter/X |
| 🚀 Dual Modes | Quick Action (single task) / Campaign Mode (full automation) |
| 📊 Analytics Engine | Predicts engagement, conversion, ROI |
| 💾 Persistent Memory | JSON-based learning across sessions |
| 🔧 Tool-Based Architecture | 17+ modular marketing tools |

---

---

## 🧠 How It Works (Simple Explanation)

1. User provides a **goal** (e.g., "Promote clothing brand")
2. Agent:
   - Breaks it into tasks (planning)
   - Selects tools (tool registry)
   - Generates content (Claude API)
   - Executes posts (social APIs)
3. ML system:
   - Predicts performance
   - Learns from results
4. Memory system:
   - Stores outcomes
   - Improves future decisions

---

## 📦 Installation

### 🔧 Prerequisites
- Python 3.8 – 3.11
- pip
  
### Arch 

destiny-agent/
│
├── agent.py                      # Core autonomous agent
├── HybridLearningSystemLocal.py  # ML training + predictions
├── tools.py                      # Tool registry (17+ tools)
├── memory.py                     # Persistent learning memory
├── app.py                        # Streamlit dashboard
│
├── data/                         # Training datasets
├── models/                       # Saved ML models
├── memory_store/                 # JSON memory logs
└── utils/                        # Helper functions

### 📥 Setup

```bash
git clone https://github.com/yourusername/destiny-agent.git
cd destiny-agent
pip install -r requirements.txt
python fixer.py
streamlit run app.py
---
