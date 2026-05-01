# Tool-Using LLM Agent in a 2D Virtual World

A modular harness that lets an LLM agent observe a virtual world, plan toward a goal, call validated tools, receive feedback, and continue until the task is complete.

The main focus of this project is the harness, not the complexity of the world.

## Core Idea

The harness is the product.

The LLM is not allowed to directly modify the environment. It can only act through validated tools. At each step, the agent receives a structured observation, the task goal, and available tool schemas. It then produces a JSON tool call. The harness validates and executes the tool, then feeds the resulting observation back into the next step.

This mirrors the structure of embodied systems: perception, planning, action, feedback, and state update.

## Architecture

```text
Environment -> Observation -> PlannerAgent -> Tool Call
                                  |
                                  v
                          ToolValidator
                                  |
                                  v
                           ToolExecutor
                                  |
                                  v
                           Tool Result
                                  |
                                  v
                             Logger
```

The demo uses a focused 2D grid world so the harness stays easy to inspect.

## Run

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=...
python main.py --model gpt-4o-mini --max-steps 40
```

You can also put `OPENAI_API_KEY` in a local `.env` file.

## Harness Loop

```python
observation = env.reset()

for step in range(max_steps):
    decision = planner.decide(
        observation=observation,
        tool_specs=tool_registry.specs(),
        goal=env.goal,
    )

    tool_call = decision["tool_call"]
    validation = validator.validate(tool_call, tool_registry, env)

    if validation.approved:
        tool_result = executor.execute(tool_call, env)
    else:
        tool_result = {"success": False, "message": validation.reason}

    observation = env.observe()
```

## Tool Calls

Agents choose tools instead of raw action strings:

```json
{
  "tool_call": {
    "name": "move",
    "args": {
      "direction": "east"
    }
  }
}
```

Available MVP tools:

- `look()`
- `move(direction)`
- `scan(query)`
- `pick_up(item)`
- `unlock(target, using)`
- `interact(target)`

## Environments

`Grid2DWorld` is the demo environment: find the key, unlock the door, and reach the goal.

```text
#############
#A..#......K#
#.#.#.#####.#
#.#.........#
#.#########D#
#..........G#
#############
```

Legend: `A` agent, `#` wall, `.` empty space, `K` key, `D` locked door, `G` goal.

One successful strategy is to route around the wall to the key, pick it up, return to the lower-right corridor, unlock the door, and move into the goal.

## Project Structure

```text
agents/      PlannerAgent, LLM client, prompts, parser
core/        shared types, runner, logger, registry
envs/        Grid2D environment
harness/     validator and executor
tools/       tool specs and registry
maps/        2D grid map
logs/        generated episode logs
examples/    example run artifacts
```

## Design Choices

- The agent sees structured observations, not hidden environment state.
- The harness validates tool name, schema, and environment constraints before execution.
- The executor is the only component allowed to call environment APIs.
- The logger records observation, decision, validation, and result for each step.

## Limitations

The agent is LLM-only and requires `OPENAI_API_KEY`. The project also supports loading the key from a local `.env` file.
