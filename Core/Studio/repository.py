from Core.Studio.models import Studio


class StudioRepository:
    @staticmethod
    def get_all_studios():
        return Studio.objects.all()

    @staticmethod
    def get_studio_by_id(studio_id):
        try:
            return Studio.objects.get(id=studio_id)
        except Studio.DoesNotExist:
            return None

    @staticmethod
    def get_or_create_studio(studio_data):
        studio, _ = Studio.objects.get_or_create(
            name=studio_data['name'].strip()
        )
        return studio

    @staticmethod
    def create_studio(name):
        return Studio.objects.create(name=name)

    @staticmethod
    def exists_by_name(name):
        return Studio.objects.filter(name=name).exists()

    @staticmethod
    def update_studio(studio_id, name):
        studio = StudioRepository.get_studio_by_id(studio_id)
        if studio:
            studio.name = name
            studio.save()
            return studio
        return None

    @staticmethod
    def delete_studio(studio_id):
        studio = StudioRepository.get_studio_by_id(studio_id)
        if studio:
            studio.delete()
            return True
        return False
