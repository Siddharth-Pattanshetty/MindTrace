---
name: mindtrace-exam-diagnosis
description: Forensic AI learning diagnostic workflow to analyze student exams, trace root learning gaps, generate targeted interventions, and run re-tests.
type: workflow
author: MindTrace
---

# MindTrace Forensic Exam Diagnosis Skill

Use this skill when analyzing a student's exam paper to detect error patterns, map concepts, identify root learning gaps, and measure mastery improvement.

## Diagnostic Workflow

```text
INPUT: Exam Document / Answer Sheet / Mark Scheme
   │
   ▼
[1] Document Processing (Qwen2.5-VL / PaddleOCR)
   │
   ▼
[2] Answer Evaluation & Verification (SymPy + LLM)
   │
   ▼
[3] Error Taxonomy Classification (SIGN_ERROR, FACTORIZATION_ERROR, etc.)
   │
   ▼
[4] Concept Mapping & Prerequisite Graph Traversal (MiniLM + FAISS)
   │
   ▼
[5] Root-Cause Analysis & Diagnostic Confidence Calculation
   │
   ▼
[6] Adaptive Personalized Intervention Generation (4 Levels)
   │
   ▼
[7] Targeted Practice Question Generation
   │
   ▼
[8] Conceptually Similar Re-test Execution
   │
   ▼
[9] MindTrace Estimated Mastery Update & Longitudinal Tracking
```

## Sub-Skills & Specialized Modules

1. **exam-parser**: Extracts questions, student answers, and expected answers from visual/PDF documents.
2. **answer-evaluator**: Performs SymPy mathematical verification to isolate exact points of divergence.
3. **error-classifier**: Maps mistakes to structured error taxonomy (Sign Error, Factorization Error, Procedural Error, Calculation Error).
4. **concept-analyzer**: Maps questions to concept graph nodes (Expressions, Algebraic Manipulation, Equations, Factorization, Quadratics).
5. **root-cause-analyzer**: Traverses prerequisite hierarchy to discover foundational learning gaps with diagnostic confidence.
6. **remediation**: Scaffolds 4-level adaptive practice sets and verifies conceptual recovery via re-tests.

## Instructions for Execution

When invoked by LatentCode or the API pipeline:
1. Parse input raw text or image file.
2. Run SymPy math evaluation for each question.
3. If surface errors span multiple questions (e.g. Q2, Q4, Q6, Q7, Q9), identify the common prerequisite node (e.g., Algebraic Manipulation).
4. Output structured diagnostic JSON matching MindTrace schema.
