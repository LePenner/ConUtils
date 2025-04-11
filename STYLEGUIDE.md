# Styleguide

## General 

Follow PEP8 standards on a basic level, pythonic code is encuraged - use a tool,
like autopep8. Strict type checking is enforced, 
exceptions are evaluated on a per case basis.

### Classes

- should be structured as follows:

    #### head

    - `docstring`
    - `constructor`
    - `attributes` and `methods` outside the `constructor`,
    but only used by the `construcor`,
    these should **always** be private
    - for automatic doc generation add `# @constructor` in front of
    the `constructor`, this **includes** private constructor methods,
    as they serve as an extension of the constructor

    #### body
    - from top down: split into **`private`**, **`protected`** and **`public`**,
    to generate automatic docs, indicate sections with `# @private`, `# @protected`
    and `# @public`, ***if in use***
    - for every section: first define its `classattributes` and
    after define the `classmethods`
    - **note:** `properties` count as `attributes` and should be at
    the end of `classattributes`, it is best practice to follow the `property`
    declaration immediatly by its `setter`
    - **decorated `methods`** sould be grouped at the top of `classmethods`
    sorted by occurrence

        ```python
        # NOT TYPEHINTED
        # MISSING DOCUMENTATION
        
        class Magician():
            """Magical docstring."""

        # @constructor

            def __init__(self, magic_wand):
                self._wand = magic_wand
                self.add_wand(magic_wand)
                self._magic = self.__merlin_conversion(magic_wand)

            def __merlin_conversion(self, magic_wand):
                # ...

        # @protected

            _wand_collection = [] 

            def _reset_magic(self):
                # ...
            
        # @public

            @property
            def magic(self):
                return self._magic
            
            @magic.setter
            def magic(self, magic):
                #...
                self._magic = magic
            
            @classmethod
            def add_wand(cls, wand):
                cls._wand_collection.append(wand)
            
            @classmethod
            def remove_wand(cls, wand):
                cls._wand_collection.remove(wand)

            @staticmethod
            def ask_merlin(args):
                # ...
                return merlin_answer

            def spell_effectiveness(self, spell):
                return self.ask_merlin((self._wand, self.magic, spell))
        ```

    #### notes
    - docmarkings **are** optional but nice to have 
    - the above example has no `private` section and thus does not
    add the `# @private` indicator
---         

# Docstring Styleguide

## Usage

This guide aims to clarify how to write short and precise
documentation for packages, classes, methods, etc., to furtherunderstanding
of the codebase by introducing minimalist principles, to inforce these values.

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
    
    - need to be typehinted, as types are not part of the documentation
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

    - may define an `@Exposes` section as interface

        ```python
        # package/
        """Contains different kinds of spells, all making use of :class:`Spell`

        @Exposes
            classes
                - :class:Arcana
                - :class:Fire
                - :class:Mele
        """

        from .arcana import Arcana
        from .fire import Fire
        from .mele import Mele

        __all__ = ["Arcana", "Fire", "Mele"]
        ```

    - #### note the import structure:
        - packages should **only** expose the interface, **not** take in arguments 
        - dependencies are declared on a per file basis via **relative import** 
        

            ```python
            # package/arcana.py

            from .. import Spell

            class Arcana(Spell):
                def __init__(self, ...)
                # ...
            ```
    
    


