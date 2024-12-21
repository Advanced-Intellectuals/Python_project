from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataUpdateScheduler:
    def __init__(self, data, recommender):
        self.scheduler = AsyncIOScheduler()
        self.data = data
        self.recommender = recommender

    async def update_data(self):
        """Обновляет данные из базы данных"""
        try:
            logger.info("Starting data update...")
            
            # Загружаем новые данные
            await self.data.load_data()
            self.data.data_preprocessing()
            
            logger.info("Data successfully updated")
            
        except Exception as e:
            logger.error(f"Error updating data: {e}")

    def start(self):
        """Запускает планировщик с часовым интервалом"""
        self.scheduler.add_job(
            self.update_data,
            trigger=IntervalTrigger(hours=1),
            id='data_update',
            name='Update recommendation data',
            replace_existing=True
        )
        self.scheduler.start()
        logger.info("Scheduler started - data will be updated every hour")

    def stop(self):
        """Останавливает планировщик"""
        self.scheduler.shutdown()
        logger.info("Scheduler stopped") 