import os
import pytest
from recipes_bot.extractors.recipe import extract_recipe


def test_openai_syntesises_transcript():

    transcript="Here's how you're gonna fill your freezer with high protein veggie packed Chipotle black bean burritos in under an hour. This is part of my series of low effort recipes to help you eat more plants. First add diced potatoes, bell peppers, onions, and tomatoes to a sheet pan with a little bit of oil, cumin, paprika, and salt. Bake that for about 45 minutes. Now for the beans, add garlic, chipotle peppers, and two cans of black beans to a pan and saute with seasonings and salt and give that a good mash. The final piece, you're gonna blend up the cashew chipotle sauce. The full printable recipe for everything you've seen today will be on my blog. Assemble and make sure to press follow if you wanna eat healthier with me in 2025."
    recipe = extract_recipe(transcript, "test_recipe.md")
    assert recipe is not None
    assert len(recipe.title) > 5
    assert len(recipe.ingredients) == 12
