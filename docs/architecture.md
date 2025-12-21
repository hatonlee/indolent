# Architecture

## Structure Overview
The application is structured into two key constructs:
- Application Logic
- User Interface

Application logic provides the functionality of the application, while the user interface handles user interactions.

## Application Logic
Application logic follows the repository design principle with 3 main abstraction layers:
- Model
- Repository
- Service

```mermaid
flowchart TD
    C[Service] --> B[Repository]
    B --> A[Model]
```

### Model
Models represent entities in the application. The `Habit` model defines the structure of a habit. The `Completion` model tracks when a habit has been completed.

```mermaid
classDiagram
    class Habit {
        -id: int
        +name: str
        +description: str
        +start_time: datetime
        +frequency: timedelta
        +completions: list[Completion]
    }

    class Completion {
        -id: int
        +timestamp: datetime
        -habit_id: int
        +habit: Habit
    }

    Habit "1" --> "*" Completion
```

### Repository
The repository layer handles data persistence and access. The `HabitRepository` class provides methods for performing CRUD operations on the `Habit` model. `HabitRepository` uses an SQLite database via SQLAlchemy ORM.

### Service
The service layer contains all logic required by the user interface. The `HabitService` class uses `HabitRepository` for CRUD operations. Currently it does not implement additional logic, only some basic error handling.


## User Interface
The user interface is implemented using `tkinter`. There are two main views:

```mermaid
flowchart TD
    A[Main View] --> B[New Habit View]
    B --> A
```

### Main View
Displays a list of habits with their information and status.
Allows users to mark habits as completed for the current interval.

### New Habit View
Provides a form for users to create new habits by entering the required details.


### User Interface Flow


### User Interface and Application Logic Interaction
All interaction with the application logic is done through the `HabitService` class.


## Application Flow

### Create a New Habit

```mermaid
sequenceDiagram
    participant UI as UI
    participant Service as HabitService
    participant Repo as HabitRepository
    participant DB as Database (SQLALchemy)
    participant Model as Habit model

    UI->>Service: create_habit(habit_data)
    Service->>Repo: add(habit_data)
    Repo->>DB: add(Habit)
    DB-->>Model: Habit(habit_data)
    Model-->>DB: Habit
    DB-->>DB: add(Habit)
    DB-->>Repo: return Habit (detached)
    Repo-->>Service: return Habit
    Service-->>UI: return Habit
    UI->>UI: add habit to list / refresh UI
```

Description:
- The UI gets and validates form input and calls `HabitService.create_habit(habit_data)`.
- `HabitService.create_habit` calls `HabitRepository.add(habit_data)`.
- `HabitRepository.add(habit_data)` constructs a `Habit` ORM object, loads its `completions` relationship and returns a detached `Habit` object.
- The service receives the `Habit` and returns it to the UI, which adds it to the habit list and refreshes the view.

### Mark a Habit As Done

```mermaid
sequenceDiagram
    participant UI as UI
    participant Service as HabitService
    participant Repo as HabitRepository
    participant DB as Database (SQLALchemy)
    participant Model as Habit model

    UI->>Service: mark_completed(habit_id)
    Service->>Repo: complete(habit_id, time=now)
    Repo->>DB: complete(habit_id, time)
    DB-->>DB: get(Habit)
    DB-->>Model: Completion(habit_id, time)
    Model-->>DB: Completion
    DB-->>DB: add(Completion)
    DB-->>Repo: return Habit
    Repo-->>Service: return Habit
    Service-->>UI: return Habit
    UI->>UI: update habit status / refresh UI
```

Description:
- The UI triggers `HabitService.mark_completed(habit_id)` when the "complete" button is pressed.
- `HabitService.mark_completed(habit_id)` calls `HabitRepository.complete(habit_id, time=now)`.
- `HabitRepository.complete(habit_id, time)` loads the `Habit` and its `Completion`s, then calls `habit.completed(time)` to determine whether a completion already exists for the corresponding interval.
- If the habit has not yet been completed for that interval, the repository appends a new `Completion(time=time)` to `habit.completions`, and returns the updated `Habit` object.
- The service returns the updated Habit object to the UI, which updates the habit completion status and refreshes the view.

Generally the interaction between the user interface and application logic follows the same pattern. Changes in the UI trigger service methods, which in turn call repository methods to interact with the database. The results are passed back up to the UI for display and updates.
