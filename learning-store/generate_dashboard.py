import json
from pathlib import Path
from collections import defaultdict

def generate_html_dashboard(data_dir="data", output_file="index.html"):
    metrics_file = Path(data_dir) / "retrospective_metrics.jsonl"
    
    if not metrics_file.exists():
        print("No metrics data found.")
        return

    # Data structures for layout
    agent_performance = defaultdict(lambda: {"count": 0, "total_quality": 0.0, "total_cost": 0.0, "total_time": 0.0})
    issue_throughput = defaultdict(int)
    
    with open(metrics_file, "r") as f:
        for line in f:
            if not line.strip(): continue
            record = json.loads(line)
            agent = record["agent"]
            
            agent_performance[agent]["count"] += 1
            agent_performance[agent]["total_quality"] += record["quality_score"]
            agent_performance[agent]["total_cost"] += record["cost"]
            agent_performance[agent]["total_time"] += record["resolution_time"]
            issue_throughput[record["issue_type"]] += 1

    # Generate HTML
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Multi-Agent Factory Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f4f9; }
            h1 { color: #333; }
            .card { background: #fff; padding: 20px; margin-bottom: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            table { width: 100%; border-collapse: collapse; margin-top: 10px; }
            th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
            th { background-color: #007bff; color: white; }
        </style>
    </head>
    <body>
        <h1>🏭 Agent Factory Learning Dashboard</h1>
        
        <div class="card">
            <h2>Agent Performance & Cost Breakdown</h2>
            <table>
                <tr>
                    <th>Agent</th>
                    <th>Tasks Completed</th>
                    <th>Avg Quality Trend</th>
                    <th>Avg Resolution Time (s)</th>
                    <th>Total Cost ($)</th>
                </tr>
    """
    
    for agent, stats in agent_performance.items():
        count = stats["count"]
        avg_quality = stats["total_quality"] / count
        avg_time = stats["total_time"] / count
        total_cost = stats["total_cost"]
        
        html += f"""
                <tr>
                    <td>{agent}</td>
                    <td>{count}</td>
                    <td>{avg_quality:.2f}</td>
                    <td>{avg_time:.1f}</td>
                    <td>${total_cost:.4f}</td>
                </tr>
        """
        
    html += """
            </table>
        </div>
        
        <div class="card">
            <h2>Issue Throughput</h2>
            <ul>
    """
    
    for issue_type, count in issue_throughput.items():
        html += f"<li><strong>{issue_type}</strong>: {count} resolved</li>"
        
    html += """
            </ul>
        </div>
    </body>
    </html>
    """
    
    with open(output_file, "w") as f:
        f.write(html)
    print(f"Dashboard generated successfully at {output_file}")

if __name__ == "__main__":
    generate_html_dashboard()
