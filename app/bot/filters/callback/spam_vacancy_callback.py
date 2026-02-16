from aiogram.filters.callback_data import CallbackData


class SpamVacancyCallback(CallbackData, prefix="spam_vacancy"):
    """
    Callback-данные для пометки вакансии как спам.

    Attributes:
        vacancy_id (int): Уникальный идентификатор вакансии, которую нужно пометить как спам.

    Этот callback используется для inline-кнопок, чтобы бот мог определить,
    какую именно вакансию пользователь считает спамом и обработать это действие.
    """

    vacancy_id: int


class SpamVacancyCallbackForAdmin(CallbackData, prefix="spam_admin"):
    user_id: int
    vacancy_id: int
    message_id: int

class SpamAndIncrementUserBonusForSpamVacancyCallback(
    SpamVacancyCallbackForAdmin, prefix="spam_increment"
):
    ...
class IncrementUserBonusForSpamVacancyCallback(
    SpamVacancyCallbackForAdmin, prefix="increment"
):
    message_id: int = 0

class NotSpamButDeleteMessagesForSpamVacancyCallback(
    SpamVacancyCallbackForAdmin, prefix="not_spam"
):
    ...

class RejectSpamVacancyCallback(SpamVacancyCallbackForAdmin, prefix="reject_spam"):
    message_id: int = 0
