---

description: "Tasks for Phase I: CLI Todo Application"
---

# Tasks: Phase I - CLI Todo Application

**Input**: Design documents from `/specs/phase-i-cli-todo/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: All tasks include test creation as per the project constitution's Test-First principle.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, Console)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/todo_app/`, `tests/` at repository root

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure: `src/todo_app/`, `tests/`
- [ ] T002 Initialize Python packages: Create `src/todo_app/__init__.py` and `tests/__init__.py`
- [ ] T003 Configure `pytest` for the project

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Create `Task` data model in `src/todo_app/models.py` with fields: `id` (integer), `title` (string), `description` (string, optional), `completed` (boolean, default false).
- [ ] T005 Implement an in-memory task manager (e.g., a class or dictionary based) in `src/todo_app/main.py` to hold `Task` objects. This manager should handle ID generation.

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add Task (Priority: P1)

**Goal**: User can add new tasks with a title (required) and optional description. System assigns a unique ID, and tasks are incomplete by default.

**Independent Test**: Can be tested by adding a task and verifying its presence and attributes in the task list.

### Tests for User Story 1 ⚠️

- [ ] T006 [P] [US1] Unit test for adding a task with valid title and description in `tests/test_todo_app.py`
- [ ] T007 [P] [US1] Unit test for `add_task` to ensure auto-generated ID is unique and sequential (or robustly unique).
- [ ] T008 [P] [US1] Unit test for `add_task` with an empty title (should raise an appropriate error).

### Implementation for User Story 1

- [ ] T009 [US1] Implement `add_task` function in `src/todo_app/main.py` that handles task creation, ID generation, and defaults `completed` to `false`.

**Checkpoint**: User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View Task List (Priority: P1)

**Goal**: User can view all tasks with their ID, title, and completion status. Completed tasks are visually distinguishable.

**Independent Test**: Can be tested by creating tasks and then listing them, verifying correct display.

### Tests for User Story 2 ⚠️

- [ ] T010 [P] [US2] Unit test for `get_all_tasks` when the list is empty in `tests/test_todo_app.py`.
- [ ] T011 [P] [US2] Unit test for `get_all_tasks` with multiple tasks, including both complete and incomplete items, verifying correct data retrieval.
- [ ] T012 [P] [US2] Unit test for the display logic to ensure completed tasks are visually distinguishable (e.g., marked with `[X]` or similar).

### Implementation for User Story 2

- [ ] T013 [US2] Implement `get_all_tasks` function in `src/todo_app/main.py` to retrieve all tasks from the manager.
- [ ] T014 [US2] Implement console display logic in `src/todo_app/main.py` for tasks, showing ID, title, and completion status, with visual distinction for completed tasks.

**Checkpoint**: User Story 2 should be fully functional and testable independently

---

## Phase 5: User Story 3 - Update Task (Priority: P2)

**Goal**: User can update the title and/or description of an existing task by its ID.

**Independent Test**: Can be tested by updating a task and verifying the changes, and by attempting to update a non-existent task.

### Tests for User Story 3 ⚠️

- [ ] T015 [P] [US3] Unit test for `update_task` with a valid ID and new title/description in `tests/test_todo_app.py`.
- [ ] T016 [P] [US3] Unit test for `update_task` with a non-existent ID (should raise an appropriate error/return failure).

### Implementation for User Story 3

- [ ] T017 [US3] Implement `update_task` function in `src/todo_app/main.py` to modify task title/description by ID, handling non-existent IDs.

**Checkpoint**: User Story 3 should be fully functional and testable independently

---

## Phase 6: User Story 4 - Delete Task (Priority: P2)

**Goal**: User can delete a task by its ID.

**Independent Test**: Can be tested by deleting a task and verifying its removal, and by attempting to delete a non-existent task.

### Tests for User Story 4 ⚠️

- [ ] T018 [P] [US4] Unit test for `delete_task` with a valid ID in `tests/test_todo_app.py`.
- [ ] T019 [P] [US4] Unit test for `delete_task` with a non-existent ID (should raise an appropriate error/return failure).

### Implementation for User Story 4

- [ ] T020 [US4] Implement `delete_task` function in `src/todo_app/main.py` to remove a task by ID, handling non-existent IDs.

**Checkpoint**: User Story 4 should be fully functional and testable independently

---

## Phase 7: User Story 5 - Mark Task as Complete / Incomplete (Priority: P1)

**Goal**: User can toggle the completion status of a task by its ID.

**Independent Test**: Can be tested by changing a task's status and verifying the update.

### Tests for User Story 5 ⚠️

- [ ] T021 [P] [US5] Unit test for `toggle_task_status` with a valid ID in `tests/test_todo_app.py`.
- [ ] T022 [P] [US5] Unit test for `toggle_task_status` with a non-existent ID (should raise an appropriate error/return failure).

### Implementation for User Story 5

- [ ] T023 [US5] Implement `toggle_task_status` function in `src/todo_app/main.py` to change the `completed` status of a task by ID, handling non-existent IDs.

**Checkpoint**: User Story 5 should be fully functional and testable independently

---

## Phase 8: Console Interaction (Menu System) (Priority: P1)

**Goal**: The application must display a menu, accept user input for actions, and exit cleanly. Menu reappears after every action.

**Independent Test**: Requires integration testing/manual verification due to direct console interaction.

### Tests for Console Interaction ⚠️

- [ ] T024 [P] [Console] Basic test for main menu display (e.g., using mocked input/output in `tests/test_todo_app.py`).
- [ ] T025 [P] [Console] Test for handling invalid menu choices gracefully.

### Implementation for Console Interaction

- [ ] T026 [Console] Implement the main application loop and display the menu options (Add, View, Update, Delete, Mark Complete/Incomplete, Exit) in `src/todo_app/main.py`.
- [ ] T027 [Console] Implement user input handling for menu choices.
- [ ] T028 [Console] Integrate `add_task` function into the menu system.
- [ ] T029 [Console] Integrate `get_all_tasks` function and display logic into the menu system.
- [ ] T030 [Console] Integrate `update_task` function into the menu system.
- [ ] T031 [Console] Integrate `delete_task` function into the menu system.
- [ ] T032 [Console] Integrate `toggle_task_status` function into the menu system.
- [ ] T033 [Console] Implement clean exit functionality.
- [ ] T034 [Console] Implement graceful error handling for all user inputs within the menu system.

**Checkpoint**: The full CLI application is functional and interactive.

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Final review and minor improvements.

- [ ] T035 Review and refine console output for readability and user experience.
- [ ] T036 Ensure all error paths are handled gracefully and user-friendly messages are displayed.
- [ ] T037 Final check against Definition of Done for Phase I.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion. User stories can then proceed in parallel or sequentially.
- **Console Interaction (Phase 8)**: Depends on all user story functionalities being implemented.
- **Polish (Phase 9)**: Depends on all other phases being complete.

### Within Each User Story

- Tests MUST be written and FAIL before implementation.
- `Task` model before manager.
- Manager functions before integration into the console menu.

### Parallel Opportunities

- Setup tasks marked [P] can run in parallel.
- Tests within a user story marked [P] can run in parallel.
- Different user stories (Phases 3-7) can be worked on in parallel by different team members once the Foundational phase is complete.
