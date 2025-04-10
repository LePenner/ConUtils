# Docstring Styleguide

## Usage

This guide aims to clarify how to write short and precise
documentation for packages, classes, methods, etc., to further understanding of the codebase by
introducing minimalist principles, to inforce these values.

## Principles

### General

 1. **Don't state the obvious**. Anything clearly stated by the **signature**
 is redundant and thus should not be documented. Avoid phrases like
 "This function does..." or "argument_x (int)".
 
 2. The description is twofold: 
     - the first line should explain the **essential functionality**.
     - *if more explenation is needed it is to be done in the following lines
     and in as much depth as nessecary without overexplaining*
 
 3. Use **bold** for key information, *italic* for optional behavior,
     and `monospace` for anything in code eg. methods, variables, classes...

## Further specifying
 
- ### Methods, Functions and Classes
    
    - may define an `Interface` section where clarification 
    on `inputs` and `outputs` is specified:
    
        ```python
        def function(x, y, magic: Magic.magic) -> magic_coordinates:
            """Process coordinates for a wizzard.

            Infuses `x` and `y` with `magic` and
            calls function :func:`process_magic`.

            Interface
                takes:
                    - magic: provides a spell,
                        see :class:`magic` in magic.py
            """
            # ...
        ```
    - #### after Interface
        - **functions and methods**: may define `takes` and `returns`
        - **classes**: may define `inherits`, public `methods` 
        and public `arguments`, any nonpublic attributes are to be explained
        in their respective method and/or the class description.
        Wrappers and decorators are to be treated from the public perspective.
    
- ### Packages

    - to be expanded on

