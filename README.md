# Apple-Style Strong Password Generator

Generates passwords that follow **Apple's strong password pattern** with **configurable length**.

### Default (classic Apple)
xxxxxx-xxxxxx-xxxxxx          ← 3 blocks = 18 characters

### Custom length
--blocks 1   →  xxxxxx
--blocks 2   →  xxxxxx-xxxxxx
--blocks 4   →  xxxxxx-xxxxxx-xxxxxx-xxxxxx
--blocks 10  →  60-character password

---

## Rules (same as Apple)

- CVC syllables (Consonant-Vowel-Consonant)
- Only non-ambiguous characters (no `l`, `1`, `0`, `O`…)
- Exactly **one** uppercase letter
- Exactly **one** digit on a block boundary
- Blocklist filter
- Cryptographically secure randomness (`secrets`)

---

## Installation (Global Command)

You can install the generator as a global `passgen` command so you can run it from anywhere in your terminal.

1. Navigate into the project folder:
   ```bash
   cd passwd-gen
   ```
2. Make the install script executable:
   ```bash
   chmod +x install.sh
   ```
3. Run the installation (requires `sudo` password):
   ```bash
   ./install.sh
   ```

*(To uninstall later, simply run `sudo rm /usr/local/bin/passgen`.)*

---

## Usage

### With global command (recommended)

```bash
# Classic Apple password (18 chars)
passgen

# Shorter or longer
passgen --blocks 1
passgen --blocks 5
passgen --blocks 10

# Generate many
passgen -n 100
passgen -n 1000000 -o million.txt

# Long + many
passgen -n 50 --blocks 6 -o strong.txt
```

### Without installation (via Python)

```bash
cd passwd-gen
python3 passgen.py
python3 passgen.py --blocks 5
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
