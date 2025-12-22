# Candidates Service

Candidates Service provides other services like the Cache Populator with the potential candidates for the fresh batch of videos.

### Overview

The overall flow is like this:

```
    Context -> Filter Endorse and Reject Keywords -> Initialize our YT API wrapper -> Pool videos by searching endorse keywords -> Filter Using reject keywords -> Parse the noisy JSON into pydantic models -> Return the list
```

### Planned next steps:

1. Replace static context with dynamic one by setting up API at the other end.
2. Implementation of techniques to pool the maximum number of videos in order to serve content frequently and on user demand without exhausting quota.
3. An effective filter layer to block short form of content, cringe, and slop.

### Procedure to run:

1. Go to candidates_service\main.py and uncomment the file dumping portions of code to review the outputs.
2. From the root do: (A venv is recommended)
   ```
       pip install -r requirements.txt
       python -m candidates_service.main
   ```
3. Review the output files.
