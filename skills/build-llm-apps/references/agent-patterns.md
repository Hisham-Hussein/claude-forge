<overview>
Agent patterns determine how LLM-powered applications are structured. Choose the simplest pattern that solves the problem—complexity adds failure modes.
</overview>

<single_agent>
<name>Single Agent (ReAct)</name>

<when_to_use>
- Simple tasks with clear goals
- Single focus area
- No need for parallelism or specialization
</when_to_use>

<how_it_works>
The agent reasons about what to do, acts by calling a tool, observes the result, and repeats until done.

```
User Query → Reason → Act (tool call) → Observe → Reason → ... → Final Answer
```
</how_it_works>

<best_for>
Research tasks, simple Q&A, single-domain operations.
</best_for>

<anti_pattern>
Using single agent for tasks requiring multiple specialized domains.
</anti_pattern>
</single_agent>

<orchestrator_workers>
<name>Orchestrator-Workers</name>

<when_to_use>
- Complex tasks that can be broken into parallelizable subtasks
- Multiple independent data sources
- Batch processing needs
</when_to_use>

<how_it_works>
A coordinator agent analyzes the task, breaks it into subtasks, dispatches to worker agents, and synthesizes results.

```
Task → Orchestrator breaks down → [Worker 1, Worker 2, Worker 3] → Synthesize → Result
```
</how_it_works>

<best_for>
Report generation, multi-source research, batch processing.
</best_for>

<anti_pattern>
Using for simple sequential tasks—overhead not worth it.
</anti_pattern>
</orchestrator_workers>

<subagents_as_tools>
<name>Subagents as Tools</name>

<when_to_use>
- Hierarchical tasks requiring specialized expertise
- Complex multi-step workflows
- Need to encapsulate specialist knowledge
</when_to_use>

<how_it_works>
Wrap specialized agents as callable tools. The main agent delegates by "calling" a subagent.

```python
def research_tool(query: str) -> str:
    """Delegates to research specialist agent."""
    return research_agent.invoke(query)

main_agent.tools = [research_tool, writing_tool, analysis_tool]
```
</how_it_works>

<best_for>
Teams of specialists, complex multi-step workflows.
</best_for>

<anti_pattern>
Deep nesting (>2 levels) creates debugging nightmares.
</anti_pattern>
</subagents_as_tools>

<multi_agent_handoffs>
<name>Multi-Agent Handoffs</name>

<when_to_use>
- Conversations that cross domain boundaries
- Different specialists needed at different times
- State needs to transfer between agents
</when_to_use>

<how_it_works>
Agents can "hand off" conversations to specialists. State transfers with the handoff.

```
User (sales question) → Sales Agent → User (support question) → [handoff] → Support Agent
```
</how_it_works>

<best_for>
Customer service bots, multi-department workflows.
</best_for>

<anti_pattern>
Handoffs for every message—use single agent with multiple tools instead.
</anti_pattern>
</multi_agent_handoffs>

<decision_tree>
**Pattern Selection:**

```
Q1: Is task simple and focused?
    YES → Single Agent (ReAct)
    NO  → Q2

Q2: Can subtasks run in parallel?
    YES → Orchestrator-Workers
    NO  → Q3

Q3: Do domains differ significantly?
    YES → Multi-Agent Handoffs
    NO  → Subagents as Tools
```
</decision_tree>

<comparison_table>
| Pattern | Complexity | Parallelism | Best For |
|---------|------------|-------------|----------|
| Single Agent | Low | None | Simple focused tasks |
| Orchestrator-Workers | Medium | High | Parallel subtasks |
| Subagents as Tools | Medium-High | Optional | Hierarchical expertise |
| Multi-Agent Handoffs | High | None | Domain switching |
</comparison_table>
