---

authors: ['björn']
comments: false
date: 2025-05-03T16:20:00+08:00
lastmod: 2025-05-03T16:20:00+08:00
layout: post
title: Running effective meetings uses the same skills as running successful projects
subtitle: From meeting minutes to project milestones
slug: effective-meetings
categories:
  - blog
tags:
  - meetings
  - project-planning
  - planning
  - agile
  - facilitation

---



You've probably sat through your fair share of meetings where time slips away as conversations wander aimlessly, not unlike being dropped into an unfamiliar codebase, with twisting branches all alike.

A colleague asked for feedback on a meeting they ran, and after sharing my thoughts, I realized my advice about meetings sounded exactly like how I talk about planning projects. This got me thinking: the skills for running good meetings and successful projects are nearly identical.

Yet somehow, we still treat our meetings like they're different beasts entirely. Why do so many meetings fail? Usually because we approach them without a clear plan.

Meetings are often run like debugging without a hypothesis, just throwing log statements everywhere and hoping something works, where you have a list of topics but no clear goals or time constraints. You might cover everything, but that's more luck than design.

This is similar to "planning forward" in projects: We start with a feature list without understanding the details, create up-front timelines in Gantt charts that rarely get revised, and postpone integration until the end. We move through tasks sequentially, assuming everything will go right, only to discover problems when time is about to or has already run out.

Both approaches ignore that time runs out, whether in a 30-minute meeting or a three-month project. Without a plan, meetings go nowhere and projects fall behind.

In my experience, here's what both have in common:

* Gather everything that needs to get done
* Clarify goals for each item
* Group similar things together
* Prioritize the important stuff first
* Estimate how long each section will take
* Guide the work to keep it on track
* Define next steps so everyone knows what's happening after

## The pieces

Let's break down each of these components and see how they apply specifically to meetings:

### 1. Gather: Define your scope
Just as you wouldn't start coding without requirements, don't start a meeting without defining what needs covering. List all topics and be realistic about what fits in the allotted time. If your meeting scope looks like your backlog after a year of "we'll get to it later," you're doing it wrong.

### 2. Clarify: Set measurable goals for each topic
For each topic, be clear about what you're trying to accomplish:

* **Discuss:** "We need to decide on auth providers. What criteria should guide our recommendation?"
* **Decision:** "We recommend Provider A because..."
* **FYI:** "We've implemented the new provider in staging and learned..."

**Pro tip**: Prefix each agenda item with one of these categories (Discuss/Decision/FYI) to ground everyone in what you're trying to accomplish with each topic.

### 3. Group: Combine related topics
Identify when similar items come from different people and combine them. This prevents redundant discussions and gives a clearer picture of what needs attention, similar to combining related user stories into an epic. When several people raise the same issue in different ways, it's usually important.

### 4. Prioritize: Focus on what matters
Sequence by importance, not by who talks loudest or which item has been sitting on the agenda longest. Start with critical items so when you inevitably run out of time, at least the important stuff got done.

