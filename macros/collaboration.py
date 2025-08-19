def define_env(env):
    """
    Hook de mkdocs-macros-plugin pour les macros de collaboration.
    """

    @env.macro
    def collaboration_block(titre="Principe de Collaboration 🛠️ 🧰 🧵 🧪"):
        return f"""
???+ abstract "{titre}"

    * → Un à 3 ajouts et/ou modifications max par commit et par jour
    
    * → Des pages d'aides éventuellement seront listées ICI selon réactions de chacun...
    
    @ vous d'jouer 😀 !
"""
