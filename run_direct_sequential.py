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


async def run_pipeline(topic: str, output_format: str = "json"):
    """Run the complete E2E pipeline using direct sequential orchestrators."""
    
    settings = get_settings()
    logger = create_app_logger(
        log_dir=settings.paths.logs_dir,
        level=settings.log_level
    )
    output_mgr = get_output_manager()
    
    logger.info(f"🎬 Starting [PROD-HOUSE] E2E Pipeline: {topic}")
    logger.info("=" * 80)
    
    try:
        # --- Research Phase ---
        logger.info("\n📚 PHASE 1: Research (Sequential & Crisp)")
        logger.info("-" * 80)
        
        research_orch = DirectResearchOrchestrator()
        research_output, _ = await research_orch.execute_research(topic, save_output=False)
        
        logger.info(f"✅ Research complete: {len(research_output)} chars (Crisp Edition)")
        
        # Save research as Markdown (Internal Reference)
        research_path = output_mgr.save_research_report(
            topic=topic,
            content=research_output,
            metadata={'orchestrator': 'DirectResearchOrchestrator', 'edition': 'Crisp-Production'}
        )
        
        # --- Production Phase ---
        logger.info("\n🎬 PHASE 2: Production (JSON-Optimized & Bengali)")
        logger.info("-" * 80)
        
        production_orch = DirectProductionOrchestrator()
        production_json, session_id = await production_orch.execute_production(
            research_output, 
            save_output=True, 
            output_format=output_format
        )
        
        if output_format == "json":
            import json
            logger.info("✅ Production complete: Structured JSON Export generated.")
            logger.info(f"   Scene Title: {production_json['scenes'][0]['title']}")
            logger.info(f"   Bengali Dialogue: {len(production_json['scenes'][0]['dialogue_bengali'])} chars")
            
            # Save for final delivery
            delivery_path = output_mgr.save_session_data(f"delivery_{session_id}", production_json)
            logger.info(f"📦 FINAL DELIVERY READY: {delivery_path}")
        else:
            logger.info(f"✅ Production complete: {len(production_json)} chars")
        
        # --- Summary ---
        logger.info("\n" + "=" * 80)
        logger.info("✨ PRODUCTION RECORD READY")
        logger.info("=" * 80)
        if output_format == "json":
            logger.info(f"Research Path: {research_path}")
            logger.info(f"Delivery Path: {delivery_mgr_path if 'delivery_mgr_path' in locals() else 'Check outputs/sessions'}")
        
    except Exception as e:
        logger.error(f"❌ Pipeline failed: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise
        
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
