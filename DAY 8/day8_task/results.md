# Day 8 – College Helpdesk Agent

## 1. Project Objective
Extend the College Helpdesk Agent with placement-policy retrieval, exam eligibility checking, and a relevance guard that avoids unsupported answers.

## 2. Test Results

Run `python task_agent.py`, then complete the table with the actual tool calls and answers printed by your run.

| # | Tools called (in order) | Agent's answer (short) | Correct? (Y/N) | If N, why? |
|---|---|---|---|---|
| 1 | Fill from run | Fill from run | | |
| 2 | Fill from run | Fill from run | | |
| 3 | Fill from run | Fill from run | | |
| 4 | Fill from run | Fill from run | | |
| 5 | Fill from run | Fill from run | | |

## 3. Configuration
- Model used: Fill in actual model
- Embedding model: Fill in actual model
- MAX_DISTANCE: Fill in selected threshold

## 4. Similarity Scores
- Placement question scores: Fill in actual scores from `python 2_search.py`
- France question scores: Fill in actual scores from `python 2_search.py`
- Reason for threshold: Explain how the measured scores informed the selected value.

## 5. Observations
Record whether the agent used the expected tools, calculated fees correctly, retained conversation context for Question 4, and rejected the unrelated France question.

Report mistakes honestly. A model making a mistake does not mean the test report is invalid; explain the likely cause.

## 6. Conclusion
Summarize the improvements to retrieval, tool use, and unsupported-answer handling.
