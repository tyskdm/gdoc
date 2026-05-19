# gdoc Server Architecture

gdoc Server provides two types of servers: a language server and an object server.

1. Language Server
   - Provides server features compatible with LSP 3.17.0
2. Object Server
   - Provides APIs for accessing and manipulating gdoc objects.

In the current version of gdoc Server, changes to objects can only be made from the language server.

## Overview

### Structure

![gdoc Server Architecture](./gdocServerArchitecture.drawio.png)

#### Language Server

It has four main components:

1. gdoc Language Server
   - Provides Language Server Protocol (LSP) APIs as a frontend component.
   - This component will be implemented using Python's async.

2. gdoc Object Database
   - Provides Object Database APIs that performs various task management related to gdoc documents, such as parsing, analyzing, and generating gdoc Objects.

3. gdoc Object Datastore
   - A database-like class to manage gdoc Objects and their relationships.

4. gdoc Object Builder(s)
   - Provide APIs that parses target files, resolve links and building packages.
   - Different Builders are provided as plugins for each type of target package.

#### Object server

It replaces the gdoc Language Server, which is the frontend of the language server, with a gdoc Object Server frontend component.

The rest of the configuration is the same as the Language Server.

### Behaivior

When the language‑server client sends a text‑edit notification, the gdoc server behaves as follows.

1. gdoc Language Server receives text editing events from the client.
2. gdoc Language Server requests gdoc Object Database to parse the edited text.
3. gdoc Object Database create a plan and return the task ticket to Language Server.
4. gdoc Object Database isuse a job ticket to parses the text for gdoc Object Builder.
5. gdoc Object Builder parses the text and return to gdoc Object Database.
6. gdoc Object Database updates gdoc Objects in gdoc Object Datastore.
7. gdoc Language Server receives notifications from the gdoc Object Database about changes in gdoc Objects
8. gdoc Language Server gets semantic tokens, diagnostics, and error messages from gdoc Object Database and sends them to the client.

## Key Abstractions

### Logical Hierarchy: Workspace, Project, and Package

The gdoc server organizes resources into a hierarchical structure to manage scopes and dependencies effectively:

- **Project**: Represents the root organizational unit, mapping 1:1 to a VSCode **Workspace**. It serves as the top-level container for configuration and resource management.
- **Package**: The fundamental unit of content and distribution. A Project can contain multiple internal packages (e.g., a `gdoc` documentation package and a `doxml` source code package).
- **External References**: Projects can import and reference external packages, allowing for cross-project linking and resource sharing.

### Execution Model: Request, Task, and Job

To ensure high responsiveness and efficient resource utilization, gdoc utilizes a tiered execution abstraction:

- **Request**: An external interaction initiated by a client (e.g., an LSP command or an Object API call). Frontends are responsible for translating these protocol-specific messages into internal representations.
- **Task**: The primary unit of internal orchestration. Tasks are protocol-agnostic and represent a logical operation (e.g., "Analyze Document"). The Object Database manages the lifecycle, priority, and cancellation of Tasks.
- **Job**: The atomic unit of execution. A Task is decomposed into one or more Jobs (e.g., *Parse*, *Link*, *Compile*). Jobs are dispatched to Object Builders and executed based on available system resources and dependency constraints.

## Structure: Role and Responsibilities

### Overview

![gdoc Server Architecture](./gdocServerInternalBlocks.drawio.png)

### 1. gdoc Language Server

- Role:
  - Acts as the LSP-compliant **Frontend**, providing the primary interface for IDE clients.
  - Translates protocol-specific messages (LSP) into internal **Requests** for orchestration by the gdoc Object Database.
  - Manages the lifecycle of the LSP session (Initialize, Shutdown, etc.).

- Characteristics:
  - **High Responsiveness**: Leverages Python's `asyncio` to handle concurrent client I/O without blocking internal processing.
  - **Stateful Protocol Handler**: Maintains the mapping between client-side URIs and internal document/package identifiers.
  - **Event-Driven**: Reacts to file system changes and workspace configuration updates to maintain **Project** integrity.

