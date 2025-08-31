# Agent Evaluation System

This system evaluates the performance of your construction project AI agent using a carefully curated test set while ensuring the agent cannot access the test set components in its RAG pipeline.

## 🎯 Purpose

The evaluation system is designed to:
1. **Test agent performance** on realistic construction tasks
2. **Prevent cheating** by ensuring the agent cannot access test set components during evaluation
3. **Provide detailed metrics** on generation accuracy
4. **Enable benchmarking** of different approaches

## 📁 Files Overview

### Core Files
- `generate_test_set.py` - Generates the test set from knowledge base
- `evaluate_agent.py` - Main evaluation script
- `test_evaluation.py` - Quick test script for verification
- `test_set.json` - Generated test set (50 components)
- `test_set_python.py` - Test set in Python format

### Output Files
- `evaluation_results.json` - Detailed evaluation results
- `test_set.json` - Test set in JSON format

## 🚀 Quick Start

### 1. Generate Test Set
```bash
python generate_test_set.py
```
This creates `test_set.json` with 50 random components from the knowledge base.

### 2. Run Full Evaluation
```bash
python evaluate_agent.py
```
This evaluates the agent on all test cases and saves results.

### 3. Quick Test (Optional)
```bash
python test_evaluation.py
```
This runs evaluation on just 3 test cases for quick verification.

## 🔧 How It Works

### Test Set Generation
1. **Filters components** with `"original_format": "new"` (reliable data)
2. **Randomly selects** 50 components using seed 42 (reproducible)
3. **Extracts key fields** for evaluation
4. **Uses actual "Opgave"** descriptions as input strings

### Evaluation Process
1. **Creates filtered agent** that cannot access test set components
2. **Runs each test case** through the agent's `generate_component_with_rag` method
3. **Compares generated values** against ground truth with tolerance settings
4. **Calculates success metrics** and error margins

### Anti-Cheating Mechanism
The `FilteredSemanticSearch` class wraps the original search system and filters out any components whose "Opgave" field matches test set descriptions before returning results to the agent.

## 📊 Evaluation Metrics

### Success Criteria
A test case is considered successful if **all fields** are within tolerance:

| Field | Tolerance | Description |
|-------|-----------|-------------|
| Admin | 10% | Administrative costs |
| Timer | 20% | Labor hours |
| Takst | 15% | Hourly rate |
| Kostpris_EP | 15% | Labor cost |
| Materialer | 20% | Material costs |
| Påslag_MAT | 25% | Material markup |
| Salgspris_MAT | 20% | Material sales price |
| UE | 20% | Subcontractor costs |
| Påslag_UE | 25% | Subcontractor markup |
| Salgspris_UE | 20% | Subcontractor sales price |
| Tilbud | 15% | Total price |

### Output Metrics
- **Success Rate**: Percentage of successful generations
- **Average Error**: Mean error across all fields
- **Detailed Results**: Per-test-case breakdown

## 📋 Test Set Characteristics

The test set includes:
- **50 components** from reliable sources (`"original_format": "new"`)
- **Diverse tasks**: Masonry, carpentry, electrical, plumbing, demolition
- **Realistic descriptions**: Actual "Opgave" field values
- **Wide price range**: 805 DKK to 50,895 DKK
- **Various complexity levels**: Simple tasks to complex projects

## 🔍 Understanding Results

### Success Rate Interpretation
- **80%+**: Excellent performance
- **60-80%**: Good performance
- **40-60%**: Moderate performance
- **<40%**: Needs improvement

### Error Analysis
- **Low average error** (<10%): Agent generates accurate values
- **High average error** (>20%): Agent struggles with estimation
- **Field-specific errors**: Identify problematic areas

## 🛠️ Customization

### Adjusting Tolerance
Modify `tolerance_settings` in `AgentEvaluator.__init__()`:
```python
self.tolerance_settings = {
    'Admin': 0.1,      # 10% tolerance
    'Timer': 0.2,      # 20% tolerance
    # ... adjust as needed
}
```

### Changing Test Set Size
Modify the `random.sample()` call in `generate_test_set.py`:
```python
selected_components = random.sample(new_format_components, 100)  # Change 50 to desired size
```

### Using Different Quality Settings
Modify the `use_high_quality_only` parameter in `evaluate_single_test()`:
```python
generated_component = agent.generate_component_with_rag(description, use_high_quality_only=False)
```

## ⚠️ Important Notes

### Environment Requirements
- Ensure your virtual environment is activated
- Set `OPENAI_API_KEY` environment variable
- Install all required packages: `pip install -r requirements.txt`

### Fair Evaluation
- The evaluation ensures the agent cannot access test set components
- This prevents "cheating" through exact matches
- Results reflect true generation capability

### Rate Limiting
- The script includes 1-second delays between API calls
- For large test sets, consider increasing delays if needed
- Monitor API usage to avoid rate limits

## 📈 Benchmarking Different Approaches

To compare different approaches:

1. **Modify agent parameters** (e.g., different prompts, models)
2. **Run evaluation** with each configuration
3. **Compare success rates** and error margins
4. **Analyze detailed results** for specific improvements

Example comparison:
```bash
# Baseline evaluation
python evaluate_agent.py
# Results saved to evaluation_results.json

# Modified agent evaluation
# (modify agent code, then run again)
python evaluate_agent.py
# Results saved to evaluation_results.json (overwrites)
```

## 🐛 Troubleshooting

### Common Issues
1. **"test_set.json not found"**: Run `generate_test_set.py` first
2. **Import errors**: Ensure virtual environment is activated
3. **API errors**: Check `OPENAI_API_KEY` and rate limits
4. **Memory issues**: Reduce test set size for testing

### Debug Mode
Add debug prints to `evaluate_agent.py` for detailed logging:
```python
print(f"DEBUG: Generated component: {generated_component}")
```

## 📝 Example Output

```
🚀 Starting Agent Evaluation
📊 Test Set Size: 50
============================================================
🔧 Creating filtered agent (excluding test set components)...

--- Test Case 1: Maling af underboens loft... ---
Success: True
Error Margin: 5.23%
Generated Tilbud: 3685.50
Ground Truth Tilbud: 3510.00
Notes: All fields within tolerance

📈 EVALUATION SUMMARY
============================================================
Total Tests: 50
Successful Tests: 42
Success Rate: 84.00%
Average Error: 12.45%

📋 Detailed Results:
✅ Test 1: Maling af underboens loft...
✅ Test 2: Nye indfatninger på inderside af dør...
❌ Test 3: Nedrivning af brusevæg, stål og glasbyggesten...
   Notes: Timer: GT=2.0, Gen=4.5, Error=125.00%
```

This evaluation system provides a robust, fair, and comprehensive way to assess your agent's performance on realistic construction tasks.