### 5. Estimate: Time boxing
We accept that iteration estimates will be wrong (it's just a question of how wrong), and meeting time estimates work exactly the same way. Having a clear time target keeps everyone aligned. Be explicit about constraints: "We have 15 minutes for this topic" creates healthy pressure to stay focused.

### 6. Guide: Keep discussions on track
Just like daily standups in project work, regularly check in on your meeting's progress. Help nudge the meeting along:

#### Monitor progress toward goals
Just like in daily standups, pay attention to whether the discussion is moving toward your goal. Ask yourself, "Are we just talking, or are we getting closer to making a decision?" If you're 10 minutes into database options and no one has mentioned the actual requirements, it's time to refocus.

#### Keep discussions focused
When someone goes off on a tangent describing an intricate edge case, redirect with: "That sounds like an important edge case. Will this affect the decision we're trying to make right now? If not, could you chat with the relevant team after this? Right now we need to focus on making our decision."

#### Provide time checks
My [rice'n'garlic advice](https://www.geepawhill.org/2021/04/07/rice-garlic-more-smaller-steps/) is to check in halfway through a conversation and remind everyone of the time left. Sometimes simply saying "We have 7 minutes left to decide on this" creates the right pressure to wrap things up. If needed, quickly restate the goal: "Remember, we just need to agree on which two options to research further, not make the final decision today."

#### Make realistic time decisions
Be realistic about whether you can finish in the time you have. If a 15-minute agenda item is turning into a 45-minute discussion, decide whether to:
- Extend the current meeting (if everyone can stay)
- Schedule a follow-up with just the key stakeholders
- Assign someone to gather more data and come back next time

### 7. Next steps: Ensure clear outcomes
Don't let topics end without everyone knowing the outcome. For each item, ensure everyone knows:
- Is it done or still open?
- Who owns any follow-up actions?
- When should we expect progress?
- How will we track it?

Capture this in your meeting notes. Don't rely on memory. Write down the decisions, owners, and deadlines so our future selves can thank us.

## In practice

Different meetings need different approaches, but a well-run meeting follows the same meta structure. This structure works for all kinds of meetings: one-on-ones, planning sessions, even technical architecture reviews, because the topics and participants change, but the structure that makes meetings effective doesn't.

Let's see how this structure looks in practice with a couple of common meeting types.

### Retrospectives
Retros help teams reflect on what worked, what didn't, and what to improve, much like code reviews but for your processes.

- **Gather**: Have everyone add topics to a shared retrospective board
- **Clarify & Group**: Cluster related topics to understand common themes
- **Prioritize**: Vote on which issues will have the most impact to address
- **Estimate & Guide**: Timebox discussions, default 3 minutes per topic, explicitly decide to extend or move on
- **Next Steps**: Capture clear action items, owners, and timelines

**Pro tip**: Seeing the same issues iteration after iteration? Try a [reverse retrospective](https://www.thoughtworks.com/en-au/insights/blog/reverse-retrospective-part-1) where you start with known problems and dedicate the entire session to brainstorming solutions.

### Recurring team meetings
Regular meetings work best with a consistent structure, like good software needs a reliable architecture.

- **Gather**: Maintain a living document where people add items between meetings, plus time at the start to add more
- **Prioritize**: Critical conversations happen first, not just what's been on the list longest
- **Clarify**: Define each topic's goal and intended outcome (FYI, discussion, or decision-making)
- **Estimate**: Allocate time to topics based on importance and complexity
- **Guide**: Check progress mid-topic with "Are we getting closer to our goal?"
- **Next Steps**: Note who's doing what by when

**Pro tip**: For complex topics, try a [silent meeting](https://medium.com/swlh/the-silent-meeting-manifesto-v1-189e9e3487eb) approach where everyone reads and comments on a shared document before discussion. This helps people think deeply, solve quick questions in writing, and prevent a few voices from dominating.

## The meta-skill

Running a good meeting uses the same mental muscles as running a good project:

- Scope definition is like requirements gathering
- Timeboxing topics is like defining iterations
- Progress checks are like standups

If you can't keep a 30-minute meeting on track, how will you keep a three-month project on track? Both require the same core skills:

1. **Clear Goals**: "We want to discuss database options" is as useless as "We want to build a better app."

2. **Risk Management**: Put risky, important topics first, whether in meetings or project timelines.

3. **Progress Monitoring**: Regularly ask: "Are we moving toward our goal or getting sidetracked?"

4. **Flexibility with Discipline**: Sometimes you need to extend a meeting or an iteration, but do it consciously, not by default.

5. **Follow-through**: Track action items like you track bugs, they're just as important.

I wonder if running meetings could be good practice for running projects? The skills are similar, but the feedback cycle is much shorter.

## Conclusion

Every engineer knows that a well-designed system needs both good architecture and regular maintenance. Your meetings are no different.

By applying the same structured thinking to your meetings that you use in your code (defining clear requirements, managing scope, prioritizing effectively, and documenting outcomes), you transform the meetings in your calendar into productive work sessions.

In my experience, these skills compound nicely. I bet you'll get better at delivering focused projects as you get better at running focused meetings.

So before you schedule your next meeting, run it through the same mental checklist you'd use for planning a project:
- Have you gathered topics and defined what you want from each one?
- Have you prioritized what matters most?
- Can this all get done in the time you have?
- Do you have a plan to keep discussions on track?

Keep in mind that guiding meetings is a lot like incident response. You can plan all you want, but you need to react to what's actually happening. This framework gives you a starting point, but the real magic happens when you apply it in the moment. Start small by focusing on timeboxing discussions or defining clear outcomes. The structure matters, but how you adapt when the sewage hits the aerowatt generator is what really counts.

If not, refactor before you commit.

Efficient meetings aren't magic. They're just good engineering applied to communication.
