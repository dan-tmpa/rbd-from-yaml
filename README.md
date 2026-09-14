# RBD YAML Reader

Small Python application for defining Reliability Block Diagrams (RBDs) in YAML and calculating system reliability at a specified mission time.

The current implementation supports:

- series logic;
- parallel logic;
- nested series/parallel blocks;
- exponential reliability models;
- Weibull reliability models;
- constant reliability values;
- mission time defined in YAML or overridden from the command line.

## Installation

```bash
python -m venv .venv
```

Activate the environment and install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py examples/pumping_system.yaml
```

Override the mission time:

```bash
python main.py examples/pumping_system.yaml --time 10000
```

Print component reliabilities as well:

```bash
python main.py examples/pumping_system.yaml --components
```

## YAML specification

A YAML input file has four main sections:

```yaml
system:
  ...

components:
  ...

rbd:
  ...

analysis:
  ...
```

### `system`

Optional metadata about the system.

```yaml
system:
  id: SYS-001
  name: Pumping System
```

The program currently uses `name` only for display purposes.

### `components`

`components` is a mapping whose keys are unique component identifiers.

```yaml
components:
  P1:
    type: pump
    reliability:
      distribution: exponential
      lambda: 1.0e-5
```

The component `type` is metadata and does not affect the calculation in the current version.

Every component must contain a `reliability` mapping.

#### Exponential model

For a constant failure rate $\lambda$:

$$
R(t)=e^{-\lambda t}
$$

YAML:

```yaml
reliability:
  distribution: exponential
  lambda: 1.0e-5
```

`lambda` must use the reciprocal of the time unit used for the mission time.

#### Weibull model

For Weibull shape parameter $\beta$ and scale parameter $\eta$:

$$
R(t)=\exp\left[-\left(\frac{t}{\eta}\right)^\beta\right]
$$

YAML:

```yaml
reliability:
  distribution: weibull
  beta: 2.0
  eta: 50000
```

`eta` must use the same time unit as the mission time.

#### Constant model

Useful for testing or when reliability is already supplied directly:

```yaml
reliability:
  distribution: constant
  value: 0.99
```

`value` must be between 0 and 1.

## RBD specification

The `rbd` section defines the logical structure of the Reliability Block Diagram.

Each entry is either:

1. a component reference; or
2. a `series` or `parallel` logic block.

### Component reference

```yaml
- component: P1
```

The identifier must exist in `components`.

### Series block

```yaml
rbd:
  type: series
  blocks:
    - component: A
    - component: B
    - component: C
```

The blocks are interpreted in the sequence in which they appear in the YAML file.

For independent components:

$$
R_{series}=\prod_i R_i
$$

### Parallel block

```yaml
rbd:
  type: parallel
  blocks:
    - component: A
    - component: B
```

For independent components:

$$
R_{parallel}=1-\prod_i(1-R_i)
$$

### Nested logic

Series and parallel blocks can be nested arbitrarily.

```yaml
rbd:
  type: series
  blocks:
    - type: parallel
      blocks:
        - component: P1
        - component: P2
    - component: V1
    - component: HX1
```

This corresponds to:

```text
      +-- P1 --+
------|        |------ V1 ------ HX1 ------
      +-- P2 --+
```

or mathematically:

```text
(P1 || P2) -> V1 -> HX1
```

The order of the entries in `blocks` is preserved and represents their sequence in the diagram. For pure reliability calculation, the order of independent elements in a series block does not change the numerical result, but it is retained so the same structure can later be used for visualization or graph generation.

## Analysis section

The mission time can be declared in the YAML file:

```yaml
analysis:
  mission_time: 8760
  time_unit: hour
```

`time_unit` is descriptive in the current implementation. The user is responsible for ensuring that all model parameters use compatible units.

A command-line `--time` value overrides `analysis.mission_time`.

## Complete example

```yaml
system:
  id: SYS-001
  name: Pumping System

components:
  P1:
    type: pump
    reliability:
      distribution: exponential
      lambda: 1.0e-5

  P2:
    type: pump
    reliability:
      distribution: exponential
      lambda: 1.2e-5

  V1:
    type: valve
    reliability:
      distribution: weibull
      beta: 1.5
      eta: 100000

rbd:
  type: series
  blocks:
    - type: parallel
      blocks:
        - component: P1
        - component: P2
    - component: V1

analysis:
  mission_time: 8760
  time_unit: hour
```

## Assumptions

The current analytical equations assume statistical independence among component failures.

The repository intentionally separates:

- YAML parsing;
- RBD structure;
- reliability models; and
- RBD evaluation.

This makes it straightforward to add additional distributions or logic types later, such as `k_out_of_n` blocks.

## Running tests

From the root directory, run:

```bash
python -m pytest
```

## Repository structure

```text
rbd-yaml-reader/
├── main.py
├── README.md
├── requirements.txt
├── examples/
│   └── pumping_system.yaml
├── rbd/
│   ├── __init__.py
│   ├── evaluator.py
│   ├── io.py
│   ├── models.py
│   └── parser.py
└── tests/
    └── test_rbd.py
```
