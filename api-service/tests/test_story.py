import pytest
from unittest.mock import patch
from app.story import StoryGenerator

@pytest.fixture
def story_generator_fixture():
    """
    Cria uma instância de StoryGenerator, mas evita carregar o modelo real,
    pois para testar apenas 'clean_text' não precisamos baixar/puxar o modelo.
    """
    with patch("app.story.AutoModelForCausalLM.from_pretrained"), \
         patch("app.story.AutoTokenizer.from_pretrained"), \
         patch("app.story.pipeline"):
        
        story_generator = StoryGenerator()
        return story_generator

def test_clean_text_remove_trailing_spaces(story_generator_fixture):
    """
    Verifica se o método clean_text remove espaços em branco
    ao final da string.
    """
    input_text = "texto de teste    "
    expected = "texto de teste"
    result = story_generator_fixture.clean_text(input_text)
    assert result == expected.lower(), f"Esperado '{expected.lower()}', mas obteve '{result}'"

def test_clean_text_converts_to_lowercase(story_generator_fixture):
    """
    Verifica se o método clean_text converte o texto para minúsculo.
    """
    input_text = "TEXTO EM MAIÚSCULAS  "
    # Para ficar claro, após remover trailing spaces, deve ficar "TEXTO EM MAIÚSCULAS"
    # e então converter para minúsculo -> "texto em maiúsculas"
    expected = "texto em maiúsculas"
    result = story_generator_fixture.clean_text(input_text)
    assert result == expected, f"Esperado '{expected}', mas obteve '{result}'"

def test_clean_text_without_trailing_spaces(story_generator_fixture):
    """
    Verifica o comportamento caso não haja espaços ao final.
    O texto deve apenas ser convertido para minúsculo.
    """
    input_text = "Já está sem espaços"
    expected = "já está sem espaços"
    result = story_generator_fixture.clean_text(input_text)
    assert result == expected, f"Esperado '{expected}', mas obteve '{result}'"
