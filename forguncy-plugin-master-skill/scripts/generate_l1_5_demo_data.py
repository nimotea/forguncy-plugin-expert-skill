import json
import random
import datetime
import argparse
from pathlib import Path

def generate_data(num_orders=10, num_resources=5, output_dir="."):
    """
    Generates demo data for L1.5 Scheduling logic.
    Output: WorkOrders.json, Resources.json
    """
    
    # 1. Generate Resources
    resource_groups = ["Turning", "Milling", "Drilling", "Assembly", "Inspection"]
    resources = []
    
    for i in range(num_resources):
        group = resource_groups[i % len(resource_groups)]
        resources.append({
            "Id": f"RES-{i+1:03d}",
            "Name": f"{group}-Machine-{i+1}",
            "Group": group,
            "Capacity": 1.0,  # Standard capacity
            "Efficiency": random.uniform(0.8, 1.2)
        })
        
    # 2. Generate Work Orders
    work_orders = []
    start_date = datetime.datetime.now()
    
    for i in range(num_orders):
        wo_id = f"WO-{i+1:04d}"
        quantity = random.randint(10, 1000)
        
        # Random flow of operations
        num_ops = random.randint(1, 4)
        ops = []
        selected_groups = random.sample(resource_groups, num_ops)
        
        for j, group in enumerate(selected_groups):
            ops.append({
                "OpCode": f"{10 * (j+1)}",
                "Name": f"Op-{group}",
                "ResourceGroup": group,
                "StandardTime": round(random.uniform(0.1, 2.0), 2), # Hours per unit
                "SetupTime": random.randint(15, 60) # Minutes
            })
            
        due_date = start_date + datetime.timedelta(days=random.randint(5, 30))
        
        work_orders.append({
            "Id": wo_id,
            "Product": f"Product-{random.randint(1, 20)}",
            "Quantity": quantity,
            "ReleaseDate": start_date.isoformat(),
            "DueDate": due_date.isoformat(),
            "Priority": random.randint(1, 10),
            "Operations": ops
        })

    # 3. Write to files
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    
    with open(out_path / "Resources.json", "w", encoding="utf-8") as f:
        json.dump(resources, f, indent=4, ensure_ascii=False)
        
    with open(out_path / "WorkOrders.json", "w", encoding="utf-8") as f:
        json.dump(work_orders, f, indent=4, ensure_ascii=False)
        
    print(f"Generated {len(resources)} resources in {out_path / 'Resources.json'}")
    print(f"Generated {len(work_orders)} work orders in {out_path / 'WorkOrders.json'}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate L1.5 Scheduling Demo Data")
    parser.add_argument("--orders", type=int, default=10, help="Number of work orders")
    parser.add_argument("--resources", type=int, default=5, help="Number of resources")
    parser.add_argument("--output", type=str, default=".", help="Output directory")
    
    args = parser.parse_args()
    generate_data(args.orders, args.resources, args.output)
