# Task Distribution and Sequencing Rules

## 1. Sequencing
No task may begin until:
- architecture is complete  
- QA is complete  
- QA-of-QA is complete  

## 2. Parallelization
Builders may work in parallel IF:
- tasks do not depend on one another  
- sequencing rules allow it  

## 3. Integration Stage
After builders finish:
- Maturion performs integration QA  
- Maturion performs drift QA  
- Maturion checks inter-module links  

## 4. Human Approval
No module is considered “built” until:
- Maturion approves  
- Johan approves  
