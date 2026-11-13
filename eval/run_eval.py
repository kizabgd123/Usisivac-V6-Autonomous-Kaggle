#!/usr/bin/env python3
"""
CLI runner for the Usisivac V6 Evaluation & Quality Flywheel Harness.
Exposes 'eval' namespace commands matching the Google agents-cli eval specification:
  - run: generate + grade in one go
  - generate: produce agent traces from eval dataset
  - grade: score traces and generate summary + HTML report
  - compare: side-by-side diff of score changes (per-case analysis)
  - analyze: cluster failure traces into actionable themes
  - optimize: prompt hill-climbing pass
  - check-regression: automated threshold check for CI/scheduled runs (exits non-zero on failure)
"""

import sys
import os
import argparse

# Ensure workspace root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from Usisivac.src.core.eval_harness import EvalHarness
except ImportError:
    EvalHarness = None


def main():
    parser = argparse.ArgumentParser(
        description="Usisivac V6 Evaluation & Quality Flywheel Harness (agents-cli eval paradigm)"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # 1. run (generate + grade)
    p_run = subparsers.add_parser("run", help="Run agent inference over eval dataset and grade traces")
    p_run.add_argument("--dataset", default="eval/datasets/baseline_dataset.json", help="Path to EvaluationDataset JSON")
    p_run.add_argument("--config", default="eval/eval_config.yaml", help="Path to eval_config.yaml")
    p_run.add_argument("--system-instruction", default=None, help="Custom system instruction prompt")

    # 2. generate
    p_gen = subparsers.add_parser("generate", help="Run agent inference over eval cases and record traces")
    p_gen.add_argument("--dataset", default="eval/datasets/baseline_dataset.json", help="Path to EvaluationDataset JSON")
    p_gen.add_argument("--output", default=None, help="Custom output trace JSON path")
    p_gen.add_argument("--system-instruction", default=None, help="Custom system instruction prompt")

    # 3. grade
    p_grade = subparsers.add_parser("grade", help="Score traces against configured metrics")
    p_grade.add_argument("--traces", required=True, help="Path to trace JSON file")
    p_grade.add_argument("--config", default="eval/eval_config.yaml", help="Path to eval_config.yaml")
    p_grade.add_argument("--output", default=None, help="Custom output results JSON path")
    p_grade.add_argument("--no-llm-judge", action="store_true", help="Skip LLM-as-a-judge queries (fast test mode)")

    # 4. compare
    p_comp = subparsers.add_parser("compare", help="Compare two eval result JSON files side-by-side")
    p_comp.add_argument("baseline", help="Path to baseline results JSON")
    p_comp.add_argument("candidate", help="Path to candidate results JSON")

    # 5. analyze
    p_ana = subparsers.add_parser("analyze", help="Cluster failure traces into actionable themes")
    p_ana.add_argument("results", help="Path to results JSON file")

    # 6. optimize
    p_opt = subparsers.add_parser("optimize", help="Automated hill-climbing pass on system prompts")
    p_opt.add_argument("--dataset", default="eval/datasets/baseline_dataset.json", help="Path to EvaluationDataset JSON")
    p_opt.add_argument("--iterations", type=int, default=2, help="Number of hill-climbing iterations")
    p_opt.add_argument("--baseline-prompt", default="You are Usisivac V6 ML engineer.", help="Starting system prompt")

    # 7. check-regression
    p_reg = subparsers.add_parser("check-regression", help="Automated threshold check for CI/alerts (exits non-zero on regression)")
    p_reg.add_argument("baseline", help="Path to baseline results JSON")
    p_reg.add_argument("candidate", help="Path to candidate results JSON")
    p_reg.add_argument("--threshold", type=float, default=0.1, help="Max allowable drop in mean score (default: 0.1)")

    # 8. paired-eval (Kaggle Multi-Seed Evaluation Protocol)
    p_pe = subparsers.add_parser("paired-eval", help="Run multi-seed paired t-test champion promotion gate (Kaggle Eval Protocol)")
    p_pe.add_argument("--matrix", required=True, help="Path to CSV matrix containing seed,baseline_auc,candidate_auc")
    p_pe.add_argument("--baseline", default="baseline_auc", help="Column name for baseline AUC scores")
    p_pe.add_argument("--candidate", default="candidate_auc", help="Column name for candidate AUC scores")
    p_pe.add_argument("--seed-col", default="seed", help="Column name for seeds")
    p_pe.add_argument("--json", action="store_true", help="Output full stats as JSON")
    p_pe.add_argument("--append-log", default=None, help="Append JSON results to evaluation log (e.g. eval/eval_history.jsonl)")

    args = parser.parse_args()

    if args.command != "paired-eval":
        if EvalHarness is None:
            print("ERROR: EvalHarness not found in current environment.", file=sys.stderr)
            sys.exit(1)
        harness = EvalHarness(config_path=getattr(args, "config", "eval/eval_config.yaml"))

    if args.command == "run":
        trace_path = harness.generate(dataset_path=args.dataset, system_instruction=args.system_instruction)
        harness.grade(traces_path=trace_path)

    elif args.command == "generate":
        harness.generate(dataset_path=args.dataset, output_file=args.output, system_instruction=args.system_instruction)

    elif args.command == "grade":
        harness.grade(traces_path=args.traces, output_file=args.output, use_llm_judge=not args.no_llm_judge)

    elif args.command == "compare":
        harness.compare(args.baseline, args.candidate)

    elif args.command == "analyze":
        harness.analyze(args.results)

    elif args.command == "optimize":
        harness.optimize(dataset_path=args.dataset, baseline_prompt=args.baseline_prompt, iterations=args.iterations)

    elif args.command == "check-regression":
        passed = harness.check_regression(args.baseline, args.candidate, threshold=args.threshold)
        if not passed:
            print("❌ Exiting with non-zero exit code due to evaluation regression.")
            sys.exit(1)
        print("✅ Regression check passed.")
        sys.exit(0)

    elif args.command == "paired-eval":
        from eval.paired_eval import load_matrix_pure, compute_paired_stats, render_report, _SCIPY
        from pathlib import Path
        import json

        matrix_path = Path(args.matrix)
        if not matrix_path.is_file():
            print(f"ERROR: matrix file not found: {matrix_path}", file=sys.stderr)
            sys.exit(2)

        try:
            if _SCIPY:
                import pandas as pd
                df = pd.read_csv(matrix_path)
                seeds = df[args.seed_col].tolist()
                baselines = df[args.baseline].tolist()
                candidates = df[args.candidate].tolist()
            else:
                seeds, baselines, candidates = load_matrix_pure(
                    str(matrix_path), args.seed_col, args.baseline, args.candidate
                )
        except KeyError as e:
            print(f"ERROR: missing column {e} in {matrix_path}", file=sys.stderr)
            sys.exit(2)

        deltas = [c - b for c, b in zip(candidates, baselines)]
        try:
            stats = compute_paired_stats(deltas)
        except ValueError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            sys.exit(2)

        stats["seeds"] = seeds
        stats["deltas"] = deltas
        stats["baseline_col"] = args.baseline
        stats["candidate_col"] = args.candidate
        stats["matrix_path"] = str(matrix_path)

        if args.json:
            print(json.dumps(stats, indent=2))
        else:
            print(render_report(seeds, deltas, stats))

        if args.append_log:
            log_path = Path(args.append_log)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(stats) + "\n")
            if not args.json:
                print(f"\n  📝 Result appended to: {log_path}")

        if stats["promoted"]:
            print("✅ Promotion verdict: PROMOTE (p < 0.05 and CI_lower > 0)")
            sys.exit(0)
        else:
            print("❌ Promotion verdict: HOLD (p >= 0.05 or CI_lower <= 0)")
            sys.exit(1)


if __name__ == "__main__":
    main()