- Responsibilities:
  - **Project & Package Scoping**:
    - Monitors the workspace root to define the **Project** scope using configuration files (e.g., `gdoc.project.json`).
    - Identifies and tracks internal **Packages** and their dependencies within the Project.
  - **Request Translation**:
    - Converts LSP-specific calls (e.g., `textDocument/hover`) into unified internal **Requests**.
    - Initiates corresponding **Tasks** in the Object Database to trigger necessary analysis or data retrieval.
  - **Asynchronous Feedback**:
    - Dispatches diagnostics, semantic tokens, and error messages generated during **Job** execution back to the client as LSP notifications.
  - **Document Synchronization**:
    - Synchronizes IDE editor buffers via `didOpen`, `didChange`, and `didClose`, triggering background **Tasks** to ensure the Project state remains consistent with user edits.

### 2. gdoc Object Database

- Role:
  - Acts as the central orchestrator for document analysis workflows (Parse -> Link -> Analyze).
  - Provides a stable interface for **Frontends** to submit **Requests** and monitor their progress.
  - Manages the decomposition of **Requests** into protocol-agnostic **Tasks** and atomic **Jobs**.
  - Saved and managed the generated object data in the Object Datastore.

- Characteristics:
  - **Threaded Execution**: Operates in a dedicated background worker thread to ensure that computationally intensive analysis does not block the Frontend's high-responsiveness I/O loop.
  - **Internal Async Orchestration**: Uses an internal `asyncio` event loop within its worker thread to manage concurrent **Tasks** and **Jobs** efficiently.
  - **Plugin Host**: Provides the execution environment and lifecycle management for **gdoc Object Builders**, which are integrated as plugins.
  - **Synchronous API for Frontends**: Exposes thread-safe synchronous methods to Frontends, abstracting the internal asynchronous and multi-threaded complexity.

- Responsibilities:
  - **Task Scheduling & Prioritization**: Dynamically manages the execution order of **Tasks** based on user focus (e.g., open documents) and dependency requirements.
  - **Cancellation**: Aborts obsolete **Tasks** and their associated **Jobs** when newer document versions or conflicting **Requests** arrive.
  - **Dependency Graph Management**: Tracks relationships between documents within **Packages** to identify affected scopes when a dependency changes, ensuring the **Project** state remains consistent.

### 3. gdoc Object Datastore

- Role:
  - Acts as the internal storage engine for the **Object Database**, managing the state of **Packages** and **Documents**.
  - Serves as the primary repository for generated object data and their cross-document relationships within a **Project**.

- Characteristics:
  - **Synchronous Implementation**: Composed entirely of synchronous functions to ensure predictable, low-latency data operations.
  - **Encapsulated Component**: Completely hidden from **Frontends** and external components; it is accessible only via the **Object Database**.
  - **No Internal Concurrency Control**: Does not implement its own locking or thread-safety mechanisms. Exclusive access and synchronization are managed externally by the **Object Database**.
  - **In-Memory Storage**: Realized as a collection of optimized in-memory data structures.

- Responsibilities:
  - **Data Persistence**: Stores and manages the lifecycle of gdoc objects and metadata produced by **Jobs**.
  - **Relationship Mapping**: Maintains the physical integrity of links and dependencies between objects.
  - **State Retrieval**: Provides fast lookup capabilities for the **Object Database** to resolve symbols and project structures.

### 4. gdoc Object Builder

- Role:
  - Acts as the execution engine for atomic **Jobs** (Parse, Link, Compile), managing their lifecycle and execution state.
  - Coordinates Job execution when requested by multiple **Tasks** (e.g., from both the Language Server and Object Server).
  - Provides domain-specific logic for different package types and document formats as a plugin.

- Characteristics:
  - **Job Deduplication & Multi-tasking**: If multiple Tasks request the same Job (e.g., parsing the same file), the Builder manages it as a single unit of work shared by those Tasks.
  - **Priority Inheritance**: A Job dynamically inherits the highest priority among all the Tasks currently requesting it.
  - **Reference-based Cancellation**: A Job remains active as long as at least one requesting Task is still alive. It is only canceled when all associated Tasks have been canceled or removed.
  - **Plugin-Based Architecture**: Different builders are implemented for specific content types (e.g., `gdoc`, `doxml`).

