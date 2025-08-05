from livekit.agents import function_tool

@function_tool(name="plan_tasks", description="Breaks big tasks into smaller steps.")
async def plan_tasks(context, goal: str) -> str:
    steps = [
        f"Step {i+1}: {step}" for i, step in enumerate(
            [
                "Understand user goal",
                "Check if tools are available",
                "Split goal into sub-tasks",
                "Execute each task",
                "Verify result",
                "Inform user"
            ]
        )
    ]
    return f"📋 Plan for: {goal}\n" + "\n".join(steps)
