# Personal Productivity Agent Context Management

## Agent Configuration

```yaml
agent_role: personal_assistant
primary_tools:
  - ctx (task/project tracking)
  - mcp_memory_docker (learning patterns)
  - mcp_browser (research assistance)
```

## Daily Context Management

```
Morning initialization:
1. ctx create daily-{YYYY-MM-DD}
2. ctx set-state ☀️
3. Daily setup:
   - ctx note "FOCUS: {main_priority_today}"
   - ctx note "MEETINGS: {count} scheduled | BLOCKS: {deep_work_blocks}"
   - ctx note "ENERGY: {high/medium/low} | MOOD: {emoji}"
```

## Task Management Prompts

### 1. Task Capture
```
Quick task entry:
- ctx note "TODO: {task_description} | DUE: {date} | EST: {time_estimate}"
- ctx note "CONTEXT: @{location} #{project} !{priority}"
- Memory: Link task to project entity
```

### 2. Time Blocking
```
Time block management:
- ctx note "BLOCK: {start_time}-{end_time} | {task_type} | {description}"
- ctx note "COMPLETED: {actual_time} | QUALITY: {1-5} | INTERRUPTIONS: {count}"
- Memory: Track productivity patterns by time of day
```

### 3. Project Tracking
```
Project context:
- ctx create project-{name}
- ctx note "GOAL: {outcome} | DEADLINE: {date}"
- ctx note "MILESTONE: {name} - {status} - {completion}%"
- ctx note "BLOCKER: {description} | NEED: {required_action}"
```

## Learning Context

```
Learning session tracking:
1. ctx create learn-{topic}
2. ctx set-state 📚
3. Knowledge capture:
   - ctx note "SOURCE: {book/article/video} - {url/reference}"
   - ctx note "INSIGHT: {key_learning}"
   - ctx note "ACTION: {how_to_apply}"
   - Memory: Create knowledge entity with connections
```

## Personal Workflow States

```
Daily states:
☀️ (morning) -> 🏃 (active) -> 🍽️ (break) -> 🌙 (evening) -> 📊 (review)

Task states:
📥 (inbox) -> 🎯 (focused) -> ⏸️ (paused) -> ✅ (done) -> 📦 (archived)
```

## Weekly Review Context

```
Weekly review process:
1. ctx create weekly-review-{week_number}
2. Accomplishments:
   - ctx list | grep "✅" > completed_tasks.tmp
   - ctx note "WINS: {top_3_accomplishments}"
   - ctx note "METRICS: {tasks_completed}/{tasks_planned}"
3. Planning:
   - ctx note "NEXT_WEEK: {top_3_priorities}"
   - Memory: Analyze productivity patterns
```

## Health & Wellness Tracking

```
Wellness context:
- ctx note "SLEEP: {hours}h | QUALITY: {1-5}"
- ctx note "EXERCISE: {type} - {duration} - {intensity}"
- ctx note "MOOD: {emoji} | ENERGY: {1-10} | STRESS: {1-10}"
- Memory: Correlate wellness metrics with productivity
```

## Decision Making

```
Decision context:
1. ctx create decision-{topic}
2. ctx note "QUESTION: {decision_to_make}"
3. ctx note "OPTION: {option_name} | PROS: {list} | CONS: {list}"
4. ctx note "CRITERIA: {factor} - WEIGHT: {importance}"
5. ctx note "DECISION: {chosen_option} | RATIONALE: {reasoning}"
6. Memory: Track decision patterns and outcomes
```

## Reading List Management

```
Reading tracking:
- ctx create reading-{year}
- ctx note "BOOK: {title} by {author} | STATUS: {reading/completed}"
- ctx note "RATING: {1-5} | TAGS: {categories}"
- ctx note "TAKEAWAY: {main_lesson} | APPLICATION: {how_to_use}"
```

## Habit Tracking

```
Habit context:
1. ctx create habit-{habit_name}
2. Daily check-in:
   - ctx note "CHECK: {date} - {completed: Y/N} | STREAK: {days}"
   - ctx note "OBSTACLE: {what_prevented} | SOLUTION: {adjustment}"
3. Memory: Track habit formation patterns
```

## Personal Retrospective

```
Monthly retrospective:
1. ctx create retro-{YYYY-MM}
2. Reflection prompts:
   - ctx note "GRATEFUL: {three_things}"
   - ctx note "LEARNED: {key_lessons}"
   - ctx note "IMPROVED: {areas_of_growth}"
   - ctx note "CHALLENGE: {biggest_obstacle} | OVERCAME: {how}"
3. Memory: Build personal growth timeline
```

## Integration with Memory

```
Personal knowledge graph:
1. Memory entities:
   - Projects (type: project)
   - Skills (type: skill)
   - People (type: contact)
   - Resources (type: reference)
2. Relations:
   - {project} -> requires -> {skill}
   - {person} -> expert_in -> {topic}
   - {task} -> belongs_to -> {project}
3. Queries:
   - "What projects used {skill}?"
   - "Who can help with {topic}?"
   - "What resources for {learning_goal}?"
```
