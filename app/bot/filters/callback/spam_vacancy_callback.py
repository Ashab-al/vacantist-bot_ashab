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


class SpamVacancyCallbackForAdmin(CallbackData, prefix="spam_vacancy_admin"):
    vacancy_id: int
    user_id: int
    message_id: int


class IncrementUserBonusForSpamVacancyCallback(
    CallbackData, prefix="increment_user_bonus"
):
    user_id: int
    vacancy_id: int

class SpamAndIncrementUserBonusForSpamVacancyCallback(
    CallbackData, prefix="spam_and_increment_user_bonus"
):
    user_id: int
    vacancy_id: int
    message_id: int

class NotSpamButDeleteMessagesForSpamVacancyCallback(
    CallbackData, prefix="not_spam_but_delete_messages"
):
    user_id: int
    vacancy_id: int
    message_id: int

class RejectSpamVacancyCallback(CallbackData, prefix="reject_spam_vacancy"):
    vacancy_id: int
    user_id: int
