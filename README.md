# Apple-Style Strong Password Generator

Generates passwords that follow **Apple's strong password pattern** with **configurable length**.

### Default (classic Apple)
```
xxxxxx-xxxxxx-xxxxxx          ← 3 blocks = 18 characters
```

### Custom length
```
--blocks 1   →  xxxxxx
--blocks 2   →  xxxxxx-xxxxxx
--blocks 4   →  xxxxxx-xxxxxx-xxxxxx-xxxxxx
--blocks 10  →  60-character password
```

---

## Rules (same as Apple)

- CVC syllables (Consonant-Vowel-Consonant)
- Only non-ambiguous characters (no `l`, `1`, `0`, `O`…)
- Exactly **one** uppercase letter
- Exactly **one** digit on a block boundary
- Blocklist filter
- Cryptographically secure randomness (`secrets`)

---

## Usage

```bash
cd passwd-gen

# Classic Apple password (18 chars)
python3 passgen.py

# Shorter or longer
python3 passgen.py --blocks 1
python3 passgen.py --blocks 5
python3 passgen.py --blocks 10

# Generate many
python3 passgen.py -n 100
python3 passgen.py -n 1000000 -o million.txt

# Long + many
python3 passgen.py -n 50 --blocks 6 -o strong.txt
```

### Options

| Flag            | Description                                              |
|-----------------|----------------------------------------------------------|
| `-n N`          | Number of passwords (can be very large, e.g. 1 000 000) |
| `-b / --blocks` | Number of 6-char blocks (default: 3)                     |
| `-o FILE`       | Write to file                                            |
| `-q`            | Quiet mode                                               |

### Length reference

| Blocks | Characters (without hyphens) | Example shape                  |
|--------|------------------------------|--------------------------------|
| 1      | 6                            | `xxxxxx`                       |
| 2      | 12                           | `xxxxxx-xxxxxx`                |
| 3      | 18 (Apple default)           | `xxxxxx-xxxxxx-xxxxxx`         |
| 4      | 24                           | `xxxxxx-xxxxxx-xxxxxx-xxxxxx`  |
| 5      | 30                           | …                              |
| 10     | 60                           | very long                      |

You can go higher (up to 1000 blocks). Generating 1 trillion passwords is theoretically possible with `-n` but will take an extremely long time and require enormous storage.
