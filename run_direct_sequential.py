"""
E2E Pipeline using Direct Sequential Orchestrators.

This approach explicitly calls each sub-agent in sequence.
"""

import sys
import asyncio

from backend.core import get_settings, create_app_logger
from backend.core.output_manager import get_output_manager
from backend.orchestration.direct_research_orchestrator import DirectResearchOrchestrator
from backend.orchestration.direct_production_orchestrator import DirectProductionOrchestrator


async def run_pipeline(topic: str):
    """Run the complete E2E pipeline using direct sequential orchestrators."""
    
    settings = get_settings()
    logger = create_app_logger(
        log_dir=settings.paths.logs_dir,
        level=settings.log_level
    )
    output_mgr = get_output_manager()
    
    logger.info(f"🎬 Starting E2E Pipeline: {topic}")
    logger.info("=" * 80)
    
    try:
        # --- Research Phase ---
        logger.info("\n📚 PHASE 1: Research (Sequential Sub-Agents)")
        logger.info("-" * 80)
        
        research_orch = DirectResearchOrchestrator()
        research_output, _ = await research_orch.execute_research(topic, save_output=False)
        
        logger.info(f"✅ Research complete: {len(research_output)} chars")
        
        # Save research
        research_path = output_mgr.save_research_report(
            topic=topic,
            content=research_output,
            metadata={'orchestrator': 'DirectResearchOrchestrator', 'topic': topic}
        )
        logger.info(f"   Research saved: {research_path}")
        
        # --- Production Phase ---
        logger.info("\n🎬 PHASE 2: Production (Sequential Sub-Agents)")
        logger.info("-" * 80)
        
        production_orch = DirectProductionOrchestrator()
        production_output, _ = await production_orch.execute_production(research_output, save_output=False)
        
        logger.info(f"✅ Production complete: {len(production_output)} chars")
        
        # Save production script
        script_path = output_mgr.save_production_script(
            topic=topic,
            content=production_output,
            metadata={'orchestrator': 'DirectProductionOrchestrator', 'topic': topic}
        )
        logger.info(f"   Script saved: {script_path}")
        
        # Save session data
        session_data = {
            'topic': topic,
            'research_length': len(research_output),
            'production_length': len(production_output),
            'research_path': research_path,
            'script_path': script_path,
        }
        session_path = output_mgr.save_session_data('direct_sequential', session_data)
        
        # --- Summary ---
        logger.info("\n" + "=" * 80)
        logger.info("✨ PIPELINE COMPLETE")
        logger.info("=" * 80)
        logger.info(f"Research: {len(research_output)} chars → {research_path}")
        logger.info(f"Production: {len(production_output)} chars → {script_path}")
        logger.info(f"Session data: {session_path}")
        
    except Exception as e:
        logger.error(f"❌ Pipeline failed: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_direct_sequential.py \"Your Topic\"")
        sys.exit(1)
    
    topic = sys.argv[1]
    asyncio.run(run_pipeline(topic))
