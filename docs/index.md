---
title: About
icon: lucide/circle-question-mark
---

Django Comb is a command-line tool to help you untangle your Django models.

## What does Django Comb do?

In large Django projects, the data model can become very intertwined. In particular, foreign key relationships can
create undesirable dependencies between different parts of the system, leading to poor database performance,
slower tests and high cognitive load.

If a team decides that they want to limit foreign keys pointing to a particular model, it's not easy to enforce.
Code ownership rules won't catch models that are created in apps elsewhere in a large code base.
That's the problem Django Comb was created to address.  

## How it works

- You define [rules](rules.md) about sets of models in `model_rules.toml` files, in your project's apps. 
- Then [the `lint_models` management command](management-commands/lint-models.md) should be added to your CI pipeline.
  A rule violation will cause CI to fail.

## Tracking technical debt

If you're starting to put model rules in place, chances are there are already some foreign keys that you'd like to
remove. You can express this technical debt as `silenced-violations` in your rules, so the linter will pass despite
them being included.

[The `get_model_rules` management command](management-commands/get-model-rules.md) is
provides a way of getting the number of silenced violations, and anything else you've defined in your rules.
You can use this as part of tooling to track progress on removing them.

[Get started](installation.md){ .md-button .md-button--primary }