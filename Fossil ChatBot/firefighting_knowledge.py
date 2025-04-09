"""
Firefighting knowledge base for the decision-making AI app.
"""

# Knowledge base for different firefighting strategies
FIREFIGHTING_KNOWLEDGE = {
    "defensieve_buiteninzet": {
        "doel": [
            "Het voorkomen van uitbreiding naar belendende panden",
            "Het voorkomen van milieuschade",
            "Het beperken van de effecten van rook"
        ],
        "criteria": [
            "Brand heeft zich al verspreid",
            "Directe interventie is te gevaarlijk",
            "Brand is niet meer te blussen van binnen",
            "Er is geen direct gevaar voor mensenlevens"
        ],
        "risico's": [
            "Uitbreiding van de brand",
            "Milieuschade door bluswater",
            "Rookverspreiding",
            "Schade aan omliggende gebouwen"
        ],
        "technieken": [
            "Water geven op afstand",
            "Ventilatie van buitenaf",
            "Brandwacht houden",
            "Monitoring van de situatie"
        ]
    },
    "offensieve_buiteninzet": {
        "doel": [
            "Verbeteren van levenscondities van eventuele slachtoffers",
            "Mogelijk maken van een veilige betreding",
            "Voorkomen van uitbreiding",
            "Blussen van de brand"
        ],
        "criteria": [
            "Er zijn slachtoffers in het gebouw",
            "Directe toegang is te gevaarlijk",
            "Brand is nog beperkt",
            "Er is kans op succesvolle interventie"
        ],
        "risico's": [
            "Flashover",
            "Backdraft",
            "Instorting",
            "Verslechtering van de situatie"
        ],
        "technieken": [
            "Koude snede",
            "Massale aanval",
            "Ventilatie van buitenaf",
            "Brandwacht houden"
        ]
    },
    "defensieve_binneninzet": {
        "doel": [
            "Gelegenheid bieden voor een evacuatie",
            "Het voorkomen van uitbreiding",
            "Het voorkomen van rookverspreiding",
            "Schadebeperking"
        ],
        "criteria": [
            "Er zijn nog mensen in het gebouw",
            "Brand is nog niet volledig ingeperkt",
            "Evacuatie is mogelijk",
            "Er is voldoende beveiliging"
        ],
        "risico's": [
            "Flashover",
            "Backdraft",
            "Instorting",
            "Rookverspreiding"
        ],
        "technieken": [
            "Ventilatie van binnenuit",
            "Brandwacht houden",
            "Evacuatie begeleiden",
            "Brandcompartimentering behouden"
        ]
    },
    "offensieve_binneninzet": {
        "doel": [
            "Redding van mensen",
            "Bestrijding van brand"
        ],
        "criteria": [
            "Directe redding van mensenlevens vereist",
            "Brand is nog beperkt",
            "Er is voldoende beveiliging",
            "Er is kans op succesvolle interventie"
        ],
        "risico's": [
            "Flashover",
            "Backdraft",
            "Instorting",
            "Verslechtering van de situatie"
        ],
        "technieken": [
            "Directe brandbestrijding",
            "Redding van slachtoffers",
            "Brandcompartimentering behouden",
            "Ventilatie van binnenuit"
        ]
    }
}

def get_strategy_info(strategy_name: str) -> dict:
    """
    Get information about a specific firefighting strategy.
    
    Args:
        strategy_name (str): The name of the strategy to get information about.
        
    Returns:
        dict: Information about the strategy.
    """
    return FIREFIGHTING_KNOWLEDGE.get(strategy_name, {})

def get_all_strategies() -> list:
    """
    Get a list of all available firefighting strategies.
    
    Returns:
        list: A list of strategy names.
    """
    return list(FIREFIGHTING_KNOWLEDGE.keys()) 