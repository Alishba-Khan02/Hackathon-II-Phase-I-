This specification defines Phase I of the Evolution of Todo project.

Goal:
Build a command-line Todo application that runs locally, stores data in memory, and supports basic task management.

Out of Scope (Strict):

❌ Database

❌ Web UI

❌ Authentication

❌ AI / Chatbot

❌ File persistence

❌ Networking

2. Target User

A single local user

Uses terminal/console

Manages personal todos during one program session

3. Functional Requirements (WHAT)
3.1 Add Task

User Story:
As a user, I want to add a new task so that I can track things I need to do.

Requirements:

User can enter:

title (required)

description (optional)

System assigns a unique task ID

Task is marked incomplete by default

Acceptance Criteria:

Task appears in task list after creation

Title must not be empty

ID is auto-generated and unique in session

3.2 View Task List

User Story:
As a user, I want to view all tasks so I can see what I need to do.

Requirements:

Display all tasks

Show:

ID

Title

Completion status

Acceptance Criteria:

Completed tasks are visually distinguishable

Empty list shows friendly message

3.3 Update Task

User Story:
As a user, I want to update a task so I can correct or change details.

Requirements:

Update title and/or description

Task identified by ID

Acceptance Criteria:

Task updates only if ID exists

Invalid ID shows error message

Updated values are reflected immediately

3.4 Delete Task

User Story:
As a user, I want to delete a task so I can remove tasks I no longer need.

Requirements:

Delete by task ID

Acceptance Criteria:

Task is removed from memory

Deleting non-existent ID shows error

Remaining tasks stay unchanged

3.5 Mark Task as Complete / Incomplete

User Story:
As a user, I want to mark a task as complete so I know it is done.

Requirements:

Toggle completion status by task ID

Acceptance Criteria:

Completed status updates correctly

Invalid ID handled gracefully

Task list reflects new status

4. Console Interaction Requirements
4.1 Menu System

The application must display a menu with options:

Add Task

View Tasks

Update Task

Delete Task

Mark Task Complete / Incomplete

Exit

Acceptance Criteria:

Menu reappears after every action

Invalid menu choice shows error

Program exits cleanly

5. Data Model (In-Memory)
Task Entity
Field	Type	Required	Description
id	integer	Yes	Auto-generated
title	string	Yes	Task title
description	string	No	Task details
completed	boolean	Yes	Default false
6. Non-Functional Requirements

Must run on Python 3.13+

No external database

No file storage

Clean separation of concerns

Readable console output

Graceful error handling

7. Constraints (Enforced)

Tasks exist only in memory

All data is lost on program exit

No background threads

No async code

No third-party task libraries

8. Definition of Done (Phase I)

Phase I is complete when:

All 5 core features work

Console menu operates correctly

Errors are handled gracefully

Application runs without crashing

Spec-driven workflow is followed

No manual code written