- Responsibilities:
  - **Execution Management**: Maintains a registry of active Jobs, tracking which Tasks are waiting for which results.
  - **Content Parsing & Transformation**: Converts raw source content into structured **gdoc Objects** and generates metadata (Semantic Tokens, Symbols).
  - **Diagnostic Generation**: Identifies syntax and semantic errors during the build process to be reported as LSP diagnostics.
  - **Resource Optimization**: Prevents redundant processing by identifying overlapping Job requirements across different Frontends.

## Behaviour: LSP Detailed Sequences

### Scenario Categories

#### Lifecycle Management

- Open Workspace
- Edit Workspace Configuration File

#### Document Synchronization & Updates

- Open Text
- Edit Text
- Close Text
- Update Document
- Bulk File Changes (e.g., Git branch switch)

#### Information Retrieval (Read-only)

- Hover Request
- Go to Definition
- Find References
- Document / Workspace Symbols

#### Dynamic Assistance

- Code Completion

#### Refactoring

- Rename (textDocument/rename)

### 1. Open workspace

#### Triggering events

1. [`initialize`](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#initialize) request:
   - This is the first request sent from the client to the server.
   - The [`InitializeParams`](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#initializeParams) contains:
     - `workspaceFolders`: A list of workspace folders currently open in the IDE. This is the primary source for defining gdoc **Projects**.
     - `rootUri` (Deprecated): The URI of the root workspace folder. Used as a fallback if `workspaceFolders` is not provided.
   - The server uses these URIs to locate `gdoc.project.json` and identify the **Project** scope.

2. [`initialized`](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#initialized) notification:
   - Sent by the client after receiving the `initialize` response.
   - This signal indicates that the client is ready to receive requests and notifications (e.g., capability registration or diagnostics) from the server.

3. [`workspace/didChangeWorkspaceFolders`](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspace_didChangeWorkspaceFolders) notification:
   - Sent when the user adds or removes folders from the workspace dynamically.
   - The server must update its internal **Project** structure and add/remove **Packages** accordingly.

#### Sequence

```mermaid
sequenceDiagram
  participant IDE as Client IDE
  participant LS as Language Server
  participant ODB as Object Database
  participant OBJ as Object Datastore
  participant BLD as Object Builder

  IDE -) +LS: initialize /<br>didChangeWorkspaceFolders
    Loop for each workspaceFolder
      Note over LS: Frontend: Read PROJECT config<br/>and locate Package folders
      Loop for each packageFolder
        LS ->> +ODB: Open Package (Request)
          Note over ODB: Create Task: Initialize Package
          ODB ->> +OBJ: Register Package info
          OBJ -->> -ODB: OK
          ODB -->> -LS: Package Metadata
        LS -) +IDE: client/registerCapability<br>(didChangeWatchedFiles)
      end
    end
  deactivate LS

  IDE -) +LS: Registration Response
    LS ->> +ODB: Build Package (Request)
      Note over ODB: Create Task: Build Package
      ODB ->> +OBJ: Initialize Document entries<br>(State: Created)
      OBJ -->> -ODB: OK
      Loop for each Document
        ODB ->> +BLD: Dispatch Job: Parse/Link
        BLD -->> -ODB: gdoc Objects & Diagnostics
        ODB ->> +OBJ: Store Data & Relationships
        OBJ -->> -ODB: OK
      end
      ODB -->> -LS: Task Handle
  deactivate LS
```

#### Notes

- Registering `DidChangeWatchedFiles` is necessary to receive notifications about file changes in the workspace, which is essential for keeping the gdoc Objects up-to-date. And it should be send before requesting to build the Package, because file changes can happen during the setup process.
  - However, as of LSP 3.17, there is no way for the client to notify the server that it has finished configuring `DidChangeWatchedFiles`. Therefore, the Worker starts building the package only after receiving a response to the registration request.

### 2. Edit Workspace Configuration File

Modifying the workspace configuration file (e.g., `gdoc.project.json`) allows for dynamic updates to the project scope, package definitions, and build settings without requiring a server restart.

#### Triggering events

1. [`textDocument/didSave`](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_didSave) notification:
   - Triggered when the user saves changes to the configuration file within the IDE.
2. [`workspace/didChangeWatchedFiles`](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspace_didChangeWatchedFiles) notification:
   - Triggered when the configuration file is modified externally (e.g., via a version control system or manual file move).

#### Sequence

- [ ] ToDo: check this sequence

```mermaid
sequenceDiagram
  participant IDE as Client IDE
  participant LS as Language Server
  participant ODB as Object Database
  participant OBJ as Object Datastore
  participant BLD as Object Builder

  IDE -) +LS: textDocument/didSave /<br/>didChangeWatchedFiles (config)
    LS ->> +ODB: Update Project Config (Request)
      Note over ODB: Parse new configuration<br/>Compare with existing state
      ODB ->> +OBJ: Update Project/Package Metadata
      OBJ -->> -ODB: OK
      
      alt Package definitions changed
        Note over ODB: Identify added/removed packages
        ODB ->> OBJ: Purge obsolete package data
        ODB ->> OBJ: Initialize new package entries
      end
      
      ODB -->> -LS: Configuration Updated
    LS -) IDE: Update Capabilities (if necessary)
  deactivate LS

  Note over ODB: Background: Trigger Build Tasks<br/>for affected scopes
```

#### Notes

- **Incremental Updates**: The Object Database compares the new configuration with the current state to determine if a full re-scan is necessary or if only specific packages need to be updated.
- **Resource Cleanup**: When a package or folder is removed from the configuration, the Object Database orchestrates the cancellation of pending tasks and the removal of associated objects from the Object Datastore to free system resources.
- **Build Trigger**: Significant changes to build options (e.g., changing search paths or plugin versions) will invalidate existing objects, prompting the Object Database to issue new Jobs to the Object Builder.

### 3. Open Text

- [ ] ToDo: Review this section

When a text document is opened, the Language Server initializes the document's internal state and triggers an analysis workflow. This process ensures that the IDE is immediately populated with diagnostics and semantic information.

#### Triggering events

- The Client IDE sends a [`textDocument/didOpen`](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_didOpen) notification to the Language Server.

#### Sequence

```mermaid
sequenceDiagram
  participant IDE as Client IDE
  participant LS as Language Server
  participant ODB as Object Database
  participant OBJ as Object Datastore
  participant BLD as Object Builder

  IDE -) +LS: textDocument/didOpen
    LS ->> +ODB: Analyze Document (Request)
      Note over ODB: Create Task: Document Analysis
      ODB -->> -LS: Task Handle
    
    Note over ODB: Background Execution
    ODB ->> +BLD: Dispatch Job: Parse & Analyze
    BLD -->> -ODB: gdoc Objects, Diagnostics, & Tokens
    
    ODB ->> +OBJ: Update Document State
    OBJ -->> -ODB: OK
    
    ODB -) LS: Notify: Analysis Complete
    deactivate LS

    activate LS
    LS -) IDE: publishDiagnostics
    LS -) IDE: semanticTokens/full (if requested)
    deactivate LS
```

#### Notes

- **Buffer Synchronization**: The Language Server passes the initial content of the document to the Object Database to ensure the Object Builder works with the latest editor buffer rather than the version on disk.
- **Priority**: Documents opened by the user are assigned high-priority Tasks to ensure low-latency feedback for diagnostics and syntax highlighting.
- **Incremental State**: The Object Datastore tracks the document version to ensure that late-arriving results from background Jobs do not overwrite newer edits.

### 3. Open Text (Original)

When a text document is opened, the language server parses it, reports problems such as diagnostics, and provides semantic token information.

#### Triggering events

- Client IDE sends [`textDocument/didOpen`](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_didOpen) notification to the Language Server.

#### Sequence

```mermaid
sequenceDiagram
  participant IDE as Client IDE
  participant LS as Language Server
  participant ODB as Object Database
  participant OBJ as Object Store
  participant BLD as Object Builder

  IDE -) +LS: textDocument/didOpen
    LS ->> +ODB: Update text
      Note over ODB: Create a Task for<br>Open Text
      ODB -) ODB: Start task
    ODB -->> -LS: Task (Open Text)
    Note over LS: Store Task
    deactivate LS
    %
    ODB -) +ODB: task
    Note over ODB: Compile the Document<br>with the Sub-process<br>Blocking here
    ODB --) LS: Problems<br>(Diagnostic)
      activate LS
      LS --) IDE: Problems<br>(Diagnostic)
      deactivate LS
    alt Ok
      ODB ->> +OBJ: Add document<br>(text and object)
      Note right of OBJ: Store the text<br>with version
      OBJ -->> -ODB: Document added
    end
    ODB --) -LS: Semantic Tokens
      activate LS
      LS --) IDE: Semantic Tokens
      deactivate LS
```

### 4. Edit Text

#### Triggering events

- Client IDE sends [`textDocument/didChange`](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_didChange) notification to the Language Server.

#### Sequence

```mermaid
sequenceDiagram
  participant IDE as Client IDE
  participant LS as Language Server
  participant ODB as Object Database
  participant OBJ as Object Store
  participant BLD as Object Builder

  IDE -) +LS: textDocument/didChange
    LS ->> +ODB: Update text
      ODB -) ODB: task
    ODB -->> -LS: Ok
    Note over LS: Store Task
    deactivate LS
    %
    ODB -) +ODB: task
    Note over ODB: Compile the Document<br>with the Sub-process<br>Blocking here
    ODB --) LS: Problems<br>(Diagnostic)
      activate LS
      LS --) IDE: Problems<br>(Diagnostic)
      deactivate LS
    alt Ok
      ODB ->> +OBJ: Add document<br>(text and object)
      Note right of OBJ: Store the text<br>with version
      OBJ -->> -ODB: Document added
    end
    ODB --) -LS: Semantic Tokens
      activate LS
      LS --) IDE: Semantic Tokens
      deactivate LS
```

### 6. Update Document

#### Triggering events

1. `Update Document` request from Background Worker itself:
   - This case, it's an internal request from gdoc Object Database descrived above.
2. [`workspace/didChangeWatchedFiles`](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspace_didChangeWatchedFiles) notification:
   - Sent when a file in the workspace is changed, created, or deleted.
   - The notification includes a list of [`FileEvent`](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#fileEvent), where each [`FileEvent`](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#fileEvent) has a [`uri`](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#documentUri) and a [`type`](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#fileChangeType) (Created, Changed, or Deleted).

#### Sequence

```mermaid
sequenceDiagram
  participant IDE as Client IDE
  participant LS as Language Server
  participant ODB as Object Database
  participant OBJ as Object Store
  participant BLD as Object Builder

  %% Trigger
  Note over IDE, DB: Trigger
  alt from Background Worker
    ODB ->> ODB: Update Document (Created)
  else by DidChangeWatchedFiles
    IDE ->> +LS: Notify file change<br>with DidChangeWatchedFiles
      LS ->> +ODB: Update a File
      alt Created
        ODB ->> ODB: Update Document (Created)
      else Changed
        ODB ->> ODB: Update Document (Changed)
      else Deleted
        ODB ->> ODB: Update Document (Deleted)
      end
    ODB -->> -LS: Response
    deactivate LS
  end
  %% Update Document
  Note over IDE, DB: Update Document (Document URI, type)
  activate Worker
  alt Created
    ODB ->> +OBJ: Add document<br>(not yet parsed)
    OBJ -->> -ODB: Document added
    Note over ODB: Create Task Queue<br>for the document and append<br>the task to parse the document
  else Changed
    Note over ODB: Append the task<br>to parse the document
  else Deleted
    Note over ODB: Cancel tasks<br>and delete the Queue
    ODB ->> +OBJ: Delete document
    OBJ -->> -ODB: Document deleted
  end
  deactivate Worker
```

#### Notes

- `Task Queue`
  - It's a queue of tasks for each document. It is used to manage the tasks for each document and to ensure that the tasks are executed in order. For example, if there are multiple file editing events for the same file, only the latest one should be processed. Therefore, when a new task is added to the queue, the previous tasks in the queue should be canceled.

### 8. Hover Request

#### Triggering events

> The [`Hover Request`](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_hover) is sent from the client to the server to request hover information at a given text document position.

#### Sequence

```mermaid
sequenceDiagram
  participant IDE as Client IDE
  participant LS as Language Server
  participant ODB as Object Database
  participant OBJ as Object Store
  participant BLD as Object Builder

  IDE -) +LS: Hover Request with<br>textDocument/hover
    LS ->> +OBJ: Get data
    OBJ -->> -LS: Hover Data or Need to compile
    alt if Need to compile Object
      Note over LS: Create Task
      Loop while Need to compile next Object
        Note over LS: Create a Request Form<br>to Compile next Object
        LS -) +ODB: Request Form
        deactivate LS
          Note over ODB: Compile the Document<br>with the Sub-process<br>Blocking here
          ODB ->> +OBJ: Add document
          OBJ -->> -ODB: Document added
        ODB --) -LS: Request Form (Done)
        activate LS
          LS ->> +OBJ: Get data
          OBJ -->> -LS: Hover Data
        end
      Note over LS: Delete Task
    end
  LS --) IDE: Hover | null
  deactivate LS
```

## Detailed Design Guidelines

### Workspace, Project And Package

### Task Management

#### Priority

1. LSP messages from the client IDE
   - Messages from the client must be handled with the highest priority
   - However, avoid implementing complex processing to keep execution time to a minimum
2. Tasks to resolve LSP requests from the client IDE
   - If responding to an LSP request requires more complex processing, these tasks should be executed after the initial handling of the LSP messages to ensure that the server remains responsive to the client.
3. Tasks to update gdoc Objects in the Object Database
   - These tasks can be executed with lower priority as they are not directly related to responding to the client IDE's requests.
   - However, they should still be executed in a timely manner to ensure that the gdoc Objects are up-to-date for any subsequent LSP requests that may require information from the Object Database.
   - The priority is as follows:
     1. Compile and link documents referenced by open text files
     2. Compile and link documents referenced by the unopened referenced documents mentioned above
     3. Following the above, compile and link the referenced documents in the order of their reference levels from the open text
     4. Documents that are neither open nor referenced are compiled and linked last.

#### Task Scheduling

##### Overview

- Tasks managed by gdoc Object Database are those of priority 2 and later in the list above.
- The priority changes every time an LSP message is received (i.e., every time the user interacts with the client IDE). Priority adjustment is performed while processing item 1 above.
- For example, a definition lookup task requested for hover display decreases in priority when the user performs actions such as editing a different file.

##### Scheduling Method

###### Dependency States

1. Active client requests (not cancelled)
   - Documents required by the requests increase in priority, regardless of whether they are open or not.

2. Open text documents
   - If a text document is closed, requests that assume the text document is open are cancelled (e.g., hover information for a closed file is no longer used).
   - Documents referenced by an open text document increase in priority, regardless of whether they are open or not.

3. Part of a package
   - Documents included in a package have higher priority than those that are in the workspace but not part of any package.
   - Changes to the package settings in the workspace (project) root configuration file can alter this state.
     - Changes to configuration files are not affected by changes to open text documents and are only reflected upon saving.

###### State-based Scheduling

- Every document in the workspace has state variables corresponding to the conditions above.
  - When a request is received from the client, the involved document enters state 1.
  - When state 1 is cleared, the task is rescheduled based on the priority determined by state 2 or 3.

- Note(1):
  - If multiple requests require a single document, the document remains in state 1 until all requests are cancelled.

- Memo:
  - A single request may require multiple referenced documents:
    - In many cases, it is not possible to determine if there are subsequent referenced documents without compiling and linking the first referenced document.
    - In other words, the referenced documents required by the request become sequentially apparent during request processing.
  - As an exception, when all references to a certain object are requested, it is necessary to complete all compilations and links of 2.
  - Task scheduling is managed per client.
    - There is one LSP client, but there may be multiple object database clients.

#### Task and Subtask

- A single request always corresponds to a single task. Processing tasks such as compilation and linking required within a task are managed as subtasks.
  - A single task can contain multiple subtasks.

- Tasks correspond to requests from clients, including both requests from the LSP client and requests from the Object Database client.
  - Therefore, task management is divided into parts that differ by client type and parts that are common to all clients.
  - The common part is priority management. The gdoc server provides an abstract class implementing only this common part and concrete classes implementing the parts that differ by client type.
