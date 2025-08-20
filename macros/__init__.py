from pyodide_mkdocs_theme.pyodide_macros import PyodideMacrosPlugin
from . import one_citation_a_day, all_citations, collaboration


def define_env(env: PyodideMacrosPlugin):

    # env.macro(one_citation_a_day)      # my_file1 contient une fonction "macro1"
    one_citation_a_day.define_env(env)
    all_citations.define_env(env)
    collaboration.define_env(env)
    # env.macro(my_file1.macro2)

    # Ou créer les macros directement ici (mais le package n'a alors plus d'intérêt...)
    # @env.macro
    # def macroX(...) : ...

    # 2dbug retrait icon/lien pour éditer la page dans pages dynamiques
