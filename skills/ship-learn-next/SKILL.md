---
name: ship-learn-next
description: Use when user has learning content (YouTube transcripts, articles, tutorials) and wants to make it actionable. Triggers include "turn this into a plan", "make this actionable", "I watched/read X, now what?", or requests to create reps from educational material.
allowed-tools: Read,Write
---

<objective>
Transform passive learning content into shippable iterations using the Ship-Learn-Next framework: Ship something real, Learn from it, plan Next rep.
</objective>

<triggers>
Use this skill when the user:
- Has a transcript/article/tutorial and wants to "implement the advice"
- Asks to "turn this into a plan" or "make this actionable"
- Wants to extract implementation reps from educational content
- Needs help breaking down big ideas into small, shippable reps
- Says "I watched/read X, now what should I do?"
</triggers>

<quick_start>
1. Read the content file user provides
2. Extract 3-5 core actionable lessons
3. Help user define a 4-8 week quest goal
4. Design Rep 1: smallest shippable version (1-7 days)
5. Map Reps 2-5 as progression
6. Save plan as "Ship-Learn-Next Plan - [Quest Title].md"
</quick_start>

<success_criteria>
- Core lessons extracted (actionable, not theoretical)
- Quest goal defined (specific, measurable, 4-8 weeks)
- Rep 1 is shippable in 1-7 days with clear success criteria
- Reps 2-5 show progression building on previous reps
- Plan saved to markdown file with clear filename
- User knows when to start and what "done" looks like
</success_criteria>

<framework>
<core_principle>
100 reps beats 100 hours of study. Learning = doing better, not knowing more.
</core_principle>

<cycle>
1. SHIP - Create something real (code, content, product, demonstration)
2. LEARN - Honest reflection on what happened
3. NEXT - Plan the next iteration based on learnings
</cycle>
</framework>

<process>
<read_content>
Read the file user provides (transcript, article, notes) using Read tool.
</read_content>

<extract_lessons>
Identify from the content:
- Main advice/lessons (key takeaways)
- Actionable principles (what can be practiced)
- Skills being taught
- Examples/case studies to replicate

Avoid:
- Summarizing everything (focus on actionable parts)
- Listing theory without application
- Including "nice to know" vs "need to practice"
</extract_lessons>

<define_quest>
Ask user:
1. "Based on this content, what do you want to achieve in 4-8 weeks?"
2. "What would success look like? (Be specific)"
3. "What's something concrete you could build/create/ship?"

Good quest: "Ship 10 cold outreach messages and get 2 responses"
Bad quest: "Learn about sales" (too vague)
</define_quest>

<design_rep_1>
Ask:
- "What's the smallest version you could ship THIS WEEK?"
- "What do you need to learn JUST to do that?" (not everything)
- "What would 'done' look like for rep 1?"

Make it:
- Concrete and specific
- Completable in 1-7 days
- Produces real evidence/artifact
- Small enough to not be intimidating
- Big enough to learn something meaningful
</design_rep_1>

<map_future_reps>
Progression principles:
- Each rep adds ONE new element
- Increase difficulty based on success
- Reference specific lessons from the content
- Keep reps shippable (not theoretical)
</map_future_reps>
</process>

<rep_template>
```markdown
## Rep N: [Specific Goal]

**Ship Goal**: [What you'll create/do]
**Success Criteria**: [How you'll know it's done]
**What You'll Learn**: [Specific skills/insights]
**Resources Needed**: [Minimal - just what's needed for THIS rep]
**Timeline**: [Specific deadline]

**Action Items**:
1. [Concrete item 1]
2. [Concrete item 2]
3. [Concrete item 3]

**After Shipping - Reflection**:
- What actually happened? (Be specific)
- What worked? What didn't?
- What surprised you?
- Rate this rep: _/10
- What would you do differently?
```
</rep_template>

<output_template>
```markdown
# Your Ship-Learn-Next Quest: [Title]

## Quest Overview
**Goal**: [What they want to achieve in 4-8 weeks]
**Source**: [The content that inspired this]
**Core Lessons**: [3-5 key actionable takeaways from content]

---

## Rep 1: [Specific, Shippable Goal]

**Ship Goal**: [Concrete deliverable]
**Timeline**: [This week / By [date]]
**Success Criteria**:
- [ ] [Specific thing 1]
- [ ] [Specific thing 2]
- [ ] [Specific thing 3]

**What You'll Practice** (from the content):
- [Skill/concept 1 from source material]
- [Skill/concept 2 from source material]

**Action Items**:
1. [Concrete item]
2. [Concrete item]
3. [Concrete item]
4. Ship it (publish/deploy/share/demonstrate)

**Minimal Resources** (only for this rep):
- [Link or reference - if truly needed]

**After Shipping - Reflection**:
- What actually happened?
- What worked? What didn't?
- What surprised you?
- Rate this rep: _/10
- What's one thing to try differently?

---

## Rep 2: [Next Iteration]
**Builds on**: Rep 1 + [what you learned]
**New element**: [One new challenge/skill]
**Ship goal**: [Next concrete deliverable]

---

## Reps 3-5: Future Path
**Rep 3**: [Brief description]
**Rep 4**: [Brief description]
**Rep 5**: [Brief description]

*(Details will evolve based on what you learn in Reps 1-2)*

---

## Remember
- This is about DOING, not studying
- Aim for 100 reps over time (not perfection on rep 1)
- Each rep = Plan → Do → Reflect → Next
- You learn by shipping, not by consuming

**Ready to ship Rep 1?**
```
</output_template>

<conversation_style>
<approach>
- Direct but supportive, no fluff
- "Ship it, then we'll improve it"
- "What's the smallest version you could do this week?"
- Question-driven: make them think, don't just tell
- Specific, not generic: "By Friday, ship one landing page" not "Learn web development"
- Always end with "what's next?"
</approach>

<key_phrases>
- "What's the smallest version you could ship this week?"
- "What do you need to learn JUST to do that?"
- "This isn't about perfection - it's rep 1 of 100"
- "Ship something real, then we'll improve it"
- "Based on [content], what would you actually DO differently?"
- "Learning = doing better, not knowing more"
</key_phrases>
</conversation_style>

<avoid>
- Creating a study plan (create a SHIP plan)
- Listing all resources to read/watch (pick minimal for current rep)
- Making perfect the enemy of shipped
- Letting them plan forever without starting
- Accepting vague goals ("learn X" → "ship Y by Z date")
- Overwhelming with the full journey (focus on rep 1)
</avoid>

<content_types>
YouTube transcripts: Focus on advice not stories, extract concrete techniques, identify case studies to replicate
Articles/tutorials: Identify "now do this" parts vs theory, extract the workflow, find minimal starting example
Course notes: Find smallest project from course, identify modules needed for rep 1, what can be practiced immediately
</content_types>

<saving>
Filename: "Ship-Learn-Next Plan - [Brief Quest Title].md"
Quest title: 3-6 words, descriptive of main goal

After creating:
1. Show: "Saved to: [filename]"
2. Brief overview of quest
3. Highlight Rep 1 (what's due this week)

Then ask:
1. "When will you ship Rep 1?"
2. "What's the one thing that might stop you? How will you handle it?"
3. "Come back after you ship and we'll reflect + plan Rep 2"
</saving>

<quality_checklist>
- Specific, shippable rep 1 (completable in 1-7 days)
- Clear success criteria (user knows when done)
- Concrete artifacts (something real to show)
- Direct connection to source content
- Progression path for reps 2-5
- Emphasis on action over consumption
- Honest reflection built in
- Small enough to start today, big enough to learn
</quality_checklist>
