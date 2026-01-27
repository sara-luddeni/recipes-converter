"""Recipe extraction from transcript text using LLM."""

import json
import os
import tempfile
from pathlib import Path
from typing import Dict, Any

from openai import OpenAI

from .models import Recipe
from .audio import transcribe
from ..downloaders.tiktok import TikTokDownloader


def extract_recipe(transcript: str, output_path: str, model: str = "gpt-4o-mini") -> Recipe:
    """
    Extract structured recipe information from transcript text using LLM.
    
    Args:
        transcript: Recipe transcript text from video
        output_path: Path where the Markdown recipe file will be saved
        model: OpenAI model to use (default: gpt-4o-mini)
        
    Returns:
        Recipe object with extracted information
        
    Raises:
        ValueError: If transcript is empty or API key is missing
        RuntimeError: If LLM extraction fails or API call fails
    """
    if not transcript or not transcript.strip():
        raise ValueError("Transcript text cannot be empty")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable is required. "
            "Please set it with your OpenAI API key."
        )
    
    client = OpenAI(api_key=api_key)
    
    system_prompt = """You are a recipe extraction assistant. Extract structured recipe information from transcript text.
Extract:
1. A clear recipe title
2. A list of ingredients with quantities (normalize units when possible)
3. Step-by-step instructions in order

Handle common transcript issues like filler words, repetitions, and incomplete sentences.
Return the result as JSON with keys: "title", "ingredients" (array of strings), and "instructions" (array of strings)."""
    
    user_prompt = f"""Extract the recipe information from this transcript:

{transcript}

Return only valid JSON with the structure:
{{
  "title": "Recipe Title",
  "ingredients": ["ingredient with quantity", ...],
  "instructions": ["step 1", "step 2", ...]
}}"""
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3,
        )
        
        content = response.choices[0].message.content
        if not content:
            raise RuntimeError("LLM returned empty response")
        
        recipe_data: Dict[str, Any] = json.loads(content)
        
        if "title" not in recipe_data or "ingredients" not in recipe_data or "instructions" not in recipe_data:
            raise RuntimeError("LLM response missing required fields")
        
        recipe = Recipe(
            title=recipe_data["title"].strip(),
            ingredients=[ing.strip() for ing in recipe_data["ingredients"] if ing.strip()],
            instructions=[inst.strip() for inst in recipe_data["instructions"] if inst.strip()]
        )
        
        if not recipe.title:
            raise RuntimeError("Extracted recipe title is empty")
        if not recipe.ingredients:
            raise RuntimeError("Extracted recipe has no ingredients")
        if not recipe.instructions:
            raise RuntimeError("Extracted recipe has no instructions")
        
        markdown_content = _format_recipe_as_markdown(recipe)
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(markdown_content, encoding="utf-8")
        
        return recipe
        
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse LLM response as JSON: {e}") from e
    except Exception as e:
        if isinstance(e, (ValueError, RuntimeError)):
            raise
        raise RuntimeError(f"Failed to extract recipe from transcript: {e}") from e


def extract_recipe_from_video(video_path: str, output_path: str, model: str = "gpt-4o-mini") -> Recipe:
    """
    Extract recipe from video by transcribing audio and extracting structured recipe information.
    
    Args:
        video_path: Path to input video file (.mp4)
        output_path: Path where the Markdown recipe file will be saved
        model: OpenAI model to use for extraction (default: gpt-4o-mini)
        
    Returns:
        Recipe object with extracted information
        
    Raises:
        FileNotFoundError: If video file not found
        ValueError: If transcript is empty or API key is missing
        RuntimeError: If transcription or extraction fails
    """
    transcript = transcribe(video_path)
    return extract_recipe(transcript, output_path, model)


def extract_recipe_from_url(url: str, output_path: str, model: str = "gpt-4o-mini") -> Recipe:
    """
    Download video from URL, extract recipe, and clean up the temporary video file.
    
    Args:
        url: TikTok video URL to download
        output_path: Path where the Markdown recipe file will be saved
        model: OpenAI model to use for extraction (default: gpt-4o-mini)
        
    Returns:
        Recipe object with extracted information
        
    Raises:
        FileNotFoundError: If video download fails
        ValueError: If transcript is empty or API key is missing
        RuntimeError: If transcription or extraction fails
    """
    temp_video_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
            temp_video_path = temp_file.name
        
        TikTokDownloader.download(url, temp_video_path)
        return extract_recipe_from_video(temp_video_path, output_path, model)
    finally:
        if temp_video_path:
            Path(temp_video_path).unlink(missing_ok=True)


def _format_recipe_as_markdown(recipe: Recipe) -> str:
    """
    Format Recipe object as Markdown text.
    
    Args:
        recipe: Recipe object to format
        
    Returns:
        Markdown formatted string
    """
    lines = [
        f"# {recipe.title}",
        "",
        "## Ingredients",
        ""
    ]
    
    for ingredient in recipe.ingredients:
        lines.append(f"- {ingredient}")
    
    lines.extend([
        "",
        "## Instructions",
        ""
    ])
    
    for i, instruction in enumerate(recipe.instructions, start=1):
        lines.append(f"{i}. {instruction}")
    
    return "\n".join(lines)
