class BlacklistedVacancyError(Exception):
    """Вакансия в черном списке."""

    def __init__(self):
        super().__init__("Вакансия в черном списке.")
