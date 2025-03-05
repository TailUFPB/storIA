import pytest
from unittest.mock import patch
from app.story import StoryGenerator


@pytest.fixture
def story_generator_fixture():
    """
    Cria uma instância de StoryGenerator,
    mas evita carregar o modelo real.
    """
    with patch("app.story.AutoModelForCausalLM.from_pretrained"), \
         patch("app.story.AutoTokenizer.from_pretrained"), \
         patch("app.story.pipeline"):
        generator = StoryGenerator()
        return generator


def test_generate_story_basic(story_generator_fixture):
    """
    Teste básico para verificar se generate_story retorna
    algo formatado quando a pipeline é mockada.
    """
    mock_return = [{'generated_text': "era uma vez..."}]
    with patch.object(story_generator_fixture, 'writer', return_value=mock_return):
        texto_inicial = "início"
        story = story_generator_fixture.generate_story(texto_inicial, size=10, temperature=0.7)
        
        # Verifica se o texto retornado contém (no mínimo) algo esperado
        assert "Era uma vez. . ." in story, f"Esperado ter 'Era uma vez...', mas foi '{story}'"


def test_generate_story_parameters(story_generator_fixture):
    """
    Verifica se os parâmetros passados para pipeline
    são consistentes com o que definimos no código.
    """
    with patch.object(story_generator_fixture, 'writer') as mock_writer:
        story_generator_fixture.generate_story("início", 15, 1.0)
        mock_writer.assert_called_once()

        # Recupera os argumentos usados na chamada
        _, kwargs = mock_writer.call_args
        expected_max_length = len("início".split()) + 15

        assert kwargs["max_length"] == expected_max_length, \
            f"Esperado max_length={expected_max_length}, mas obteve {kwargs['max_length']}."
        assert kwargs["temperature"] == 1.0, f"Esperado temperature=1.0, obteve {kwargs['temperature']}."
        assert kwargs["repetition_penalty"] == 1.2
        assert kwargs["num_beams"] == 5
        assert kwargs["no_repeat_ngram_size"] == 3
        assert kwargs["truncation"] is True


def test_generate_story_exception(story_generator_fixture):
    """
    Verifica se a exceção é levantada corretamente se a pipeline falha.
    """
    with patch.object(story_generator_fixture, 'writer', side_effect=Exception("Simulando erro na geração")):
        with pytest.raises(Exception) as exc_info:
            story_generator_fixture.generate_story("qualquer texto", 10, 0.7)
        assert "Simulando erro na geração" in str(exc_info.value), "Mensagem de erro inesperada"


def test_generate_story_integration_format(story_generator_fixture):
    """
    Teste para garantir que generate_story chame 'format_text' ao final,
    resultando em texto capitalizado e formatado.
    """
    mock_return = [{'generated_text': "once upon a time there was a   story"}]
    with patch.object(story_generator_fixture, 'writer', return_value=mock_return):
        story = story_generator_fixture.generate_story("once", 10, 0.7)
        # Se 'format_text' for chamado, esperamos "Once upon a time there was a story"
        assert "Once upon a time there was a story" in story, f"Texto formatado inesperado: {story}"
