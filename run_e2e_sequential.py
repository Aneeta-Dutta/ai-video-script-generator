"""
E2E Pipeline using ADK SequentialAgent workflow.

Simplified approach using ADK's built-in pattern.
"""

import sys
import asyncio
from pathlib import Path

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from backend.core import get_settings, create_app_logger
from backend.orchestration.research_pipeline import research_pipeline_agent
from backend.orchestration.production_pipeline import production_pipeline_agent


async def run_pipeline(topic: str):
    """Run the complete E2E pipeline using ADK SequentialAgents."""
    
    settings = get_settings()
    logger = create_app_logger(
        log_dir=settings.paths.logs_dir,
        level=settings.log_level
    )
    
    logger.info(f"🎬 Starting E2E Pipeline: {topic}")
    logger.info("=" * 80)
    
    try:
        # --- Research Phase ---
        logger.info("\n📚 PHASE 1: Research")
        logger.info("-" * 80)
        
        # Create session service and runner for research
        research_session_service = InMemorySessionService()
        research_runner = Runner(
            agent=research_pipeline_agent,
            session_service=research_session_service,
            app_name="research_pipeline"
        )
        
        # Create session
        await research_session_service.create_session(
            user_id="user_01",
            session_id="research_session",
            app_name="research_pipeline"
        )
        
        # Run research pipeline
        research_output = ""
        async for event in research_runner.run_async(
            user_id="user_01",
            session_id="research_session",
            new_message=types.Content(
                role="user",
                parts=[types.Part(text=f"Research topic: {topic}")]
            )
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        research_output += part.text
        
        logger.info(f"✅ Research complete: {len(research_output)} chars")
        
        # Save research using OutputManager
        from backend.core.output_manager import get_output_manager
        output_mgr = get_output_manager()
        
        research_path = output_mgr.save_research_report(
            topic=topic,
            content=research_output or "No research output generated",
            metadata={'session_id': 'research_session', 'topic': topic}
        )
        logger.info(f"   Research saved: {research_path}")
        
        # --- Production Phase ---
        logger.info("\\n🎬 PHASE 2: Production")
        logger.info("-" * 80)
        
        # Create session service and runner for production
        production_session_service = InMemorySessionService()
        production_runner = Runner(
            agent=production_pipeline_agent,
            session_service=production_session_service,
            app_name="production_pipeline"
        )
        
        await production_session_service.create_session(
            user_id="user_01",
            session_id="production_session",
            app_name="production_pipeline"
        )
        
        # Run production pipeline
        production_output = ""
        async for event in production_runner.run_async(
            user_id="user_01",
            session_id="production_session",
            new_message=types.Content(
                role="user",
                parts=[types.Part(text=f"Create shooting script for: {research_output or topic}")]
            )
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        production_output += part.text
        
        logger.info(f"✅ Production complete: {len(production_output)} chars")
        
        # Save production script using OutputManager  
        script_path = output_mgr.save_production_script(
            topic=topic,
            content=production_output or "No production output generated",
            metadata={'session_id': 'production_session', 'topic': topic}
        )
        
        # --- Summary ---
        logger.info("\n" + "=" * 80)
        logger.info("✨ PIPELINE COMPLETE")
        logger.info("=" * 80)
        logger.info(f"Research: {len(research_output)} chars → {research_path}")
        logger.info(f"Production: {len(production_output)} chars → {script_path}")
        
    except Exception as e:
        logger.error(f"❌ Pipeline failed: {str(e)}")
        raise


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_e2e_sequential.py \"Your Topic\"")
        sys.exit(1)
    
    topic = sys.argv[1]
    asyncio.run(run_pipeline(topic))
