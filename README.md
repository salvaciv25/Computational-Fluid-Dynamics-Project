# Numerical Investigation of Vortex Shedding Past Bluff Bodies

This repository contains a comparative CFD study of unsteady laminar flow past three different 2D bluff body geometries: **Circular**, **Square**, and **Hexagonal** cylinders. The project was developed using the **Kratos Multiphysics** framework.

## Project Overview

The study investigates how geometric variations affect wake dynamics, vortex shedding frequencies, and aerodynamic forces at a fixed Reynolds number (Re = 100).

### Key Features

* **Solver:** Kratos Multiphysics (Monolithic Finite Element formulation).
* **Stabilization:** Variational Multiscale (VMS) and Quasi-Static VMS (QSVMS).
* **Physics:** Incompressible Navier-Stokes equations.
* **Analysis:** Spectral analysis of lift signals to determine the **Strouhal Number (St)**.

## Numerical Methodology

* **Discretization:** Unstructured FEM mesh (~10,000 elements) with refinement in the wake region.
* **Temporal Scheme:** Implicit time integration.
* **Boundary Conditions:** * *Inlet:* Parabolic velocity profile ().
* *Outlet:* "Do-nothing" boundary condition.
* *Body:* No-slip condition.



##  Results & Discussion

The simulations successfully captured the formation of a **Von Kármán vortex street** for all geometries.

### Aerodynamic Comparison

The sharp corners of the square and hexagonal cylinders lead to stronger flow separation compared to the circular cylinder, resulting in higher drag and lift fluctuations.

| Geometry | Strouhal Number () | Mean  | RMS  |
| --- | --- | --- | --- |
| **Circular** | 0.222 | 2.119 | 0.713 |
| **Square** | 0.182 | 4.294 | 1.737 |
| **Hexagonal** | 0.250 | 3.099 | 0.946 |

### Visualizations

The wake patterns were analyzed using velocity and vorticity fields.

* **Circular:** Exhibits a well-organized, symmetric vortex street.
* **Square:** Generates a wider recirculation region and the highest drag coefficient.
* **Hexagonal:** Shows intermediate behavior with the highest shedding frequency ().

## Repository Structure

* `kratos_files/`: ProjectParameters.json, MDPA mesh files, and MainKratos.py.
* `scripts/`: Python scripts for post-processing and FFT analysis of lift/drag signals.

## How to Run

1. Install [Kratos Multiphysics](https://www.google.com/search?q=https://github.com/KratosMultiphysics/Kratos).
2. Clone this repository.
3. Run the simulation:
```bash
python3 MainKratos.py

```

4. Run the post-processing script:
```bash
python3 scripts/post_process.py

```

