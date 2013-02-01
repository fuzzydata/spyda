try:
    from calais import Calais
except ImportError:
    Calais = None  # NOQA


if Calais is not None:
    def process_calais(content, key=None):
        if key is None:
            return {}

        calais = Calais(key)
        response = calais.analyze(content)

        people = [entity["name"] for entity in response.entities if entity["_type"] == "Person"]

        return {"people": people}
