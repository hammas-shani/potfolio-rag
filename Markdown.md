graph TD
    %% Styling
    classDef source fill:#f9f871,stroke:#333,stroke-width:2px;
    classDef script fill:#ffc75f,stroke:#333,stroke-width:2px;
    classDef db fill:#ff9671,stroke:#333,stroke-width:2px;
    classDef model fill:#ff6f91,stroke:#333,stroke-width:2px;
    classDef ui fill:#d65db1,stroke:#333,stroke-width:2px,color:#fff;
    classDef user fill:#845ec2,stroke:#333,stroke-width:2px,color:#fff;

    %% Nodes
    A[GitHub Repositories]:::source
    B(Data Sync Script):::script
    C[(Local Dataset)]:::db
    D(Text Splitter & Embeddings):::script
    E[(Main Vector DB)]:::db
    F((User)):::user
    G[Chainlit UI]:::ui
    H[(Semantic Cache DB)]:::db
    I(Groq LLM):::model

    %% Data Pipeline (Backend)
    A -->|Fetch READMEs| B
    B -->|Save as Markdown| C
    C -->|Chunk & Encode| D
    D -->|Store Vectors| E

    %% Interaction Pipeline (Frontend)
    F -->|Asks Question| G
    G -->|Check Similarity| H
    
    %% Cache Hit/Miss Logic
    H -- Cache Hit -->|Return Fast Answer| G
    H -- Cache Miss -->|Search Context| E
    E -->|Provide Context| I
    I -->|Generate Answer| H
    H -->|Save New Answer| G
    G -->|Display Output| F
