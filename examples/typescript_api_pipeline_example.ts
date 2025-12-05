/**
 * Memory Integration Example - TypeScript Chat/API Pipeline
 * 
 * This example demonstrates how to integrate the Unified Memory Fabric
 * into a TypeScript/JavaScript-based application (e.g., Next.js API routes).
 * 
 * This pattern is suitable for:
 * - Vercel-hosted Foreman app
 * - Next.js API routes
 * - Node.js services
 * - Express/Fastify backends
 */

import { loadMemory, appendMemory, formatMemoriesForPrompt } from '../lib/memory/client';
import type { MemoryEntry } from '../lib/memory/client';

/**
 * Example 1: Chat/Command Processing Endpoint
 * 
 * This shows how to integrate memory into an API route handler.
 * Suitable for Next.js API routes: /api/foreman/chat
 */
export async function handleChatCommand(
  userInput: string,
  context: {
    userId?: string;
    taskType?: string;
    actionName?: string;
    isSignificant?: boolean;
  }
): Promise<{ status: string; message: string; memoriesUsed: number }> {
  
  console.log('='.repeat(60));
  console.log('Chat Command Processing with Memory Integration');
  console.log('='.repeat(60));
  
  // Step 1: Load relevant memories BEFORE processing
  console.log('\nStep 1: Loading memory context...');
  
  const scopes = ['global', 'foreman'];
  const tags = ['governance', 'architecture'];
  
  // Add context-specific tags
  if (context.taskType) {
    tags.push(context.taskType);
  }
  
  const memories = await loadMemory(scopes, tags, 'high');
  
  console.log(`✓ Loaded ${memories.length} relevant memories\n`);
  
  // Step 2: Format memories for system prompt
  console.log('Step 2: Enriching system prompt with memory context...');
  
  const memoryContext = formatMemoriesForPrompt(memories, 10);
  
  const baseSystemPrompt = `You are Maturion Foreman, the governance and orchestration AI.

Your responsibilities:
- Enforce architecture and governance rules
- Coordinate builder agents
- Ensure one-time build correctness
- Maintain zero regression
- Validate all work against standards

You MUST respect all memories provided below.
`;
  
  const enrichedSystemPrompt = `${baseSystemPrompt}\n\n${memoryContext}`;
  
  console.log(`✓ System prompt enriched (${enrichedSystemPrompt.length} characters)\n`);
  
  // Step 3: Process the command
  // In real implementation, this would call OpenAI API with enriched prompt
  console.log('Step 3: Processing command...');
  console.log(`User Input: ${userInput}\n`);
  
  // Simulate AI processing
  const response = {
    status: 'success',
    message: `Processed command with ${memories.length} memory entries as context`,
    memoriesUsed: memories.length
  };
  
  console.log('✓ Command processed\n');
  
  // Step 4: Write memory entry for significant actions
  console.log('Step 4: Writing memory entry for this action...');
  
  if (context.isSignificant) {
    const entryId = await appendMemory({
      scope: 'foreman',
      title: `Chat Command: ${context.actionName || 'Unknown'}`,
      summary: `Processed user command: ${userInput.substring(0, 100)}`,
      importance: 'low',
      tags: ['chat', 'command', 'governance'],
      details: {
        user_input: userInput.substring(0, 200), // Truncate for privacy
        memories_used: memories.length,
        context
      }
    });
    
    console.log(`✓ Memory entry created: ${entryId}\n`);
  } else {
    console.log('ℹ️  Command not significant enough for memory entry\n');
  }
  
  console.log('='.repeat(60));
  console.log('Chat Command Processing Complete');
  console.log('='.repeat(60) + '\n');
  
  return response;
}

/**
 * Example 2: Next.js API Route Handler
 * 
 * File: /pages/api/foreman/chat.ts or /app/api/foreman/chat/route.ts
 */
export async function chatApiHandler(req: any, res: any) {
  try {
    // Parse request
    const { message, context } = req.body;
    
    // Process with memory integration
    const result = await handleChatCommand(message, context || {});
    
    // Return response
    res.status(200).json({
      success: true,
      data: result
    });
    
  } catch (error) {
    console.error('Chat API Error:', error);
    res.status(500).json({
      success: false,
      error: 'Internal server error'
    });
  }
}

/**
 * Example 3: Build Wave Planning with Memory
 * 
 * This shows how to use memory when planning build sequences.
 */
