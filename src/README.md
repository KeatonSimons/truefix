# src/ — placeholder

This folder will contain the Swift / SwiftUI source for the TrueFix app once a developer collaborator joins the project.

The intended structure, from the V1 spec:

```
src/
├── TrueFix/                  # SwiftUI app
│   ├── App.swift
│   ├── Views/
│   ├── ScanEngine/
│   │   ├── RuleLoader.swift
│   │   ├── Detectors/
│   │   │   ├── ChromePolicyDetector.swift
│   │   │   ├── ExtensionFolderDetector.swift
│   │   │   ├── ConfigProfileDetector.swift
│   │   │   └── LaunchAgentDetector.swift
│   │   └── Reporter.swift
│   └── Resources/
│       └── rules/            # bundled YAML rule packs from ../../rules
└── TrueFixHelper/            # privileged XPC helper (SMAppService)
    ├── HelperTool.swift
    └── Actions/
        ├── DefaultsDeleteKey.swift
        ├── RemoveDirectory.swift
        ├── RemoveProfile.swift
        └── UnloadAndRemovePlist.swift
```

See [../docs/V1-SPEC.md](../docs/V1-SPEC.md) section 5 for the architecture, and [../CONTRIBUTING.md](../CONTRIBUTING.md) for what we're looking for in a collaborator.
