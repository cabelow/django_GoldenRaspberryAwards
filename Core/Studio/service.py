import logging

from Core.Studio.repository import StudioRepository

logger = logging.getLogger(__name__)


class StudioService:
    @staticmethod
    def get_all_studios():
        try:
            return StudioRepository.get_all_studios()
        except Exception as e:
            logger.error(f"Failed to fetch all studios: {str(e)}")
            raise

    @staticmethod
    def get_studio_by_id(studio_id):
        try:
            studio = StudioRepository.get_studio_by_id(studio_id)
            if not studio:
                logger.warning(f"Studio with ID {studio_id} not found.")
            return studio
        except Exception as e:
            logger.error(f"Error fetching studio by ID {studio_id}: {str(e)}")
            raise

    @staticmethod
    def create_studio(name):
        try:
            if StudioRepository.exists_by_name(name):
                message = f"Studio with name '{name}' already exists."
                logger.warning(message)
                raise ValueError(message)
            studio = StudioRepository.create_studio(name)
            logger.info(f"Studio '{name}' created successfully with ID {studio.id}.")
            return studio
        except Exception as e:
            logger.error(f"Error creating studio '{name}': {str(e)}")
            raise

    @staticmethod
    def update_studio(studio_id, name):
        try:
            studio = StudioRepository.update_studio(studio_id, name)
            if studio:
                logger.info(f"Studio ID {studio_id} updated successfully.")
            else:
                logger.warning(f"Studio ID {studio_id} not found.")
            return studio
        except Exception as e:
            logger.error(f"Error updating studio ID {studio_id}: {str(e)}")
            raise

    @staticmethod
    def delete_studio(studio_id):
        try:
            success = StudioRepository.delete_studio(studio_id)
            if success:
                logger.info(f"Studio ID {studio_id} deleted successfully.")
            else:
                logger.warning(f"Studio ID {studio_id} not found.")
            return success
        except Exception as e:
            logger.error(f"Error deleting studio ID {studio_id}: {str(e)}")
            raise