export async function planBuildWave(modules: string[]): Promise<{
  sequence: string[];
  reasoning: string;
  memoriesApplied: number;
}> {
  
  console.log('\n' + '='.repeat(60));
  console.log('Build Wave Planning with Memory Integration');
  console.log('='.repeat(60) + '\n');
  
  // Load build-related memories
  console.log('Loading build and sequencing memories...');
  
  const memories = await loadMemory(
    ['global', 'foreman'],
    ['build', 'sequence', 'governance'],
    'medium'
  );
  
  console.log(`✓ Loaded ${memories.length} relevant memories\n`);
  
  // Extract learned patterns from memories
  const sequencingPatterns: string[] = [];
  
  for (const memory of memories) {
    if (memory.tags.includes('sequence') && memory.details?.constraints) {
      sequencingPatterns.push(...memory.details.constraints);
    }
  }
  
  console.log(`Found ${sequencingPatterns.length} sequencing patterns in memory\n`);
  
  // Apply patterns to plan sequence (simplified example)
  // Real implementation would use AI with memory context
  
  const sequence = [...modules].sort(); // Simplified
  const reasoning = `Applied ${sequencingPatterns.length} learned sequencing patterns from memory`;
  
  console.log(`Planned sequence: ${sequence.join(' → ')}\n`);
  
  // Write planning decision to memory
  await appendMemory({
    scope: 'foreman',
    title: 'Build Wave Planned',
    summary: `Planned build sequence for modules: ${modules.join(', ')}`,
    importance: 'medium',
    tags: ['build', 'planning', 'sequence'],
    details: {
      modules,
      sequence,
      patterns_applied: sequencingPatterns.length,
      reasoning
    }
  });
  
  console.log('✓ Planning decision recorded in memory\n');
  
  return {
    sequence,
    reasoning,
    memoriesApplied: memories.length
  };
}

/**
 * Example 4: QA Validation with Memory Context
 * 
 * This shows how to use memory when validating QA coverage.
 */
export async function validateQACoverage(
  module: string,
  coverageReport: any
): Promise<{
  passed: boolean;
  issues: string[];
  recommendations: string[];
}> {
  
  console.log('\n' + '='.repeat(60));
  console.log('QA Validation with Memory Integration');
  console.log('='.repeat(60) + '\n');
  
  // Load QA-related memories
  console.log('Loading QA governance memories...');
  
  const memories = await loadMemory(
    ['global', 'foreman'],
    ['qa', 'testing', 'coverage'],
    'medium'
  );
  
  console.log(`✓ Loaded ${memories.length} QA memories\n`);
  
  // Extract QA requirements from memories
  const qaRequirements: string[] = [];
  
  for (const memory of memories) {
    if (memory.tags.includes('qa') && memory.details?.constraints) {
      qaRequirements.push(...memory.details.constraints);
    }
  }
  
  console.log(`Found ${qaRequirements.length} QA requirements in memory\n`);
  
  // Validate coverage against memory (simplified)
  const issues: string[] = [];
  const recommendations: string[] = [];
  
  // Example validation
  if (coverageReport.lineCoverage < 80) {
    issues.push('Line coverage below 80% threshold (found in memory)');
    recommendations.push('Increase unit test coverage');
  }
  
  const passed = issues.length === 0;
  
  console.log(`Validation ${passed ? 'PASSED' : 'FAILED'} with ${issues.length} issues\n`);
  
  // Write validation result to memory if there were issues
  if (!passed) {
    await appendMemory({
      scope: 'foreman',
      title: `QA Validation Failed: ${module}`,
      summary: `QA coverage validation failed with ${issues.length} issues`,
      importance: 'medium',
      tags: ['qa', 'validation', 'failure'],
      details: {
        module,
        issues,
        coverage: coverageReport.lineCoverage,
        requirements_checked: qaRequirements.length
      }
    });
    
    console.log('✓ Validation failure recorded in memory\n');
  }
  
  return { passed, issues, recommendations };
}

/**
 * Demo runner - Run all examples
 */
async function runExamples() {
  console.log('\n' + '='.repeat(60));
  console.log('MEMORY INTEGRATION EXAMPLES - TYPESCRIPT/JAVASCRIPT');
  console.log('='.repeat(60));
  
  try {
    // Example 1: Governance command
    console.log('\n' + '#'.repeat(60));
    console.log('# EXAMPLE 1: Governance Decision');
    console.log('#'.repeat(60));
    
    await handleChatCommand(
      'Approve the Asset module architecture for build',
      {
        taskType: 'architecture',
        actionName: 'Architecture Approval',
        isSignificant: true
      }
    );
    
    // Example 2: Build wave planning
    console.log('\n' + '#'.repeat(60));
    console.log('# EXAMPLE 2: Build Wave Planning');
    console.log('#'.repeat(60));
    
    await planBuildWave(['Asset', 'Threat', 'Control']);
    
    // Example 3: QA validation
    console.log('\n' + '#'.repeat(60));
    console.log('# EXAMPLE 3: QA Validation');
    console.log('#'.repeat(60));
    
    await validateQACoverage('Asset', { lineCoverage: 75 });
    
    console.log('\n' + '='.repeat(60));
    console.log('All examples completed successfully!');
    console.log('='.repeat(60) + '\n');
    
    console.log('Key Takeaways:');
    console.log('1. Always load memory BEFORE processing requests');
    console.log('2. Enrich system prompt with memory context');
    console.log('3. Write memory for significant actions only');
    console.log('4. Filter memories by scope, tags, and importance');
    console.log('5. Memory ensures consistency across sessions\n');
    
  } catch (error) {
    console.error('Example execution failed:', error);
    process.exit(1);
  }
}

// Run examples if this file is executed directly
if (require.main === module) {
  runExamples();
}

// Export for use in other modules
export {
  chatApiHandler,
  planBuildWave,
  validateQACoverage
};
