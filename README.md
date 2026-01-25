# RLCEF Code Agent: Self-Fixing Code via Test Execution Feedback

**Inspired by [Poolside AI](https://poolside.ai)'s approach to autonomous code improvement**

Author: Mayank Mahawar ([LinkedIn](https://www.linkedin.com/in/mayank-mahawar-46032a4b/))  

---

## What This Does

Paste broken Python code + tests → AI fixes it automatically by:
1. Running real tests in Docker sandbox
2. Reading actual error logs
3. Generating targeted fixes
4. Repeating until all tests pass ✅

**Not autocomplete, not one-shot generation** – iterative debugging via execution feedback loop.

---

## Demo Example

**Input:**
```python
def factorial(n):
    return n * factorial(n)  # Bug: infinite recursion

# Tests
assert factorial(5) == 120
assert factorial(0) == 1

Agent Process:

Attempt 1: Runs → RecursionError detected
Attempt 2: Adds base case → Tests pass ✅
Fixed in 2 iterations (12 seconds)

Architecture

buggy_code + tests 
  ↓
LLM (Qwen 2.5 Coder via Groq)
  ↓
Docker Sandbox (pytest execution)
  ↓
feedback (errors/logs)
  ↓
LLM (with feedback history)
  ↓
... loop max 5x ...
  ↓
fixed_code ✅

Tech Stack
LLM: Qwen 2.5 Coder 32B via Groq API (400 tok/sec, $0.27/1M)

Sandbox: Docker + pytest (isolated, timeout-protected)

Execution Feedback: Real test results + error traces

Future: RAG for codebase context (Week 2)

Quick Start

# Clone
git clone https://github.com/mayankiitkgp/poolside-rlcef-agent.git
cd poolside-rlcef-agent

# Install
pip install -r requirements.txt

# Configure (add your keys)
cp .env.example .env

# Run agent
python src/agent/rlcef_loop.py --code examples/buggy_factorial.py --tests examples/test_factorial.py

# Or use Streamlit UI
streamlit run src/ui/app.py
Roadmap
 Tonight (Jan 25): Core RLCEF loop + sandbox

 Week 2: Multi-file fixes, codebase RAG retrieval

 Week 3: LoRA fine-tune on HR tech execution traces

 Month 2: VSCode extension

Relation to Poolside
Poolside trains models with RLCEF at massive scale (millions of repos, GPU clusters).

This project: Replicates their inference-time behavior (execution feedback loop) using hosted APIs – proves the mechanism works without training infrastructure.



