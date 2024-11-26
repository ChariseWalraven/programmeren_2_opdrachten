from collections.abc import Callable
from typing import Any
from itertools import product

languages = {
    'es': 'Spaans',
    'en': 'Engels',
    'ch': 'Chinees'
}


class TranslationException(BaseException):
    pass


# NOTE: Callable[..., Any] defines the type as a Callable (function) with Any inputs (*args),
# and assigns it to F (function). This is just for type hinting, and isn't required, but it is fun!
# (for me anyway)
def handle_translation_key_errors[F: Callable[..., Any]](fn: F) -> F:
    def inner(*args):
        try:
            return fn(*args)
        except KeyError as ke:
            raise TranslationException(f'De woord {ke} was niet vertaald, omdat het niet in het woordenboek bestaat.')

    return inner


def handle_translation_direction_errors[F: Callable[..., Any]](fn: F) -> F:
    def inner(*args):
        err_mess = ' is geen vertaal optie. Probeer het nogmaals, maar let op de vertaal optie (b.v. 1)'
        try:
            return fn(*args)
        except KeyError as ke:
            raise TranslationException(f'{ke}' + err_mess)
        except ValueError as ve:
            raise TranslationException(
                f'{ve.args[0].split(": ")[-1]}' + err_mess)
        except TranslationException as ae:
            raise TranslationException(f'{ae}' + err_mess)

    return inner


def handle_errors[F: Callable[..., Any]](fn: F) -> F:
    def inner(*args):
        try:
            return fn(*args)
        except TranslationException as te:
            print(te)
        except Exception as e:
            print('Iets ging mis.', e)

    return inner


def validate_user_input(translation_direction, from_word):
    if not (isinstance(translation_direction, int)
            and isinstance(from_word, str)
            and 0 < translation_direction <= len(get_directions())
    ):
        raise TranslationException(translation_direction)


def es_to_ch() -> dict[str, str]:
    return {"manzana": "苹果", "plátano": "香蕉", "coche": "汽车", "casa": "房子", "libro": "书",
            "ordenador": "电脑",
            "sol": "太阳", "luna": "月亮", "árbol": "树", "agua": "水", }


def en_to_es() -> dict[str, str]:
    return {"apple": "manzana", "banana": "plátano", "car": "coche", "house": "casa", "book": "libro",
            "computer": "ordenador", "sun": "sol", "moon": "luna", "tree": "árbol", "water": "agua", }


def es_to_en() -> dict[str, str]:
    return {en_to_es()[k]: k for k in en_to_es()}


def ch_to_es() -> dict[str, str]:
    return {es_to_ch()[k]: k for k in es_to_ch()}


def en_to_ch() -> dict[str, str]:
    # assign translation dicts to vars for performance reasons
    en_to_es_dict = en_to_es()
    es_to_ch_dict = es_to_ch()

    # 1. get spanish word from en_to_es dict
    # 2. use spanish word to get chinese word from es_to_ch dict
    return {en_word: es_to_ch_dict[en_to_es_dict[en_word]] for en_word in en_to_es_dict}


def ch_to_en() -> dict[str, str]:
    # assign translation dicts to vars for performance reasons
    ch_to_es_dict = ch_to_es()
    es_to_en_dict = es_to_en()

    # 1. get spanish word from ch_to_es dict
    # 2. use spanish word to get english word from es_to_en dict
    return {ch_word: es_to_en_dict[ch_to_es_dict[ch_word]] for ch_word in ch_to_es_dict}


translation_functions = {
    'es_to_ch': es_to_ch,
    'en_to_es': en_to_es,
    'es_to_en': es_to_en,
    'ch_to_es': ch_to_es,
    'en_to_ch': en_to_ch,
    'ch_to_en': ch_to_en,
}


def get_directions() -> dict[int, list]:
    """
    Returns a dict with an int representing the number the user should type for that translation,
    and a list with the language codes to translate to, from, and which function to use, in that order. E.g.:

    :Example:
    >>> print(get_directions()[1])
     ['es', 'en', <function es_to_en at 0x120b87060>]
    """
    return {
        i + 1: [*val, translation_functions[f'{val[0]}_to_{val[1]}']] for i, val in
        enumerate(
            filter(lambda lang_comb:
                   lang_comb[0] != lang_comb[1],
                   product(languages, languages)
                   )
        )
    }


@handle_translation_key_errors
def translate(translation_direction: int, from_word: str) -> str:
    return get_directions()[translation_direction][-1]()[from_word]


def get_from_lang_and_to_lang(translation_direction: int):
    direction = get_directions()[translation_direction]
    from_lang = languages[direction[0]]
    to_lang = languages[direction[1]]

    return from_lang, to_lang


@handle_translation_direction_errors
def get_user_input() -> tuple[int, str]:
    # choose from and to lang
    directions = get_directions()
    direction_keys = list(directions.keys())
    message = 'Vertaling opties:\n'

    for i in range(len(directions)):
        message += f'({direction_keys[i]}) {languages[directions[i + 1][0]]} naar {languages[directions[i + 1][1]]}\n'

    print(message)

    u_in_option = int(input('Typ het nummer die na de vertaling optie ligt om te kiezen: '))
    # enter word to translate
    u_word_to_translate = input('Voer het woord die je wil vertalen in: ')

    validate_user_input(u_in_option, u_word_to_translate)

    return u_in_option, u_word_to_translate


def display_translation(translation_direction: int, from_word: str, to_word: str) -> None:
    if to_word is not None:
        from_lang, to_lang = get_from_lang_and_to_lang(translation_direction)
        print(f'"{from_word}" vertaald van {from_lang} naar {to_lang} is "{to_word}"')


@handle_errors
def program():
    direction, word = get_user_input()
    translated_word = translate(direction, word)

    display_translation(direction, word, translated_word)


if __name__ == "__main__":
    program()
