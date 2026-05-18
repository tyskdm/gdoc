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

<!-- markdownlint-disable-next-line MD024 -->
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
  - Concurrency control for accessing gdoc Objects to prevent race conditions.
  - Provide APIs to manage gdoc Objects and their relationships.
  - Provide APIs to subscribe to and notify about changes in gdoc Objects.

- Characteristics:
  - Concurrency control is for asyncio tasks in other components, not for multi-threading.
  - Realized as a thin wrapper around in-memory data structures.

- Responsibilities:
  - Manage gdoc Objects and their relationships.
  - Provide APIs to notify about changes using callback functions or event emitters.

### 4. gdoc Object Builder

- Role:
  - Performs tasks such as compiling and linking gdoc objects.
  - Manages the server requirements in a queue and processes them one by one.
  - Overrides previous requirements if there are multiple requirements of the same type.
    - e.g., if there are multiple file editing events for the same file, only the latest one should be processed.

- Characteristics:
  - Performs various tasks related to gdoc documents.
  - Requirements from the Language Server are sent asynchronously depending on user actions.

- Responsibilities:
  - Manage the server requirements queue and async tasks corresponding to the requirements.
  - Mutual exclusion / synchronization of the tasks so that they don't violate database consistency.
    - Locking mechanism for the database is the responsibility of the Async Database, but task scheduling and synchronization is the responsibility of gdoc Object Database.

## Behaviour: LSP Detailed Sequences

1. Open workspace
2. Update Document
3. Open Text
4. Edit Text
5. Hover Request
6. Go to definition
7. Find references
8. Edit workspace configuration file

### 1. Open workspace

#### Triggering events

1. [`interface InitializeParams`](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#initializeParams), the parameter of [`initialize`](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#initialize) request:
   - Includes `workspaceFolders` and `rootUri` to notify the Language Server `rootUri` and `workspaceFolders` when the workspace is opened.
   - `workspaceFolders` is a list of workspace folders (List of `WorkspaceFolder`), where each `WorkspaceFolder` has a `uri` and a `name`.
   - and `rootUri` is the URI of the root workspace folder without the folder name.

2. [`workspace/didChangeWorkspaceFolders`](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspace_didChangeWorkspaceFolders) notification:
   - Sent when the workspace folders are changed (e.g., added, removed, or changed).

#### Sequence

```mermaid
sequenceDiagram
  participant IDE as Client IDE
  participant LS as Language Server
  participant ODB as Object Database
  participant OBJ as Object Store
  participant BLD as Object Builder

  IDE -) +LS: Workspace added
    Loop for workspaceFolder in workspaceFolders
      Note over LS: Read PROJECT<br>configuration file and<br>locate Package folders
      Loop for packageFolder in workspaceFolder
        LS ->> +ODB: Open Package
          Note over ODB: Read PACKAGE<br>configuration file
            ODB ->> +OBJ: Add a new Package<br>and Update the Package<br>information
            OBJ -->> -ODB: Package information updated
        ODB -->> -LS: Package information
        LS -) +IDE: Register<br>DidChangeWatchedFiles
      end
    end
  deactivate LS
  %%
  IDE -) +LS: Responce to register<br>DidChangeWatchedFiles
    deactivate IDE
    LS ->> +ODB: Build Package
      Note over ODB: Create a Task<br>for Build Package
      Note over ODB: Prepair to<br>Build Package
      Loop for document in packageFolder
        ODB ->> ODB: Update Document (Created)
      end
     ODB -->> -LS: Task (Package)
  deactivate LS
```

#### Notes

- Registering `DidChangeWatchedFiles` is necessary to receive notifications about file changes in the workspace, which is essential for keeping the gdoc Objects up-to-date. And it should be send before requesting to build the Package, because file changes can happen during the setup process.
  - However, as of LSP 3.17, there is no way for the client to notify the server that it has finished configuring `DidChangeWatchedFiles`. Therefore, the Worker starts building the package only after receiving a response to the registration request.

### 2. Update Document

<!-- markdownlint-disable-next-line MD024 -->
#### Triggering events

1. `Update Document` request from Background Worker itself:
   - This case, it's an internal request from gdoc Object Database descrived above.
2. [`workspace/didChangeWatchedFiles`](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspace_didChangeWatchedFiles) notification:
   - Sent when a file in the workspace is changed, created, or deleted.
   - The notification includes a list of [`FileEvent`](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#fileEvent), where each [`FileEvent`](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#fileEvent) has a [`uri`](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#documentUri) and a [`type`](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#fileChangeType) (Created, Changed, or Deleted).

<!-- markdownlint-disable-next-line MD024 -->
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
<!-- markdownlint-disable-next-line MD024 -->
#### Notes

- `Task Queue`
  - It's a queue of tasks for each document. It is used to manage the tasks for each document and to ensure that the tasks are executed in order. For example, if there are multiple file editing events for the same file, only the latest one should be processed. Therefore, when a new task is added to the queue, the previous tasks in the queue should be canceled.

### 3. Open Text

When a text document is opened, the language server parses it, reports problems such as diagnostics, and provides semantic token information.

<!-- markdownlint-disable-next-line MD024 -->
#### Triggering events

- Client IDE sends [`textDocument/didOpen`](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_didOpen) notification to the Language Server.

<!-- markdownlint-disable-next-line MD024 -->
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

<!-- markdownlint-disable-next-line MD024 -->
#### Triggering events

- Client IDE sends [`textDocument/didChange`](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_didChange) notification to the Language Server.

<!-- markdownlint-disable-next-line MD024 -->
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

### 5. Hover Request

<!-- markdownlint-disable-next-line MD024 -->
#### Triggering events

> The [`Hover Request`](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_hover) is sent from the client to the server to request hover information at a given text document position.

<!-- markdownlint-disable-next-line MD024 -->
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
