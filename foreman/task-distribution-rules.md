# Task Distribution and Sequencing Rules

## 1. Sequencing
No task may begin until:
- architecture is complete  
- QA is complete  
- QA-of-QA is complete
- **Memory Fabric is validated and ready**

## 2. Parallelization
Builders may work in parallel IF:
- tasks do not depend on one another  
- sequencing rules allow it  

## 3. Integration Stage
After builders finish:
- Maturion performs integration QA  
- Maturion performs drift QA  
- Maturion checks inter-module links
- **Maturion writes build outcomes to memory**

## 4. Human Approval
No module is considered “built” until:
- Maturion approves  
- Johan approves  

## 5. Memory Integration

### Pre-Build Memory Requirements
Before any task distribution:
- Load relevant memories (architectural decisions, past build outcomes, learnings)
- Validate memory readiness
- Ensure memory write capability

### During Build Memory Usage
- Consult memory for task dependencies
- Reference historical build patterns
- Check for known issues or gotchas
- Use memory to inform sequencing decisions

### Post-Build Memory Recording
- Record all task outcomes
- Log builder coordination results
- Document integration validations
- Capture lessons learned

### Memory as Readiness Gate
**Task distribution cannot begin until Memory Fabric passes validation.**
